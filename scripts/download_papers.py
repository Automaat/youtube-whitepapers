#!/usr/bin/env python3
"""Download whitepapers from input file with automatic indexing and verification."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

from status_utils import load_status, save_status, update_summary

SCRIPT_DIR = Path(__file__).parent.parent
WHITEPAPERS_DIR = SCRIPT_DIR / "whitepapers"


def parse_arxiv_url(url: str) -> str | None:
    """Extract arxiv ID from various URL formats."""
    patterns = [
        r"arxiv\.org/abs/(\d+\.\d+)",
        r"arxiv\.org/pdf/(\d+\.\d+)",
        r"ar5iv\.org/abs/(\d+\.\d+)",
    ]
    for pattern in patterns:
        if match := re.search(pattern, url):
            return match.group(1)
    return None


def parse_openreview_url(url: str) -> str | None:
    """Extract OpenReview ID from URL."""
    if match := re.search(r"openreview\.net/forum\?id=([A-Za-z0-9_-]+)", url):
        return match.group(1)
    return None


def download_from_arxiv(arxiv_id: str, output_path: Path) -> bool:
    """Download paper from arxiv using arxiv ID."""
    urls = [
        f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        f"https://export.arxiv.org/pdf/{arxiv_id}.pdf",
    ]

    for url in urls:
        try:
            result = subprocess.run(
                ["curl", "-L", "-f", "-o", str(output_path), url],
                capture_output=True,
                timeout=60,
                check=False,
            )
            if result.returncode == 0 and verify_pdf(output_path):
                return True
            output_path.unlink(missing_ok=True)
        except (subprocess.TimeoutExpired, Exception):
            output_path.unlink(missing_ok=True)
            continue

    return False


def download_from_openreview(paper_id: str, output_path: Path) -> bool:
    """Download paper from OpenReview using paper ID."""
    url = f"https://openreview.net/pdf?id={paper_id}"

    try:
        result = subprocess.run(
            ["curl", "-L", "-f", "-o", str(output_path), url],
            capture_output=True,
            timeout=60,
            check=False,
        )
        if result.returncode == 0 and verify_pdf(output_path):
            return True
        output_path.unlink(missing_ok=True)
    except (subprocess.TimeoutExpired, Exception):
        output_path.unlink(missing_ok=True)

    return False


def download_direct(url: str, output_path: Path) -> bool:
    """Download paper directly from URL."""
    try:
        result = subprocess.run(
            ["curl", "-L", "-f", "-o", str(output_path), url],
            capture_output=True,
            timeout=60,
            check=False,
        )
        if result.returncode == 0 and verify_pdf(output_path):
            return True
        output_path.unlink(missing_ok=True)
    except (subprocess.TimeoutExpired, Exception):
        output_path.unlink(missing_ok=True)

    return False


def verify_pdf(path: Path) -> bool:
    """Verify file is a valid PDF."""
    if not path.exists() or path.stat().st_size < 1000:
        return False

    # Check magic number
    try:
        with path.open("rb") as f:
            header = f.read(4)
            if header != b"%PDF":
                return False
    except Exception:
        return False

    # If PyPDF2 available, do deeper validation
    if PyPDF2:
        try:
            with path.open("rb") as f:
                reader = PyPDF2.PdfReader(f)
                _ = len(reader.pages)
            return True
        except Exception:
            return False

    return True


def find_available_episodes(status: dict[str, Any], count: int) -> list[str]:
    """Find next available episode numbers, including gaps."""
    papers = status.get("papers", [])
    used = {p["episode"] for p in papers if "episode" in p}

    available = []
    current = 1
    while len(available) < count:
        ep_str = str(current).zfill(2)
        if ep_str not in used:
            available.append(ep_str)
        current += 1
        if current > 999:
            break

    return available


def check_duplicate(status: dict[str, Any], name: str, url: str) -> str | None:
    """Check if paper already exists by name or URL. Returns episode if found."""
    papers = status.get("papers", [])

    # Check by name
    for paper in papers:
        if paper.get("name") == name:
            return paper.get("episode")

    # Check by URL (if source_url field exists)
    for paper in papers:
        if "source_url" in paper and paper["source_url"] == url:
            return paper.get("episode")

    return None


def parse_markdown_papers(content: str) -> list[dict[str, str]]:
    """Parse markdown format with paper entries.

    Expected format:
    ### Paper Title (Year)
    - **PDF:** [domain](URL)
    - **Name:** paper-slug-name
    - **Category:** category-name
    """
    papers = []
    lines = content.splitlines()
    current_paper = {}

    for line in lines:
        line = line.strip()

        # New paper section (h3)
        if line.startswith("### "):
            if current_paper.get("url"):
                papers.append(current_paper)
            current_paper = {}
            # Extract title from header
            title = line[4:].strip()
            current_paper["title"] = title

        # PDF URL
        elif "**PDF:**" in line or "**URL:**" in line:
            if match := re.search(r"\]\((https?://[^\)]+)\)", line):
                current_paper["url"] = match.group(1)

        # Name (slug)
        elif "**Name:**" in line:
            name = line.split("**Name:**", 1)[1].strip()
            current_paper["name"] = name

        # Category
        elif "**Category:**" in line:
            category = line.split("**Category:**", 1)[1].strip()
            current_paper["category"] = category

    # Add last paper
    if current_paper.get("url"):
        papers.append(current_paper)

    return papers


def parse_input_file(input_path: Path) -> list[dict[str, str]]:
    """Parse input file containing paper metadata.

    Supports JSON format:
    [
        {
            "name": "paper-name",
            "category": "llm",
            "url": "https://arxiv.org/abs/...",
            "title": "Paper Title (optional)"
        }
    ]

    Or markdown format:
    ### Paper Title (Year)
    - **PDF:** [domain](URL)
    - **Name:** paper-slug-name
    - **Category:** category-name

    Or simple text format (one URL per line):
    https://arxiv.org/abs/1234.5678
    https://openreview.net/forum?id=...
    """
    content = input_path.read_text(encoding="utf-8").strip()

    # Try JSON first
    try:
        data = json.loads(content)
        if isinstance(data, list):
            return data
        return [data] if isinstance(data, dict) else []
    except json.JSONDecodeError:
        pass

    # Try markdown format
    if "###" in content and ("**PDF:**" in content or "**URL:**" in content):
        return parse_markdown_papers(content)

    # Fallback: simple text with URLs
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    papers = []
    for url in lines:
        if not url.startswith("http"):
            continue

        # Try to generate name from URL
        if arxiv_id := parse_arxiv_url(url):
            name = f"arxiv-{arxiv_id.replace('.', '-')}"
        elif paper_id := parse_openreview_url(url):
            name = f"openreview-{paper_id}"
        else:
            name = f"paper-{len(papers) + 1}"

        papers.append({"name": name, "category": "llm", "url": url})

    return papers


def download_paper(paper: dict[str, str], episode: str, category: str) -> tuple[bool, str]:
    """Download paper and return (success, message)."""
    url = paper["url"]
    name = paper["name"]

    # Ensure category directory exists
    category_dir = WHITEPAPERS_DIR / category
    category_dir.mkdir(parents=True, exist_ok=True)

    output_path = category_dir / f"{episode}-{name}.pdf"

    # Try arxiv
    if (arxiv_id := parse_arxiv_url(url)) and download_from_arxiv(arxiv_id, output_path):
        return True, f"Downloaded from arxiv ({arxiv_id})"

    # Try openreview
    if (paper_id := parse_openreview_url(url)) and download_from_openreview(paper_id, output_path):
        return True, f"Downloaded from openreview ({paper_id})"

    # Try direct download
    if download_direct(url, output_path):
        return True, "Downloaded from direct URL"

    return False, "All download methods failed"


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Download papers with automatic indexing and verification"
    )
    parser.add_argument("input_file", type=Path, help="Input file with paper metadata")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without downloading"
    )
    args = parser.parse_args()

    if not args.input_file.exists():
        print(f"❌ Input file not found: {args.input_file}")
        return

    # Load status and input
    status = load_status()
    papers_to_download = parse_input_file(args.input_file)

    if not papers_to_download:
        print("❌ No papers found in input file")
        return

    print(f"📋 Found {len(papers_to_download)} papers in input file\n")

    # Check for duplicates
    duplicates = []
    new_papers = []
    for paper in papers_to_download:
        if dup_ep := check_duplicate(status, paper["name"], paper["url"]):
            duplicates.append((paper["name"], dup_ep))
        else:
            new_papers.append(paper)

    if duplicates:
        print("⚠️  Duplicates found (skipping):")
        for name, ep in duplicates:
            print(f"   • {name} → episode {ep}")
        print()

    if not new_papers:
        print("✅ No new papers to download")
        return

    # Find available episode numbers
    episodes = find_available_episodes(status, len(new_papers))
    if len(episodes) < len(new_papers):
        print(
            f"❌ Not enough available episode numbers (found {len(episodes)}, need {len(new_papers)})"
        )
        return

    # Show plan
    print(f"📥 Planning to download {len(new_papers)} papers:\n")
    for i, paper in enumerate(new_papers):
        ep = episodes[i]
        category = paper.get("category", "llm")
        name = paper["name"]
        print(f"   {ep}. {name} ({category})")
        print(f"       URL: {paper['url']}")

    print()

    if args.dry_run:
        print("🔍 Dry run mode - not downloading")
        return

    # Download papers
    print("🚀 Starting downloads...\n")
    success_count = 0
    failed = []

    for i, paper in enumerate(new_papers):
        ep = episodes[i]
        category = paper.get("category", "llm")
        name = paper["name"]

        print(f"📄 [{i + 1}/{len(new_papers)}] Episode {ep}: {name}")

        success, message = download_paper(paper, ep, category)

        if success:
            print(f"   ✅ {message}")

            # Update status.json
            papers_list = status.get("papers", [])
            new_entry = {
                "episode": ep,
                "name": name,
                "category": category,
                "source_url": paper["url"],
            }
            if "title" in paper:
                new_entry["title"] = paper["title"]

            papers_list.append(new_entry)
            papers_list.sort(key=lambda p: int(p.get("episode", "0")))
            status["papers"] = papers_list

            success_count += 1
        else:
            print(f"   ❌ {message}")
            failed.append(paper)

        print()

    # Save status
    if success_count > 0:
        update_summary(status)
        save_status(status)
        print(f"✅ Updated status.json with {success_count} new papers\n")

    # Summary
    print(f"🎉 Download complete: {success_count}/{len(new_papers)} successful\n")

    if failed:
        print("❌ Failed downloads - manual intervention required:\n")
        for paper in failed:
            print(f"   • {paper['name']}")
            print(f"     URL: {paper['url']}")
            print(f"     Category: {paper.get('category', 'llm')}")
            print()


if __name__ == "__main__":
    main()
