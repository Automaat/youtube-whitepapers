#!/usr/bin/env python3
"""Run one LLM step of the episode pipeline as headless Claude Code (`claude -p`).

Each step is a separate `claude -p` process with its own prompt file and tool
allowlist, so the scenario reviewer never sees the writer's session.

Usage:
    python scripts/run_llm_step.py 73 storyboard
    python scripts/run_llm_step.py 73 script
    python scripts/run_llm_step.py 73 review        # writes review.json, review.md, claims.json
    python scripts/run_llm_step.py 73 script-fix
    python scripts/run_llm_step.py 73 scenes
    python scripts/run_llm_step.py 73 stills-review
    python scripts/run_llm_step.py 73 scenes-fix
"""

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from episode_pipeline import (
    PROMPTS_DIR,
    REPO_DIR,
    build_dir,
    find_episode_dir,
    load_episode,
)

CHARS_PER_MINUTE = 1000

REVIEW_SCHEMA: dict = {
    "type": "object",
    "required": ["verdict", "summary", "claims", "coverage", "skeptic_loop", "must_fix"],
    "properties": {
        "verdict": {"enum": ["pass", "fail"]},
        "summary": {"type": "string"},
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["segment", "claim", "verdict", "location", "quote"],
                "properties": {
                    "segment": {"type": "string"},
                    "claim": {"type": "string"},
                    "verdict": {
                        "enum": ["supported", "simplified-ok", "misleading", "unsupported", "wrong"]
                    },
                    "location": {"type": "string"},
                    "quote": {"type": "string"},
                    "note": {"type": "string"},
                },
            },
        },
        "coverage": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["contribution", "covered_in", "omission_reason"],
                "properties": {
                    "contribution": {"type": "string"},
                    "covered_in": {"type": "array", "items": {"type": "string"}},
                    "omission_reason": {"type": "string"},
                },
            },
        },
        "skeptic_loop": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["question_segment", "answer_segment", "ok"],
                "properties": {
                    "question_segment": {"type": "string"},
                    "answer_segment": {"type": "string"},
                    "ok": {"type": "boolean"},
                    "note": {"type": "string"},
                },
            },
        },
        "must_fix": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["segment", "problem", "fix"],
                "properties": {
                    "segment": {"type": "string"},
                    "problem": {"type": "string"},
                    "fix": {"type": "string"},
                },
            },
        },
    },
}

STILLS_SCHEMA: dict = {
    "type": "object",
    "required": ["verdict", "findings"],
    "properties": {
        "verdict": {"enum": ["pass", "fail"]},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["still", "scene", "severity", "problem", "fix"],
                "properties": {
                    "still": {"type": "string"},
                    "scene": {"type": "string"},
                    "severity": {"enum": ["blocker", "minor"]},
                    "problem": {"type": "string"},
                    "fix": {"type": "string"},
                },
            },
        },
    },
}


@dataclass(frozen=True)
class Step:
    prompt: str
    tools: list[str]
    model: str
    budget_usd: float
    allowed_bash: list[str] = field(default_factory=list)
    schema: dict | None = None


SCENE_BASH = [
    "Bash(npm --prefix youtube/remotion run typecheck)",
    "Bash(uv run python scripts/render_episode.py stills *)",
]

STEPS: dict[str, Step] = {
    "storyboard": Step("storyboard.md", ["Read", "Write"], "opus", 6.0),
    "script": Step("script.md", ["Read", "Write"], "opus", 8.0),
    "review": Step("review.md", ["Read"], "opus", 8.0, schema=REVIEW_SCHEMA),
    "script-fix": Step("script-fix.md", ["Read", "Edit"], "opus", 5.0),
    "scenes": Step(
        "scenes.md", ["Read", "Write", "Edit", "Bash"], "opus", 30.0, allowed_bash=SCENE_BASH
    ),
    "stills-review": Step("stills-review.md", ["Read"], "opus", 8.0, schema=STILLS_SCHEMA),
    "scenes-fix": Step(
        "scenes-fix.md", ["Read", "Edit", "Bash"], "opus", 20.0, allowed_bash=SCENE_BASH
    ),
}


def render_prompt(
    template: str, episode_dir: Path, episode: dict, extra: dict[str, str] | None = None
) -> str:
    """Fill {placeholders} in a prompt template."""
    minutes = int(episode.get("target_minutes", 12))
    values = {
        "scope": "all stills",
        **(extra or {}),
        "episode": str(episode["number"]),
        "episode_dir": str(episode_dir.relative_to(REPO_DIR)),
        "slug": episode["slug"],
        "target_minutes": str(minutes),
        "target_chars": str(minutes * CHARS_PER_MINUTE),
    }
    for key, value in values.items():
        template = template.replace("{" + key + "}", value)
    return template


def build_command(step: Step, prompt: str) -> list[str]:
    """Build the `claude -p` argument list for a step."""
    cmd = [
        "claude",
        "-p",
        prompt,
        "--output-format",
        "json",
        "--model",
        step.model,
        "--no-session-persistence",
        "--restricted",
        "--strict-mcp-config",
        "--permission-mode",
        "acceptEdits",
        "--max-budget-usd",
        str(step.budget_usd),
        "--tools",
        ",".join(step.tools),
    ]
    if step.allowed_bash:
        cmd += ["--allowedTools", *step.allowed_bash]
    if step.schema is not None:
        cmd += ["--json-schema", json.dumps(step.schema)]
    return cmd


def format_review_md(review: dict) -> str:
    """Render the review JSON as Markdown for the owner's sign-off."""
    counts: dict[str, int] = {}
    for claim in review["claims"]:
        counts[claim["verdict"]] = counts.get(claim["verdict"], 0) + 1
    lines = [
        "# Scenario review",
        "",
        f"**Verdict:** {review['verdict']}",
        "",
        review["summary"],
        "",
        "| Verdict | Claims |",
        "|---|---|",
        *[f"| {k} | {v} |" for k, v in sorted(counts.items())],
        "",
        "## Must fix",
        "",
    ]
    if not review["must_fix"]:
        lines.append("None.")
    for item in review["must_fix"]:
        lines.append(f"- **{item['segment']}**: {item['problem']} → {item['fix']}")
    lines += ["", "## Claims", "", "| Segment | Verdict | Claim | Location |", "|---|---|---|---|"]
    for c in review["claims"]:
        claim = c["claim"].replace("|", "\\|")
        lines.append(f"| {c['segment']} | {c['verdict']} | {claim} | {c['location']} |")
    lines += ["", "## Coverage", ""]
    for c in review["coverage"]:
        where = ", ".join(c["covered_in"]) or f"omitted: {c['omission_reason']}"
        lines.append(f"- {c['contribution']}: {where}")
    lines += ["", "## Skeptic loop", ""]
    for s in review["skeptic_loop"]:
        mark = "✅" if s["ok"] else "❌"
        lines.append(
            f"- {mark} {s['question_segment']} → {s['answer_segment']} {s.get('note', '')}"
        )
    return "\n".join(lines) + "\n"


def save_structured(step_name: str, episode_dir: Path, data: dict, stem: str | None = None) -> None:
    """Write structured step output next to the episode files."""
    if step_name == "review":
        (episode_dir / "review.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (episode_dir / "claims.json").write_text(
            json.dumps(data["claims"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (episode_dir / "review.md").write_text(format_review_md(data), encoding="utf-8")
    elif step_name == "stills-review":
        out = build_dir(episode_dir) / f"{stem or step_name}.json"
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("episode")
    parser.add_argument("step", choices=sorted(STEPS))
    parser.add_argument("--model", help="Override the step's model")
    parser.add_argument(
        "--var", action="append", default=[], help="Extra prompt placeholder KEY=VALUE"
    )
    parser.add_argument("--log-name", help="Log file stem (default: step name)")
    parser.add_argument("--dry-run", action="store_true", help="Print the prompt only")
    args = parser.parse_args()

    episode_dir = find_episode_dir(args.episode)
    if episode_dir is None:
        print(f"❌ No episode directory for {args.episode}")
        return 1
    episode = load_episode(episode_dir)
    step = STEPS[args.step]
    if args.model:
        step = Step(**{**step.__dict__, "model": args.model})
    extra = dict(v.split("=", 1) for v in args.var)
    prompt = render_prompt(
        (PROMPTS_DIR / step.prompt).read_text(encoding="utf-8"), episode_dir, episode, extra
    )
    if args.dry_run:
        print(prompt)
        return 0

    print(f"🔄 {args.step}: claude -p ({step.model}, budget ${step.budget_usd})")
    proc = subprocess.run(build_command(step, prompt), cwd=REPO_DIR, capture_output=True, text=True)
    log = build_dir(episode_dir) / f"{args.log_name or args.step}.log.json"
    log.write_text(proc.stdout or proc.stderr, encoding="utf-8")
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(f"❌ claude -p failed (exit {proc.returncode}); see {log}")
        print(proc.stderr[-2000:])
        return 1
    if result.get("is_error"):
        print(f"❌ {result.get('subtype')}: {str(result.get('result'))[:2000]}")
        return 1
    if step.schema is not None:
        data = result.get("structured_output")
        if not isinstance(data, dict):
            print(f"❌ No structured output; see {log}")
            return 1
        save_structured(args.step, episode_dir, data, args.log_name)
        print(f"📋 verdict: {data['verdict']}")
    print(str(result.get("result", "")).strip()[:2000])
    print(
        f"✅ {args.step} done (${result.get('total_cost_usd', 0):.2f}, {result.get('num_turns')} turns)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
