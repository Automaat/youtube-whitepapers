#!/usr/bin/env python3
"""Publish YouTube video (change privacy from private to public).

Setup (one-time):
  Same as upload_youtube.py - OAuth credentials already configured

Usage:
  mise run publish -- 28
  mise run publish -- 28 --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from status_utils import find_paper_by_episode, load_status, update_episode_status
from upload_youtube import get_authenticated_service

if TYPE_CHECKING:
    from googleapiclient.discovery import Resource

SCRIPT_DIR = Path(__file__).parent.parent


def extract_video_id(youtube_url: str) -> str | None:
    """Extract video ID from YouTube URL."""
    match = re.search(r"watch\?v=([a-zA-Z0-9_-]+)", youtube_url)
    return match.group(1) if match else None


def get_video_privacy(youtube: Resource, video_id: str) -> str | None:
    """Get current privacy status of video."""
    try:
        response = youtube.videos().list(part="status", id=video_id).execute()
        items = response.get("items", [])
        if items:
            return items[0]["status"]["privacyStatus"]
    except Exception as e:
        print(f"❌ Failed to get video status: {e}")
    return None


def publish_video(youtube: Resource, video_id: str) -> bool:
    """Change video privacy status to public. Returns True on success."""
    try:
        youtube.videos().update(
            part="status",
            body={"id": video_id, "status": {"privacyStatus": "public"}},
        ).execute()
        return True
    except Exception as e:
        print(f"❌ Failed to publish video: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Publish YouTube video (change privacy to public)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 28
  %(prog)s 28 --dry-run
        """,
    )
    parser.add_argument("episode", help="Episode number (e.g., 28)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check status without making changes",
    )
    args = parser.parse_args()

    ep_num = args.episode.zfill(2)

    print(f"📺 YouTube Publish: Episode {ep_num}")
    print("━" * 50)

    # Load status.json
    status = load_status()
    papers = status.get("papers", [])
    paper = find_paper_by_episode(papers, ep_num)

    if not paper:
        print(f"❌ Episode {ep_num} not found in status.json")
        return 1

    # Check if already published
    if paper.get("published"):
        print(f"✅ Episode {ep_num} already published")
        print("   Skipping...")
        return 0

    # Check if uploaded
    if not paper.get("uploaded"):
        print(f"❌ Episode {ep_num} not uploaded yet")
        return 1

    youtube_url = paper.get("youtube_url")
    if not youtube_url:
        print(f"❌ No youtube_url found for episode {ep_num}")
        return 1

    video_id = extract_video_id(youtube_url)
    if not video_id:
        print(f"❌ Could not extract video ID from URL: {youtube_url}")
        return 1

    print(f"   📹 Video ID: {video_id}")
    print(f"   🔗 URL: {youtube_url}")

    # Get authenticated service
    youtube = get_authenticated_service()

    # Check current privacy status
    current_privacy = get_video_privacy(youtube, video_id)
    if current_privacy:
        print(f"   🔒 Current privacy: {current_privacy}")
    else:
        print("   ⚠️  Could not fetch current privacy status")

    if current_privacy == "public":
        print()
        print("✅ Video already public on YouTube")
        print("   Updating status.json...")
        update_episode_status(ep_num, "published", True)
        return 0

    if args.dry_run:
        print()
        print("━" * 50)
        print("✅ Dry run complete - ready to publish")
        return 0

    print()
    print("🔄 Publishing video...")

    if publish_video(youtube, video_id):
        print("   ✅ Video published (privacy → public)")
        update_episode_status(ep_num, "published", True)
        print()
        print("━" * 50)
        print("✅ Publish complete!")
        print(f"   URL: {youtube_url}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
