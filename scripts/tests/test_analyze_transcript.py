"""Tests for analyze_transcript.py."""

from unittest.mock import patch

from scripts.analyze_transcript import (
    extract_final_question,
    find_technical_terms,
    find_transcript,
    format_timestamp,
    load_transcript,
    suggest_topics,
)


def test_find_transcript(tmp_path):
    """Should find transcript by episode number."""
    transcripts_dir = tmp_path / "youtube/pl/transcripts"
    transcripts_dir.mkdir(parents=True)

    # Create test transcript
    transcript_file = transcripts_dir / "73-raft.json"
    transcript_file.write_text('{"segments": []}')

    with patch("scripts.analyze_transcript.TRANSCRIPTS_DIR", transcripts_dir):
        result = find_transcript("73")
        assert result == transcript_file


def test_find_transcript_not_found(tmp_path):
    """Should return None if transcript not found."""
    transcripts_dir = tmp_path / "youtube/pl/transcripts"
    transcripts_dir.mkdir(parents=True)

    with patch("scripts.analyze_transcript.TRANSCRIPTS_DIR", transcripts_dir):
        result = find_transcript("999")
        assert result is None


def test_load_transcript(tmp_path):
    """Should load transcript JSON."""
    test_file = tmp_path / "test.json"
    test_data = {"segments": [{"start": 0.0, "text": "test"}]}
    test_file.write_text('{"segments": [{"start": 0.0, "text": "test"}]}')

    result = load_transcript(test_file)
    assert result == test_data


def test_extract_final_question():
    """Should extract question from last segments."""
    segments = [
        {"start": 0.0, "text": "This is the beginning."},
        {"start": 10.0, "text": "This is the middle."},
        {"start": 20.0, "text": "Is this the end?"},
    ]

    result = extract_final_question(segments)
    assert result == "Is this the end?"


def test_extract_final_question_no_question():
    """Should return None if no question found."""
    segments = [
        {"start": 0.0, "text": "This is the beginning."},
        {"start": 10.0, "text": "This is the end."},
    ]

    result = extract_final_question(segments)
    assert result is None


def test_extract_final_question_multiple_questions():
    """Should return last question in last 10 segments."""
    segments = [
        {"start": 0.0, "text": "What is this?"},
        {"start": 10.0, "text": "This is the middle."},
        {"start": 20.0, "text": "Is this better?"},
    ]

    result = extract_final_question(segments)
    assert result == "Is this better?"


def test_find_technical_terms():
    """Should identify capitalized technical phrases."""
    text = """
    Paxos algorithm is complex. Paxos is difficult to understand.
    Leader Election is important. Leader Election requires consensus.
    AppendEntries sends data. AppendEntries is critical.
    Raft consensus algorithm uses Strong Leader principle.
    Raft is simpler than Paxos. Strong Leader is key.
    """

    result = find_technical_terms(text)

    # Should find technical terms that appear multiple times
    assert "Paxos" in result
    assert "Raft" in result
    assert any("Leader" in term for term in result)  # Leader, Strong Leader, or Leader Election
    assert "AppendEntries" in result

    # Should filter common words
    assert "The" not in result
    assert "Is" not in result


def test_find_technical_terms_frequency():
    """Should sort by frequency."""
    text = """
    Paxos is complex. Paxos is difficult. Paxos is old.
    Raft is simple. Raft is new.
    Byzantine is tricky. Byzantine is solved.
    """

    result = find_technical_terms(text)

    # Paxos appears 3 times, should be first
    # Raft appears 2 times
    # Byzantine appears 2 times
    assert len(result) > 0
    assert result[0] == "Paxos"
    assert "Raft" in result
    assert "Byzantine" in result


def test_suggest_topics():
    """Should divide transcript into chunks."""
    segments = []
    for i in range(100):
        segments.append({"start": i * 10.0, "end": (i + 1) * 10.0, "text": f"Segment {i}"})

    result = suggest_topics(segments, count=10)

    assert len(result) == 10
    assert result[0]["slide"] == 1
    assert result[0]["start"] == "0:00"
    assert result[9]["slide"] == 10
    assert "Segment" in result[0]["sample"]


def test_suggest_topics_small_transcript():
    """Should handle small transcripts."""
    segments = [
        {"start": 0.0, "end": 10.0, "text": "First"},
        {"start": 10.0, "end": 20.0, "text": "Second"},
    ]

    result = suggest_topics(segments, count=10)

    # Should still create 10 entries even with small input
    assert len(result) == 10


def test_format_timestamp():
    """Should format seconds as MM:SS."""
    assert format_timestamp(0.0) == "0:00"
    assert format_timestamp(59.0) == "0:59"
    assert format_timestamp(60.0) == "1:00"
    assert format_timestamp(125.5) == "2:05"
    assert format_timestamp(3661.0) == "61:01"


def test_format_timestamp_edge_cases():
    """Should handle edge cases."""
    assert format_timestamp(0.1) == "0:00"
    assert format_timestamp(59.9) == "0:59"
    assert format_timestamp(3599.9) == "59:59"


def test_main_missing_argument(capsys):
    """Should show usage when episode number missing."""
    from scripts.analyze_transcript import main

    with patch("sys.argv", ["analyze_transcript.py"]):
        result = main()

    captured = capsys.readouterr()
    assert result == 1
    assert "Usage:" in captured.out


def test_main_transcript_not_found(capsys, tmp_path):
    """Should show error when transcript not found."""
    from scripts.analyze_transcript import main

    transcripts_dir = tmp_path / "youtube/pl/transcripts"
    transcripts_dir.mkdir(parents=True)

    with (
        patch("sys.argv", ["analyze_transcript.py", "999"]),
        patch("scripts.analyze_transcript.TRANSCRIPTS_DIR", transcripts_dir),
    ):
        result = main()

    captured = capsys.readouterr()
    assert result == 1
    assert "❌" in captured.out
    assert "not found" in captured.out


def test_main_success(capsys, tmp_path):
    """Should analyze transcript successfully."""
    from scripts.analyze_transcript import main

    transcripts_dir = tmp_path / "youtube/pl/transcripts"
    transcripts_dir.mkdir(parents=True)

    # Create test transcript
    transcript_file = transcripts_dir / "73-raft.json"
    segments = []
    for i in range(50):
        segments.append(
            {"start": i * 10.0, "end": (i + 1) * 10.0, "text": f"Segment {i} about Paxos and Raft."}
        )
    segments[-1]["text"] = "Final question: Is this the end?"

    transcript_file.write_text(
        '{"segments": ' + str(segments).replace("'", '"').replace("True", "true") + "}"
    )

    with (
        patch("sys.argv", ["analyze_transcript.py", "73"]),
        patch("scripts.analyze_transcript.TRANSCRIPTS_DIR", transcripts_dir),
    ):
        result = main()

    captured = capsys.readouterr()
    assert result == 0
    assert "📊" in captured.out
    assert "73-raft" in captured.out
    assert "❓" in captured.out
    assert "🔧" in captured.out
    assert "📋" in captured.out
    assert "✅" in captured.out


def test_main_empty_segments(capsys, tmp_path):
    """Should handle empty segments."""
    from scripts.analyze_transcript import main

    transcripts_dir = tmp_path / "youtube/pl/transcripts"
    transcripts_dir.mkdir(parents=True)

    # Create transcript with no segments
    transcript_file = transcripts_dir / "73-raft.json"
    transcript_file.write_text('{"segments": []}')

    with (
        patch("sys.argv", ["analyze_transcript.py", "73"]),
        patch("scripts.analyze_transcript.TRANSCRIPTS_DIR", transcripts_dir),
    ):
        result = main()

    captured = capsys.readouterr()
    assert result == 1
    assert "❌" in captured.out
    assert "No segments" in captured.out
