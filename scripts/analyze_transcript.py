#!/usr/bin/env python3
"""Analyze transcript and extract structured info for slide generation.

Usage:
  mise run analyze-transcript -- 73
  python scripts/analyze_transcript.py 73
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
TRANSCRIPTS_DIR = SCRIPT_DIR / "youtube/pl/transcripts"


def find_transcript(ep_num: str) -> Path | None:
    """Find transcript matching episode number."""
    matches = list(TRANSCRIPTS_DIR.glob(f"{ep_num}-*.json"))
    return matches[0] if matches else None


def load_transcript(path: Path) -> dict:
    """Load transcript JSON."""
    return json.loads(path.read_text())


def extract_final_question(segments: list) -> str | None:
    """Extract question from last segments."""
    # Check last 10 segments for question
    for seg in reversed(segments[-10:]):
        text = seg.get("text", "")
        if "?" in text:
            return text.strip()
    return None


def find_technical_terms(text: str) -> list[str]:
    """Extract capitalized technical terms."""
    # Find sequences like "Paxos", "Leader Election", "AppendEntries", "RPC"
    # Matches both regular capitalized words and CamelCase
    pattern = r"\b[A-Z][a-z]*(?:[A-Z][a-z]*)*(?:\s+[A-Z][a-z]*(?:[A-Z][a-z]*)*)*\b"
    matches = re.findall(pattern, text)

    # Filter common words (English and Polish)
    common = {
        # English
        "The",
        "A",
        "An",
        "In",
        "On",
        "At",
        "To",
        "For",
        "And",
        "Or",
        "But",
        "If",
        "This",
        "That",
        "With",
        "From",
        "By",
        "As",
        "Of",
        "It",
        "Is",
        "Was",
        "Are",
        "Were",
        "Be",
        "Been",
        "Being",
        "Has",
        "Have",
        "Had",
        "Do",
        "Does",
        "Did",
        "Will",
        "Would",
        "Should",
        "Could",
        "Can",
        "May",
        "Might",
        "Must",
        "Shall",
        "So",
        "Then",
        "Now",
        "Just",
        "Very",
        "Too",
        "Only",
        "Also",
        "Even",
        "When",
        "Where",
        "Why",
        "How",
        "What",
        "Which",
        "Who",
        "Whom",
        "Whose",
        # Polish
        "I",
        "W",
        "Z",
        "Na",
        "O",
        "Po",
        "Dla",
        "Przez",
        "Bez",
        "Przed",
        "Za",
        "Od",
        "U",
        "Przy",
        "Nad",
        "Pod",
        "Czyli",
        "Co",
        "Tak",
        "Nie",
        "Jak",
        "Ale",
        "Bo",
        "Czy",
        "Jest",
        "Są",
        "Ten",
        "Ta",
        "Te",
        "Tego",
        "Tej",
        "Tym",
        "Tutaj",
        "Tam",
        "Tu",
        "Teraz",
        "Wtedy",
        "Już",
        "Jeszcze",
        "Właśnie",
        "Więc",
        "Tylko",
        "Bardzo",
        "Kiedy",
        "Gdzie",
        "Dlaczego",
        "Które",
        "Który",
        "Która",
        "Jakie",
        "Jaki",
        "Jaka",
        "Autorzy",
        "Jego",
        "Jej",
        "Ich",
        "Im",
        "Zamiast",
        "Dobrze",
        "Dopiero",
        "Okej",
        "Jasne",
        "Zanim",
        "Potem",
        "Jednak",
        "Zawsze",
        "Nigdy",
        "Może",
        "Można",
        "Musi",
        "Musisz",
        "Możesz",
        "Wszystko",
        "Wszystkie",
        "Każdy",
        "Każda",
        "Każde",
        "Żaden",
        "Nic",
        "Nikt",
        "Nigdzie",
    }

    # Filter: remove single letters, common words, and terms with fewer than 2 chars
    terms = [m for m in matches if len(m) >= 2 and m not in common]

    # Count occurrences and sort by frequency
    term_counts = {}
    for term in terms:
        term_counts[term] = term_counts.get(term, 0) + 1

    # Filter terms that appear less than 2 times
    filtered_counts = {term: count for term, count in term_counts.items() if count >= 2}

    # Return top 20 by frequency
    sorted_terms = sorted(filtered_counts.items(), key=lambda x: x[1], reverse=True)
    return [term for term, _ in sorted_terms[:20]]


def suggest_topics(segments: list, count: int = 10) -> list[dict]:
    """Suggest topic boundaries."""
    total_segments = len(segments)
    chunk_size = total_segments // count

    topics = []
    for i in range(count):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_segments)

        start_time = segments[start_idx]["start"]
        end_time = segments[end_idx - 1]["end"] if end_idx > 0 else start_time

        # Sample text from chunk start
        sample_text = " ".join(seg["text"] for seg in segments[start_idx : start_idx + 3])

        topics.append(
            {
                "slide": i + 1,
                "start": format_timestamp(start_time),
                "end": format_timestamp(end_time),
                "sample": sample_text[:100],
            }
        )

    return topics


def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"


def print_analysis(
    ep_name: str, data: dict, question: str | None, terms: list[str], topics: list[dict]
) -> None:
    """Print formatted analysis."""
    segments = data.get("segments", [])
    duration = segments[-1]["end"] if segments else 0

    print(f"\n📊 Transcript Analysis: {ep_name}")
    print("━" * 70)
    print(f"   Duration: {format_timestamp(duration)}")
    print(f"   Segments: {len(segments)}")
    print()

    if question:
        print("❓ Final Question:")
        print(f"   {question}")
        print()

    if terms:
        print("🔧 Technical Terms (by frequency):")
        for i, term in enumerate(terms[:15], 1):
            print(f"   {i:2d}. {term}")
        print()

    print("📋 Suggested 10-Slide Outline:")
    print()
    print("| Slide | Start    | End      | Sample Text                              |")
    print("|-------|----------|----------|------------------------------------------|")
    for t in topics:
        sample = t["sample"][:40] + "..." if len(t["sample"]) > 40 else t["sample"]
        print(f"| {t['slide']:5d} | {t['start']:8s} | {t['end']:8s} | {sample:40s} |")
    print()


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python analyze_transcript.py <episode_number>")
        print("Example: python analyze_transcript.py 73")
        return 1

    ep_num = sys.argv[1]
    transcript_path = find_transcript(ep_num)

    if not transcript_path:
        print(f"❌ Transcript not found: {TRANSCRIPTS_DIR}/{ep_num}-*.json")
        return 1

    ep_name = transcript_path.stem

    print(f"📖 Reading: {transcript_path.name}")
    data = load_transcript(transcript_path)

    segments = data.get("segments", [])
    if not segments:
        print("❌ No segments found in transcript")
        return 1

    full_text = " ".join(seg["text"] for seg in segments)

    question = extract_final_question(segments)
    terms = find_technical_terms(full_text)
    topics = suggest_topics(segments, count=10)

    print_analysis(ep_name, data, question, terms, topics)
    print("✅ Analysis complete - use this to create NotebookLM prompt")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
