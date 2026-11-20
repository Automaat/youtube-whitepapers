"""Headless Claude Code (`claude -p`) steps of the episode pipeline.

Each step is a separate `claude -p` process with its own prompt file, tool
allowlist and budget, so the scenario reviewer never sees the writer's session.
Every call appends its cost to build/costs.json.
"""

import json
import subprocess
import threading
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from pathlib import Path

from odczyt.episode import Episode
from odczyt.paths import PROMPTS_DIR

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


META_SCHEMA: dict = {
    "type": "object",
    "required": ["title", "subtitle", "authors", "paper_url"],
    "properties": {
        "title": {"type": "string"},
        "subtitle": {"type": "string"},
        "authors": {"type": "string"},
        "paper_url": {"type": "string"},
    },
}

METADATA_SCHEMA: dict = {
    "type": "object",
    "required": ["title", "intro", "topics", "publication", "tags"],
    "properties": {
        "title": {"type": "string"},
        "intro": {"type": "string"},
        "topics": {"type": "array", "items": {"type": "string"}},
        "publication": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
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


TYPECHECK = "Bash(npm --prefix youtube/remotion run typecheck)"
SCENE_BASH = [TYPECHECK, "Bash(uv run odczyt stills *)"]

STEPS: dict[str, Step] = {
    "meta": Step("meta.md", ["Read"], "sonnet", 1.5, schema=META_SCHEMA),
    "storyboard": Step("storyboard.md", ["Read", "Write"], "opus", 6.0),
    "script": Step("script.md", ["Read", "Write"], "opus", 8.0),
    "review": Step("review.md", ["Read"], "opus", 8.0, schema=REVIEW_SCHEMA),
    "script-fix": Step("script-fix.md", ["Read", "Edit"], "opus", 5.0),
    "layout": Step("layout.md", ["Read", "Write", "Bash"], "opus", 4.0, allowed_bash=[TYPECHECK]),
    "scenes": Step(
        "scenes.md", ["Read", "Write", "Edit", "Bash"], "opus", 30.0, allowed_bash=SCENE_BASH
    ),
    "stills-review": Step("stills-review.md", ["Read"], "opus", 8.0, schema=STILLS_SCHEMA),
    "scenes-fix": Step(
        "scenes-fix.md", ["Read", "Edit", "Bash"], "opus", 20.0, allowed_bash=SCENE_BASH
    ),
    "metadata": Step("metadata.md", ["Read"], "opus", 2.0, schema=METADATA_SCHEMA),
}


@dataclass
class LlmResult:
    ok: bool
    message: str
    cost: float = 0.0
    data: dict | None = None


_COST_LOCK = threading.Lock()


def render_prompt(template: str, ep: Episode, extra: dict[str, str] | None = None) -> str:
    """Fill {placeholders} in a prompt template; unknown placeholders stay as they are."""
    minutes = int(ep.config.get("target_minutes", 12))
    values = {
        "scope": "all stills",
        **(extra or {}),
        "episode": str(ep.number),
        "episode_dir": ep.rel(ep.dir),
        "slug": ep.slug,
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


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_review(ep: Episode, review: dict) -> None:
    """Write review.json, claims.json and review.md next to the episode files."""
    write_json(ep.file("review.json"), review)
    write_json(ep.file("claims.json"), review["claims"])
    ep.file("review.md").write_text(format_review_md(review), encoding="utf-8")


def record_cost(ep: Episode, label: str, result: dict) -> float:
    """Append one call to build/costs.json; return its cost."""
    cost = float(result.get("total_cost_usd") or 0.0)
    path = ep.build / "costs.json"
    with _COST_LOCK:
        entries = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
        entries.append(
            {
                "label": label,
                "usd": round(cost, 4),
                "turns": result.get("num_turns"),
                "at": datetime.now(UTC).isoformat(timespec="seconds"),
            }
        )
        write_json(path, entries)
    return cost


def total_cost(ep: Episode) -> float:
    path = ep.build / "costs.json"
    if not path.exists():
        return 0.0
    return sum(e["usd"] for e in json.loads(path.read_text(encoding="utf-8")))


def run_step(
    ep: Episode,
    name: str,
    extra: dict[str, str] | None = None,
    label: str | None = None,
    model: str | None = None,
) -> LlmResult:
    """Run one step as `claude -p`; return its result (structured data for schema steps)."""
    step = STEPS[name]
    if model:
        step = replace(step, model=model)
    label = label or name
    prompt = render_prompt((PROMPTS_DIR / step.prompt).read_text(encoding="utf-8"), ep, extra)
    print(f"🔄 {label}: claude -p ({step.model}, budget ${step.budget_usd})", flush=True)
    proc = subprocess.run(build_command(step, prompt), cwd=ep.repo, capture_output=True, text=True)
    log = ep.build / f"{label}.log.json"
    log.write_text(proc.stdout or proc.stderr, encoding="utf-8")
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return LlmResult(False, f"{label}: claude -p failed (exit {proc.returncode}); see {log}")
    cost = record_cost(ep, label, result)
    if result.get("is_error"):
        return LlmResult(False, f"{label}: {result.get('subtype')}: {result.get('result')}", cost)
    data = None
    if step.schema is not None:
        data = result.get("structured_output")
        if not isinstance(data, dict):
            return LlmResult(False, f"{label}: no structured output; see {log}", cost)
    message = str(result.get("result", "")).strip()
    print(f"✅ {label} (${cost:.2f}, {result.get('num_turns')} turns)", flush=True)
    return LlmResult(True, message, cost, data)
