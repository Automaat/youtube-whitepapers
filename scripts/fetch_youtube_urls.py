#!/usr/bin/env python3
"""Fetch YouTube video URLs from playlists and update status.json.

Fetches all video URLs from configured playlists and updates status.json
with real YouTube URLs for episodes 66+.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from status_utils import load_status, save_status
from upload_youtube import get_authenticated_service, get_playlist_id

SCRIPT_DIR = Path(__file__).parent.parent
METADATA_DIR = SCRIPT_DIR / "archive" / "pl" / "metadata"


def get_playlist_videos(youtube, playlist_id: str) -> list[dict]:
    """Fetch all videos from a playlist."""
    videos = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        )
        response = request.execute()

        for item in response.get("items", []):
            video_id = item["snippet"]["resourceId"]["videoId"]
            title = item["snippet"]["title"]
            videos.append(
                {
                    "video_id": video_id,
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                }
            )

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos


def load_episode_titles() -> dict[str, str]:
    """Load episode titles from metadata files."""
    titles = {}

    if not METADATA_DIR.exists():
        return titles

    for metadata_file in METADATA_DIR.glob("*-metadata.txt"):
        # Extract episode number from filename
        match = re.match(r"^(\d+)-", metadata_file.stem)
        if not match:
            continue

        ep_num = match.group(1).zfill(2)

        # Parse title from file
        content = metadata_file.read_text(encoding="utf-8")
        title_match = re.search(r"TYTUŁ:\s*\n(.+?)(?:\n\n|\Z)", content, re.DOTALL)
        if title_match:
            title = title_match.group(1).strip()
            titles[ep_num] = title

    return titles


def normalize_title(title: str) -> str:
    """Normalize title for matching."""
    # Remove " | Deep Dive" suffix
    title = title.split("|")[0].strip()
    # Lowercase
    title = title.lower()
    # Remove special characters and diacritics
    import unicodedata

    title = "".join(
        c for c in unicodedata.normalize("NFD", title) if unicodedata.category(c) != "Mn"
    )
    title = re.sub(r"[^a-z0-9\s]", "", title)
    # Remove extra spaces
    title = " ".join(title.split())
    return title


def find_matching_episode(video_title: str, episode_titles: dict[str, str]) -> str | None:
    """Find episode number by matching video title to metadata titles."""
    normalized_video = normalize_title(video_title)

    for ep_num, metadata_title in episode_titles.items():
        ep_int = int(ep_num)
        if ep_int < 66:  # Only episodes 66+
            continue

        normalized_metadata = normalize_title(metadata_title)

        # Exact match after normalization
        if normalized_video == normalized_metadata:
            return ep_num

    return None


def main() -> int:
    print("📺 Fetching YouTube URLs from playlists")
    print("━" * 50)

    # Load current status
    status = load_status()
    papers = status.get("papers", [])

    # Load episode titles from metadata files
    print("   📄 Loading episode titles from metadata...")
    episode_titles = load_episode_titles()
    print(f"      Found {len(episode_titles)} metadata files")

    # Get authenticated service
    youtube = get_authenticated_service()

    # Get videos from all categories
    categories = ["llm", "distributed-computing", "security", "networking", "operating-systems"]
    all_videos = {}

    for category in categories:
        playlist_id = get_playlist_id(category)
        if not playlist_id:
            print(f"   ⚠️  No playlist ID for {category}")
            continue

        print(f"   🔄 Fetching {category} playlist: {playlist_id}")
        videos = get_playlist_videos(youtube, playlist_id)
        print(f"      Found {len(videos)} videos")

        # Map by episode number using title matching
        for video in videos:
            ep_num = find_matching_episode(video["title"], episode_titles)
            if ep_num and ep_num not in all_videos:  # Only add if not already matched
                all_videos[ep_num] = video["url"]
                print(f"      ✅ Matched {ep_num}: {video['title'][:60]}...")

    print()
    print("━" * 50)
    print(f"✅ Fetched {len(all_videos)} video URLs")
    print()

    # Update status.json for episodes 66+
    updated = 0
    for paper in papers:
        ep_num = paper.get("episode")
        if not ep_num:
            continue

        ep_int = int(ep_num)
        if ep_int < 66:
            continue

        # Skip if already has non-placeholder URL
        existing_url = paper.get("youtube_url", "")
        if existing_url and "PLACEHOLDER" not in existing_url:
            print(f"   ⏭️  Episode {ep_num}: already has URL")
            continue

        # Update with real URL
        if ep_num in all_videos:
            paper["youtube_url"] = all_videos[ep_num]
            updated += 1
            print(f"   ✅ Episode {ep_num}: {all_videos[ep_num]}")
        else:
            print(f"   ❌ Episode {ep_num}: not found in playlists")

    if updated > 0:
        save_status(status)
        print()
        print("━" * 50)
        print(f"✅ Updated {updated} YouTube URLs in status.json")
    else:
        print()
        print("━" * 50)
        print("✅ No URLs needed updating")

    return 0


if __name__ == "__main__":
    sys.exit(main())
