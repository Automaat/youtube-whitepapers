"""Tests for odczyt.scenes."""

from odczyt.episode import dump_yaml
from odczyt.scenes import (
    PLACEHOLDER,
    chunk_stills,
    is_placeholder,
    part_of_scene,
    plan_parts,
    registry_source,
    scaffold,
    still_scene,
)

STORYBOARD = {
    "chapters": [{"id": "c1", "title": "A"}, {"id": "c2", "title": "B"}],
    "scenes": [
        {"id": "intro", "chapter": None},
        {"id": "hook", "chapter": "c1"},
        {"id": "glossary", "chapter": "c1"},
        {"id": "election", "chapter": "c2"},
        {"id": "outro_invite", "chapter": None},
    ],
}


def test_plan_parts_one_per_chapter_with_chapterless_neighbors():
    assert plan_parts(STORYBOARD) == [
        ("part1", ["intro", "hook", "glossary"]),
        ("part2", ["election", "outro_invite"]),
    ]


def test_part_of_scene():
    assert part_of_scene(plan_parts(STORYBOARD))["outro_invite"] == "part2"


def test_still_scene_and_chunks_keep_scenes_whole():
    names = [
        "00-intro-thumbnail",
        "01-intro--end",
        "02-hook--a",
        "02-hook--b",
        "02-hook--end",
        "03-glossary--end",
        "99-outro",
    ]
    assert still_scene("02-hook--a") == "hook"
    assert still_scene("99-outro") == ""
    assert chunk_stills(names, 3) == [
        ["00-intro-thumbnail", "01-intro--end", "02-hook--a", "02-hook--b", "02-hook--end"],
        ["03-glossary--end", "99-outro"],
    ]
    assert chunk_stills(names, 100) == [sorted(names)]


def test_scaffold_creates_placeholders_index_and_registry(episode):
    dump_yaml(episode.file("storyboard.yaml"), STORYBOARD)
    other = episode.scenes_dir.parent / "01-other"
    other.mkdir(parents=True)
    (other / "scenes.tsx").write_text("x")
    scaffold(episode)
    part1 = episode.scenes_dir / "part1.tsx"
    assert part1.read_text() == PLACEHOLDER and is_placeholder(part1)
    part1.write_text("real code")
    scaffold(episode)
    assert not is_placeholder(part1)
    index = (episode.scenes_dir / "scenes.tsx").read_text()
    assert "...part1, ...part2" in index
    registry = (episode.scenes_dir.parent / "registry.ts").read_text()
    assert registry == registry_source(episode.scenes_dir.parent)
    assert '"01-other": ep01_other' in registry and '"73-raft": ep73_raft' in registry
