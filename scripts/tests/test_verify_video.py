"""Tests for verify_video.py script."""

from pathlib import Path
from unittest.mock import MagicMock, patch


class TestRunCmd:
    """Tests for run_cmd function."""

    def test_returns_stdout(self):
        """Should return stripped stdout from command."""
        from scripts.verify_video import run_cmd

        result = run_cmd(["echo", "  hello  "])
        assert result == "hello"

    def test_handles_empty_output(self):
        """Should handle commands with no output."""
        from scripts.verify_video import run_cmd

        result = run_cmd(["true"])
        assert result == ""


class TestGetDuration:
    """Tests for get_duration function."""

    def test_parses_duration_from_ffprobe(self):
        """Should parse duration from ffprobe output."""
        from scripts.verify_video import get_duration

        with patch("scripts.verify_video.run_cmd", return_value="125.5"):
            duration = get_duration(Path("/fake/video.mp4"))

        assert duration == 125.5

    def test_calls_ffprobe_with_correct_args(self):
        """Should call ffprobe with proper arguments."""
        from scripts.verify_video import get_duration

        with patch("scripts.verify_video.run_cmd", return_value="100.0") as mock_run:
            get_duration(Path("/test/video.mp4"))

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "ffprobe"
        assert "-show_entries" in args
        assert "format=duration" in args
        assert "/test/video.mp4" in args

    def test_handles_long_duration(self):
        """Should handle long video durations."""
        from scripts.verify_video import get_duration

        with patch("scripts.verify_video.run_cmd", return_value="7200.123"):
            duration = get_duration(Path("/fake/video.mp4"))

        assert duration == 7200.123


class TestExtractFrames:
    """Tests for extract_frames function."""

    def test_extracts_start_frames(self, tmp_path):
        """Should extract frames from start of video."""
        from scripts.verify_video import extract_frames

        video = tmp_path / "test.mp4"
        video.write_bytes(b"fake video")

        mock_run = MagicMock()

        with (
            patch("scripts.verify_video.get_duration", return_value=100.0),
            patch("subprocess.run", mock_run),
        ):
            frames = extract_frames(video, tmp_path, start=True, count=3)

        assert len(frames) == 3
        assert all("start" in f.name for f in frames)
        assert mock_run.call_count == 3

    def test_extracts_end_frames(self, tmp_path):
        """Should extract frames from end of video."""
        from scripts.verify_video import extract_frames

        video = tmp_path / "test.mp4"
        video.write_bytes(b"fake video")

        mock_run = MagicMock()

        with (
            patch("scripts.verify_video.get_duration", return_value=100.0),
            patch("subprocess.run", mock_run),
        ):
            frames = extract_frames(video, tmp_path, start=False, count=3)

        assert len(frames) == 3
        assert all("end" in f.name for f in frames)

    def test_uses_correct_timestamps_for_start(self, tmp_path):
        """Should use timestamps 0, 1, 2 for start frames."""
        from scripts.verify_video import extract_frames

        video = tmp_path / "test.mp4"
        video.write_bytes(b"fake video")

        mock_run = MagicMock()

        with (
            patch("scripts.verify_video.get_duration", return_value=100.0),
            patch("subprocess.run", mock_run),
        ):
            extract_frames(video, tmp_path, start=True, count=3)

        calls = mock_run.call_args_list
        timestamps = []
        for c in calls:
            args = c[0][0]
            ss_idx = args.index("-ss")
            timestamps.append(args[ss_idx + 1])

        assert timestamps == ["0", "1", "2"]

    def test_uses_correct_timestamps_for_end(self, tmp_path):
        """Should use last 3 seconds for end frames."""
        from scripts.verify_video import extract_frames

        video = tmp_path / "test.mp4"
        video.write_bytes(b"fake video")

        mock_run = MagicMock()

        with (
            patch("scripts.verify_video.get_duration", return_value=100.0),
            patch("subprocess.run", mock_run),
        ):
            extract_frames(video, tmp_path, start=False, count=3)

        calls = mock_run.call_args_list
        timestamps = []
        for c in calls:
            args = c[0][0]
            ss_idx = args.index("-ss")
            timestamps.append(float(args[ss_idx + 1]))

        # For 100s video with count=3: 97, 98, 99
        assert timestamps == [97.0, 98.0, 99.0]


class TestGetBrightness:
    """Tests for get_brightness function."""

    def test_parses_brightness_value(self):
        """Should parse brightness from magick output."""
        from scripts.verify_video import get_brightness

        with patch("scripts.verify_video.run_cmd", return_value="0.75"):
            brightness = get_brightness(Path("/fake/image.png"))

        assert brightness == 0.75

    def test_calls_magick_with_correct_args(self):
        """Should call magick with grayscale mean calculation."""
        from scripts.verify_video import get_brightness

        with patch("scripts.verify_video.run_cmd", return_value="0.5") as mock_run:
            get_brightness(Path("/test/image.png"))

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "magick"
        assert "-colorspace" in args
        assert "Gray" in args
        assert "%[fx:mean]" in " ".join(args)

    def test_detects_black_frame(self):
        """Should detect very dark frames as black."""
        from scripts.verify_video import get_brightness

        with patch("scripts.verify_video.run_cmd", return_value="0.01"):
            brightness = get_brightness(Path("/fake/image.png"))

        assert brightness < 0.05  # Threshold for black


class TestVerifyVideo:
    """Tests for verify_video function."""

    def test_passes_when_duration_correct_and_no_black_frames(self, tmp_path, capsys):
        """Should pass verification when all checks succeed."""
        from scripts.verify_video import verify_video

        video = tmp_path / "test.mp4"
        audio = tmp_path / "test.m4a"
        video.write_bytes(b"video")
        audio.write_bytes(b"audio")

        with (
            patch("scripts.verify_video.get_duration", side_effect=[125.5, 120.5]),  # video, audio
            patch("scripts.verify_video.extract_frames") as mock_extract,
            patch("scripts.verify_video.get_brightness", return_value=0.5),
        ):
            mock_extract.return_value = [tmp_path / "frame.png"]
            (tmp_path / "frame.png").write_bytes(b"png")

            result = verify_video(video, audio)

        assert result is True
        captured = capsys.readouterr()
        assert "Video verification passed" in captured.out

    def test_fails_when_duration_wrong(self, tmp_path, capsys):
        """Should fail when video duration doesn't match expected."""
        from scripts.verify_video import verify_video

        video = tmp_path / "test.mp4"
        audio = tmp_path / "test.m4a"
        video.write_bytes(b"video")
        audio.write_bytes(b"audio")

        with (
            patch(
                "scripts.verify_video.get_duration", side_effect=[100.0, 120.5]
            ),  # Wrong duration
            patch("scripts.verify_video.extract_frames") as mock_extract,
            patch("scripts.verify_video.get_brightness", return_value=0.5),
        ):
            mock_extract.return_value = [tmp_path / "frame.png"]
            (tmp_path / "frame.png").write_bytes(b"png")

            result = verify_video(video, audio)

        assert result is False
        captured = capsys.readouterr()
        assert "Duration mismatch" in captured.out

    def test_fails_when_start_frames_black(self, tmp_path, capsys):
        """Should fail when start frames are black."""
        from scripts.verify_video import verify_video

        video = tmp_path / "test.mp4"
        audio = tmp_path / "test.m4a"
        video.write_bytes(b"video")
        audio.write_bytes(b"audio")

        frame = tmp_path / "frame.png"
        frame.write_bytes(b"png")

        def mock_brightness(path):
            if "start" in str(path):
                return 0.01  # Black
            return 0.5

        with (
            patch("scripts.verify_video.get_duration", side_effect=[125.5, 120.5]),
            patch("scripts.verify_video.extract_frames", return_value=[frame]),
            patch("scripts.verify_video.get_brightness", side_effect=mock_brightness),
        ):
            result = verify_video(video, audio)

        assert result is False
        captured = capsys.readouterr()
        assert "BLACK" in captured.out

    def test_fails_when_end_frames_black(self, tmp_path, capsys):
        """Should fail when end frames are black."""
        from scripts.verify_video import verify_video

        video = tmp_path / "test.mp4"
        audio = tmp_path / "test.m4a"
        video.write_bytes(b"video")
        audio.write_bytes(b"audio")

        start_frame = tmp_path / "start_00.png"
        end_frame = tmp_path / "end_00.png"
        start_frame.write_bytes(b"png")
        end_frame.write_bytes(b"png")

        def mock_extract(_video, _output_dir, start, _count=3):
            if start:
                return [start_frame]
            return [end_frame]

        def mock_brightness(path):
            if "end" in path.name:
                return 0.01  # Black end frame
            return 0.5

        with (
            patch("scripts.verify_video.get_duration", side_effect=[125.5, 120.5]),
            patch("scripts.verify_video.extract_frames", side_effect=mock_extract),
            patch("scripts.verify_video.get_brightness", side_effect=mock_brightness),
        ):
            result = verify_video(video, audio)

        assert result is False
        captured = capsys.readouterr()
        assert "BLACK" in captured.out

    def test_provides_fix_suggestions(self, tmp_path, capsys):
        """Should provide suggestions when verification fails."""
        from scripts.verify_video import verify_video

        video = tmp_path / "test.mp4"
        audio = tmp_path / "test.m4a"
        video.write_bytes(b"video")
        audio.write_bytes(b"audio")

        frame = tmp_path / "frame.png"
        frame.write_bytes(b"png")

        with (
            patch("scripts.verify_video.get_duration", side_effect=[100.0, 120.5]),  # Wrong
            patch("scripts.verify_video.extract_frames", return_value=[frame]),
            patch("scripts.verify_video.get_brightness", return_value=0.01),  # Black
        ):
            verify_video(video, audio)

        captured = capsys.readouterr()
        assert "Fix concat timings" in captured.out
        assert "Check thumbnail" in captured.out

    def test_tolerance_for_duration(self, tmp_path, capsys):
        """Should accept duration within 0.5s tolerance."""
        from scripts.verify_video import verify_video

        video = tmp_path / "test.mp4"
        audio = tmp_path / "test.m4a"
        video.write_bytes(b"video")
        audio.write_bytes(b"audio")

        frame = tmp_path / "frame.png"
        frame.write_bytes(b"png")

        # Expected: 120.5 + 5 = 125.5, actual: 125.8 (within 0.5s)
        with (
            patch("scripts.verify_video.get_duration", side_effect=[125.8, 120.5]),
            patch("scripts.verify_video.extract_frames", return_value=[frame]),
            patch("scripts.verify_video.get_brightness", return_value=0.5),
        ):
            result = verify_video(video, audio)

        assert result is True
        captured = capsys.readouterr()
        assert "Duration OK" in captured.out


class TestMain:
    """Tests for main function."""

    def test_shows_usage_when_no_args(self, capsys):
        """Should show usage and return 1 when missing arguments."""
        from scripts.verify_video import main

        with patch("sys.argv", ["verify_video.py"]):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_shows_usage_when_one_arg(self, capsys):
        """Should show usage when only video provided."""
        from scripts.verify_video import main

        with patch("sys.argv", ["verify_video.py", "video.mp4"]):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_returns_1_when_video_not_found(self, tmp_path, capsys):
        """Should return 1 when video file doesn't exist."""
        from scripts.verify_video import main

        audio = tmp_path / "test.m4a"
        audio.write_bytes(b"audio")

        with patch("sys.argv", ["verify_video.py", "/nonexistent/video.mp4", str(audio)]):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Video not found" in captured.out

    def test_returns_1_when_audio_not_found(self, tmp_path, capsys):
        """Should return 1 when audio file doesn't exist."""
        from scripts.verify_video import main

        video = tmp_path / "test.mp4"
        video.write_bytes(b"video")

        with patch("sys.argv", ["verify_video.py", str(video), "/nonexistent/audio.m4a"]):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Audio not found" in captured.out

    def test_returns_0_when_verification_passes(self, tmp_path):
        """Should return 0 when verification succeeds."""
        from scripts.verify_video import main

        video = tmp_path / "test.mp4"
        audio = tmp_path / "test.m4a"
        video.write_bytes(b"video")
        audio.write_bytes(b"audio")

        with (
            patch("sys.argv", ["verify_video.py", str(video), str(audio)]),
            patch("scripts.verify_video.verify_video", return_value=True),
        ):
            result = main()

        assert result == 0

    def test_returns_1_when_verification_fails(self, tmp_path):
        """Should return 1 when verification fails."""
        from scripts.verify_video import main

        video = tmp_path / "test.mp4"
        audio = tmp_path / "test.m4a"
        video.write_bytes(b"video")
        audio.write_bytes(b"audio")

        with (
            patch("sys.argv", ["verify_video.py", str(video), str(audio)]),
            patch("scripts.verify_video.verify_video", return_value=False),
        ):
            result = main()

        assert result == 1


class TestBrightnessThreshold:
    """Tests for brightness threshold behavior."""

    def test_threshold_at_0_05(self, tmp_path, capsys):
        """Should use 0.05 as black frame threshold."""
        from scripts.verify_video import verify_video

        video = tmp_path / "test.mp4"
        audio = tmp_path / "test.m4a"
        video.write_bytes(b"video")
        audio.write_bytes(b"audio")

        frame = tmp_path / "frame.png"
        frame.write_bytes(b"png")

        # 0.049 should be black, 0.051 should not
        with (
            patch("scripts.verify_video.get_duration", side_effect=[125.5, 120.5]),
            patch("scripts.verify_video.extract_frames", return_value=[frame]),
            patch("scripts.verify_video.get_brightness", return_value=0.049),
        ):
            result = verify_video(video, audio)

        assert result is False  # Should be detected as black
        captured = capsys.readouterr()
        assert "BLACK" in captured.out

    def test_passes_above_threshold(self, tmp_path, capsys):
        """Should pass when brightness above threshold."""
        from scripts.verify_video import verify_video

        video = tmp_path / "test.mp4"
        audio = tmp_path / "test.m4a"
        video.write_bytes(b"video")
        audio.write_bytes(b"audio")

        frame = tmp_path / "frame.png"
        frame.write_bytes(b"png")

        with (
            patch("scripts.verify_video.get_duration", side_effect=[125.5, 120.5]),
            patch("scripts.verify_video.extract_frames", return_value=[frame]),
            patch("scripts.verify_video.get_brightness", return_value=0.051),
        ):
            result = verify_video(video, audio)

        assert result is True
        captured = capsys.readouterr()
        assert "BLACK" not in captured.out
