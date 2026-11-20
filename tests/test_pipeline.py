"""Tests for odczyt.pipeline: freshness, adoption, gates and stop behavior."""

import pytest

from odczyt import pipeline
from odczyt.episode import digest
from odczyt.pipeline import Runner, Stage, Stop, gate


@pytest.fixture
def stages(episode, monkeypatch):
    """Two stages: create-once `gen` writes a.txt, digest-tracked `build` copies it to b.txt."""
    calls: list[str] = []

    def gen(r: Runner) -> None:
        calls.append("gen")
        r.ep.file("a.txt").write_text("v1")

    def build(r: Runner) -> None:
        calls.append("build")
        r.ep.file("b.txt").write_text(r.ep.file("a.txt").read_text())

    fake = [
        Stage("gen", "", lambda r: r.ep.file("a.txt").exists(), gen),
        Stage(
            "build",
            "",
            lambda r: r.ep.file("b.txt").exists(),
            build,
            lambda r: digest(r.ep.file("a.txt")),
        ),
    ]
    monkeypatch.setattr(pipeline, "STAGES", fake)
    return calls


def test_runs_missing_then_skips_fresh(episode, stages):
    Runner(episode).run()
    Runner(episode).run()
    assert stages == ["gen", "build"]


def test_input_change_reruns_tracked_stage_only(episode, stages):
    Runner(episode).run()
    episode.file("a.txt").write_text("hand edit")
    Runner(episode).run()
    assert stages == ["gen", "build", "build"]
    assert episode.file("b.txt").read_text() == "hand edit"


def test_existing_outputs_are_adopted(episode, stages):
    episode.file("a.txt").write_text("old")
    episode.file("b.txt").write_text("old")
    runner = Runner(episode)
    runner.run()
    assert stages == []
    assert runner.state["stages"]["build"] == digest(episode.file("a.txt"))


def test_outputs_are_not_adopted_after_an_upstream_stage_ran(episode, stages):
    episode.file("b.txt").write_text("stale")
    runner = Runner(episode)
    assert [mark for _, mark in runner.status()] == ["⏳", "⏳"]
    runner.run()
    assert stages == ["gen", "build"]
    assert episode.file("b.txt").read_text() == "v1"


def test_force_and_until(episode, stages):
    Runner(episode).run(until="gen")
    assert stages == ["gen"]
    Runner(episode).run(force={"gen"})
    assert stages == ["gen", "gen", "build"]


def test_gate_stops_until_approved_and_resets_on_change(episode, monkeypatch):
    episode.file("script.yaml").write_text("segments: []\n")
    episode.file("storyboard.yaml").write_text("scenes: []\nthumbnail: {term: X}\n")
    monkeypatch.setattr(pipeline, "STAGES", [gate("script", "read it")])
    runner = Runner(episode)
    with pytest.raises(Stop, match="approve 73 script"):
        runner.run()
    runner.approve("script")
    runner.run()
    episode.file("storyboard.yaml").write_text("scenes: []\nthumbnail: {term: Y}\n")
    Runner(episode).run()
    episode.file("script.yaml").write_text("segments: [1]\n")
    with pytest.raises(Stop):
        Runner(episode).run()


def test_gate_can_be_disabled_in_config(episode, monkeypatch):
    episode.config["pipeline"] = {"gates": ["video"]}
    episode.file("script.yaml").write_text("segments: []\n")
    episode.file("storyboard.yaml").write_text("scenes: []\n")
    monkeypatch.setattr(pipeline, "STAGES", [gate("script", "read it")])
    Runner(episode).run()


def test_stage_names_are_unique():
    names = [s.name for s in pipeline.STAGES]
    assert len(names) == len(set(names))
