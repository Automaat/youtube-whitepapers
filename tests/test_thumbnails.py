"""Tests for odczyt.thumbnails."""

import json
import subprocess

from odczyt.thumbnails import from_git, youtube_url


def git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def test_from_git_restores_last_committed_version(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "config", "user.name", "t")
    git(tmp_path, "config", "commit.gpgsign", "false")
    image = tmp_path / "youtube" / "thumbnails" / "64-x.png"
    image.parent.mkdir(parents=True)
    for content in (b"wrong", b"fixed"):
        image.write_bytes(content)
        git(tmp_path, "add", ".")
        git(tmp_path, "commit", "-q", "-m", "c")
    git(tmp_path, "rm", "-q", str(image))
    git(tmp_path, "commit", "-q", "-m", "archive")
    assert from_git(tmp_path, image)
    assert image.read_bytes() == b"fixed"
    assert not from_git(tmp_path, tmp_path / "youtube" / "thumbnails" / "65-y.png")


def test_youtube_url_from_status(tmp_path):
    status = tmp_path / "status.json"
    status.write_text(json.dumps({"papers": [{"episode": "68", "youtube_url": "https://y/1"}]}))
    assert youtube_url(status, 68) == "https://y/1"
    assert youtube_url(status, 69) is None
    assert youtube_url(tmp_path / "none.json", 68) is None
