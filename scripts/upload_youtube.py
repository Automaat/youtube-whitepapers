#!/usr/bin/env python3
"""Upload video(s) to YouTube with metadata and thumbnail.

Setup (one-time):
  1. Go to Google Cloud Console: https://console.cloud.google.com
  2. Create project or select existing
  3. Enable YouTube Data API v3
  4. Create OAuth 2.0 credentials (Desktop app)
  5. Download client_secret.json to .youtube-credentials/

Usage:
  mise run upload                   # Upload all ready episodes sequentially
  mise run upload -- 28             # Upload single episode
  mise run upload -- 28 --dry-run
  mise run upload --privacy unlisted
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from status_utils import update_episode_field, update_episode_status
from youtube_config import settings

if TYPE_CHECKING:
    from googleapiclient.discovery import Resource

SCRIPT_DIR = Path(__file__).parent.parent
YOUTUBE_DIR = SCRIPT_DIR / "youtube"
OUTPUT_DIR = YOUTUBE_DIR / "output"
THUMBNAILS_DIR = YOUTUBE_DIR / "thumbnails"
WHITEPAPERS_DIR = SCRIPT_DIR / "whitepapers"
CONFIG_FILE = YOUTUBE_DIR / "config.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]

CATEGORY_DIRS = ["llm", "distributed-computing", "security"]


def get_authenticated_service() -> Resource:
    """Get authenticated YouTube API service with OAuth2."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    token_path = settings.token_path
    client_secret_path = settings.client_secret_path

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not client_secret_path.exists():
                print(f"❌ OAuth client secret not found: {client_secret_path}")
                print("   See script docstring for setup instructions")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_path), SCOPES)
            creds = flow.run_local_server(port=0)

        settings.credentials_dir.mkdir(exist_ok=True)
        token_path.write_text(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def find_episode_files(ep_num: str) -> tuple[Path | None, Path | None, Path | None]:
    """Find video, metadata, and thumbnail for episode."""
    video_matches = list(OUTPUT_DIR.glob(f"{ep_num}-*.mp4"))
    metadata_matches = list(OUTPUT_DIR.glob(f"{ep_num}-*-metadata.txt"))

    # Prefer optimized thumbnails
    thumbnail_matches = list(THUMBNAILS_DIR.glob(f"{ep_num}-*-optimized.png"))
    if not thumbnail_matches:
        thumbnail_matches = list(THUMBNAILS_DIR.glob(f"{ep_num}-*.png"))
        thumbnail_matches = [t for t in thumbnail_matches if "-optimized" not in t.name]

    video = video_matches[0] if video_matches else None
    metadata = metadata_matches[0] if metadata_matches else None
    thumbnail = thumbnail_matches[0] if thumbnail_matches else None

    return video, metadata, thumbnail


def detect_category(ep_name: str) -> str | None:
    """Detect category from whitepaper location."""
    for category in CATEGORY_DIRS:
        category_dir = WHITEPAPERS_DIR / category
        if not category_dir.exists():
            continue

        # Extract paper name part (after episode number)
        parts = ep_name.split("-", 1)
        if len(parts) < 2:
            continue
        paper_name = parts[1]

        matches = list(category_dir.glob(f"*{paper_name}*"))
        if matches:
            return category

    return None


def get_playlist_id(category: str) -> str | None:
    """Get playlist ID for category from config or env vars."""
    env_mapping = {
        "llm": settings.playlist_llm,
        "distributed-computing": settings.playlist_distributed_computing,
        "security": settings.playlist_security,
    }

    if env_mapping.get(category):
        return env_mapping[category]

    if CONFIG_FILE.exists():
        config = json.loads(CONFIG_FILE.read_text())
        return config.get("playlists", {}).get(category)

    return None


def sanitize_youtube_text(text: str) -> str:
    """Remove/replace characters not allowed in YouTube metadata."""
    # YouTube disallows < and > in descriptions
    text = text.replace("<", "").replace(">", "")
    return text


def parse_metadata(metadata_path: Path) -> dict:
    """Parse metadata file into title, description, tags."""
    content = metadata_path.read_text(encoding="utf-8")

    result = {"title": "", "description": "", "tags": []}

    # Parse TYTUŁ:
    title_match = re.search(r"TYTUŁ:\s*\n(.+?)(?:\n\n|\nOPIS:|\Z)", content, re.DOTALL)
    if title_match:
        result["title"] = sanitize_youtube_text(title_match.group(1).strip())

    # Parse OPIS:
    desc_match = re.search(r"OPIS:\s*\n(.+?)(?:\n\nTAGI:|\nTAGI:|\Z)", content, re.DOTALL)
    if desc_match:
        result["description"] = sanitize_youtube_text(desc_match.group(1).strip())

    # Parse TAGI:
    tags_match = re.search(r"TAGI:\s*\n?(.+?)(?:\Z|\n\n)", content, re.DOTALL)
    if tags_match:
        tags_text = tags_match.group(1).strip()
        result["tags"] = [t.strip("#") for t in re.findall(r"#\w+", tags_text)]

    return result


def upload_video(
    youtube: Resource,
    video_path: Path,
    title: str,
    description: str,
    tags: list[str],
    privacy: str = "private",
) -> str:
    """Upload video to YouTube. Returns video ID."""
    from googleapiclient.http import MediaFileUpload

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "28",  # Science & Technology
            "defaultLanguage": "pl",
            "defaultAudioLanguage": "pl",
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    chunk_size = settings.chunk_size_mb * 1024 * 1024
    media = MediaFileUpload(
        str(video_path),
        chunksize=chunk_size,
        resumable=True,
        mimetype="video/mp4",
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    print("🔄 Uploading video...")
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"   {pct}% uploaded")

    return response["id"]


def upload_thumbnail(youtube: Resource, video_id: str, thumbnail_path: Path) -> None:
    """Upload custom thumbnail for video."""
    from googleapiclient.http import MediaFileUpload

    media = MediaFileUpload(str(thumbnail_path), mimetype="image/png")
    youtube.thumbnails().set(videoId=video_id, media_body=media).execute()


def add_to_playlist(youtube: Resource, video_id: str, playlist_id: str) -> None:
    """Add video to playlist."""
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    ).execute()


def get_ready_episodes() -> list[str]:
    """Get list of episodes ready for upload (have video, metadata, thumbnail)."""
    import json

    status_file = WHITEPAPERS_DIR / "status.json"
    if not status_file.exists():
        return []

    data = json.loads(status_file.read_text())

    ready = []
    for paper in data["papers"]:
        if paper.get("uploaded", False):
            continue

        ep_num = paper["episode"]

        video, metadata, thumbnail = find_episode_files(ep_num)
        if video and metadata and thumbnail:
            ready.append(ep_num)

    return sorted(ready, key=lambda x: int(x))


def check_sequential(episodes: list[str]) -> tuple[bool, str | None]:
    """Check if episode list is sequential. Returns (is_sequential, error_msg)."""
    if not episodes:
        return True, None

    nums = [int(ep) for ep in episodes]

    for i in range(len(nums) - 1):
        if nums[i + 1] != nums[i] + 1:
            return False, f"Gap in sequence: {nums[i]:02d} → {nums[i + 1]:02d}"

    return True, None


def upload_single_episode(
    ep_num: str,
    privacy: str,
    skip_thumbnail: bool,
    skip_playlist: bool,
    dry_run: bool,
) -> bool:
    """Upload single episode. Returns True on success."""
    video, metadata, thumbnail = find_episode_files(ep_num)

    print(f"📺 YouTube Upload: Episode {ep_num}")
    print("━" * 50)

    errors = []

    if not video:
        errors.append(f"Video not found: youtube/output/{ep_num}-*.mp4")
    else:
        print(f"   ✅ Video: {video.name} ({video.stat().st_size / 1024**2:.1f}MB)")

    if not metadata:
        errors.append(f"Metadata not found: youtube/output/{ep_num}-*-metadata.txt")
    else:
        print(f"   ✅ Metadata: {metadata.name}")

    if not thumbnail:
        if not skip_thumbnail:
            errors.append(f"Thumbnail not found: youtube/thumbnails/{ep_num}-*-optimized.png")
    else:
        print(f"   ✅ Thumbnail: {thumbnail.name}")

    if errors:
        print()
        for err in errors:
            print(f"❌ {err}")
        return False

    meta = parse_metadata(metadata)

    if not meta["title"]:
        print("❌ Could not parse title from metadata")
        return False

    print()
    title_preview = meta["title"][:60] + "..." if len(meta["title"]) > 60 else meta["title"]
    print(f"   📝 Title: {title_preview}")
    print(f"   🏷️  Tags: {', '.join(meta['tags'][:5])}")

    ep_name = video.stem
    category = detect_category(ep_name)
    playlist_id = get_playlist_id(category) if category else None

    if category:
        print(f"   📂 Category: {category}")
        if playlist_id:
            print(f"   📋 Playlist: {playlist_id}")
        else:
            print("   ⚠️  No playlist ID configured for category")
    else:
        print("   ⚠️  Could not detect category")

    print()
    print(f"   🔒 Privacy: {privacy}")

    if dry_run:
        print()
        print("━" * 50)
        print("✅ Dry run complete - all validations passed")
        return True

    print()
    print("━" * 50)

    youtube = get_authenticated_service()

    video_id = upload_video(
        youtube,
        video,
        meta["title"],
        meta["description"],
        meta["tags"],
        privacy,
    )
    print(f"   ✅ Video uploaded: {video_id}")

    if thumbnail and not skip_thumbnail:
        print("🔄 Uploading thumbnail...")
        upload_thumbnail(youtube, video_id, thumbnail)
        print("   ✅ Thumbnail uploaded")

    if playlist_id and not skip_playlist:
        print(f"🔄 Adding to playlist {category}...")
        add_to_playlist(youtube, video_id, playlist_id)
        print("   ✅ Added to playlist")

    print()
    print("━" * 50)
    print("✅ Upload complete!")
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"   Studio: https://studio.youtube.com/video/{video_id}/edit")
    print(f"   Public: {video_url}")

    update_episode_status(ep_num, "uploaded", True)
    update_episode_field(ep_num, "youtube_url", video_url)

    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Upload video to YouTube with metadata and thumbnail",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Setup (one-time):
  1. Go to Google Cloud Console: https://console.cloud.google.com
  2. Create project or select existing
  3. Enable YouTube Data API v3
  4. Create OAuth 2.0 credentials (Desktop app)
  5. Download client_secret.json to .youtube-credentials/

Examples:
  %(prog)s 28                    # Upload single episode
  %(prog)s                       # Upload all ready episodes sequentially
  %(prog)s 28 --dry-run
  %(prog)s 28 --privacy unlisted
        """,
    )
    parser.add_argument(
        "episode",
        nargs="?",
        help="Episode number (e.g., 28). If omitted, uploads all ready episodes sequentially.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate everything without uploading",
    )
    parser.add_argument(
        "--privacy",
        choices=["private", "unlisted", "public"],
        default=settings.default_privacy,
        help="Video privacy status (default: private)",
    )
    parser.add_argument(
        "--skip-thumbnail",
        action="store_true",
        help="Skip thumbnail upload",
    )
    parser.add_argument(
        "--skip-playlist",
        action="store_true",
        help="Skip adding to playlist",
    )
    args = parser.parse_args()

    # Sequential upload mode
    if not args.episode:
        ready_episodes = get_ready_episodes()

        if not ready_episodes:
            print("❌ No episodes ready for upload")
            print("   Episodes need: video, metadata, and thumbnail")
            return 1

        is_sequential, error_msg = check_sequential(ready_episodes)
        if not is_sequential:
            print(f"❌ {error_msg}")
            print("   Episodes must be uploaded sequentially without gaps")
            return 1

        print(f"📺 Sequential Upload: {len(ready_episodes)} episodes")
        print(f"   Episodes: {ready_episodes[0]} → {ready_episodes[-1]}")
        print("━" * 50)
        print()

        for i, ep_num in enumerate(ready_episodes, 1):
            print(f"[{i}/{len(ready_episodes)}] Episode {ep_num}")
            print()

            success = upload_single_episode(
                ep_num,
                args.privacy,
                args.skip_thumbnail,
                args.skip_playlist,
                args.dry_run,
            )

            if not success:
                print()
                print(f"❌ Upload failed for episode {ep_num}")
                return 1

            if i < len(ready_episodes):
                print()
                print()

        print()
        print("━" * 50)
        print(f"✅ All {len(ready_episodes)} episodes uploaded successfully!")
        return 0

    # Single episode mode
    success = upload_single_episode(
        args.episode,
        args.privacy,
        args.skip_thumbnail,
        args.skip_playlist,
        args.dry_run,
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
