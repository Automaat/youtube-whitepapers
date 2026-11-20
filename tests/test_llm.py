"""Tests for odczyt.llm."""

import json

import pytest

from odczyt.llm import (
    STEPS,
    build_command,
    format_review_md,
    record_cost,
    render_prompt,
    total_cost,
)


def test_render_prompt_fills_placeholders(episode):
    out = render_prompt(
        "{episode_dir} {slug} {target_minutes} {target_chars} {episode} {part} {scope} {unknown}",
        episode,
        {"part": "part1"},
    )
    assert out == "youtube/pl/episodes/73-raft 73-raft 12 12000 73 part1 all stills {unknown}"


def test_review_step_is_read_only_with_schema():
    cmd = build_command(STEPS["review"], "prompt")
    assert cmd[:3] == ["claude", "-p", "prompt"]
    assert cmd[cmd.index("--tools") + 1] == "Read"
    assert "--restricted" in cmd
    assert json.loads(cmd[cmd.index("--json-schema") + 1])["required"][0] == "verdict"
    assert "--allowedTools" not in cmd


def allowed_tools(cmd: list[str]) -> list[str]:
    rest = cmd[cmd.index("--allowedTools") + 1 :]
    return rest[: next((i for i, a in enumerate(rest) if a.startswith("--")), len(rest))]


@pytest.mark.parametrize("step", ["scenes", "scenes-fix"])
def test_scene_steps_allow_only_typecheck_and_stills(step):
    assert allowed_tools(build_command(STEPS[step], "p")) == [
        "Bash(npm --prefix youtube/remotion run typecheck)",
        "Bash(uv run odczyt stills *)",
    ]


def test_layout_step_allows_only_typecheck():
    assert allowed_tools(build_command(STEPS["layout"], "p")) == [
        "Bash(npm --prefix youtube/remotion run typecheck)"
    ]


@pytest.mark.parametrize("step", ["meta", "review", "stills-review", "metadata"])
def test_structured_steps_cannot_write(step):
    assert STEPS[step].schema is not None
    assert STEPS[step].tools == ["Read"]


def test_every_step_prompt_exists():
    from odczyt.paths import PROMPTS_DIR

    assert all((PROMPTS_DIR / s.prompt).exists() for s in STEPS.values())


def test_costs_accumulate(episode):
    record_cost(episode, "a", {"total_cost_usd": 1.25, "num_turns": 3})
    record_cost(episode, "b", {"total_cost_usd": 0.5})
    assert total_cost(episode) == pytest.approx(1.75)


def test_format_review_md_lists_must_fix_and_counts():
    review = {
        "verdict": "fail",
        "summary": "Dwa problemy.",
        "claims": [
            {
                "segment": "s002",
                "claim": "timeout 150-300 ms",
                "verdict": "supported",
                "location": "p.6 §5.2",
                "quote": "q",
            },
            {
                "segment": "s005",
                "claim": "a|b",
                "verdict": "wrong",
                "location": "p.9",
                "quote": "q",
            },
        ],
        "coverage": [
            {"contribution": "Joint consensus", "covered_in": [], "omission_reason": "za długie"}
        ],
        "skeptic_loop": [{"question_segment": "s003", "answer_segment": "s004", "ok": True}],
        "must_fix": [{"segment": "s005", "problem": "zła liczba", "fix": "popraw"}],
    }
    md = format_review_md(review)
    assert "**Verdict:** fail" in md
    assert "| supported | 1 |" in md and "| wrong | 1 |" in md
    assert "- **s005**: zła liczba → popraw" in md
    assert "a\\|b" in md
    assert "Joint consensus: omitted: za długie" in md
    assert "✅ s003 → s004" in md
