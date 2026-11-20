"""Tests for run_llm_step.py."""

import json

from scripts.run_llm_step import STEPS, build_command, format_review_md, render_prompt


def test_render_prompt_fills_placeholders(tmp_path, monkeypatch):
    monkeypatch.setattr("scripts.run_llm_step.REPO_DIR", tmp_path)
    episode_dir = tmp_path / "youtube/pl/episodes/73-raft"
    episode = {"number": 73, "slug": "73-raft", "target_minutes": 12}
    out = render_prompt(
        "{episode_dir} {slug} {target_minutes} {target_chars} {episode} {part} {scope} {unknown}",
        episode_dir,
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


def test_scenes_step_allows_only_typecheck_and_stills():
    cmd = build_command(STEPS["scenes"], "p")
    allowed = cmd[cmd.index("--allowedTools") + 1 :]
    allowed = allowed[
        : next((i for i, a in enumerate(allowed) if a.startswith("--")), len(allowed))
    ]
    assert allowed == [
        "Bash(npm --prefix youtube/remotion run typecheck)",
        "Bash(uv run python scripts/render_episode.py stills *)",
    ]


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
