"""Tests for generate_video.py script."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestRunCmd:
    """Tests for run_cmd function."""

    def test_returns_completed_process(self):
        """Should return CompletedProcess from command."""
        from scripts.generate_video import run_cmd

        result = run_cmd(["echo", "hello"])
        assert result.stdout.strip() == "hello"
        assert result.returncode == 0

    def test_check_true_raises_on_error(self):
        """Should raise when command fails and check=True."""
        from scripts.generate_video import run_cmd

        with pytest.raises(subprocess.CalledProcessError):
            run_cmd(["false"])

    def test_check_false_returns_error(self):
        """Should return error result when check=False."""
        from scripts.generate_video import run_cmd

        result = run_cmd(["false"], check=False)
        assert result.returncode != 0


class TestGetDuration:
    """Tests for get_duration function."""

    def test_parses_duration_from_ffprobe(self):
        """Should parse duration from ffprobe output."""
        from scripts.generate_video import get_duration

        mock_result = MagicMock()
        mock_result.stdout = "125.5\n"

        with patch("scripts.generate_video.run_cmd", return_value=mock_result):
            duration = get_duration(Path("/fake/video.mp4"))

        assert duration == 125.5

    def test_calls_ffprobe_with_correct_args(self):
        """Should call ffprobe with proper arguments."""
        from scripts.generate_video import get_duration

        mock_result = MagicMock()
        mock_result.stdout = "100.0"

        with patch("scripts.generate_video.run_cmd", return_value=mock_result) as mock_run:
            get_duration(Path("/test/video.mp4"))

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "ffprobe"
        assert "-show_entries" in args
        assert "format=duration" in args


class TestExtractFrame:
    """Tests for extract_frame function."""

    def test_calls_ffmpeg_with_correct_args(self, tmp_path):
        """Should call ffmpeg to extract single frame."""
        from scripts.generate_video import extract_frame

        video = tmp_path / "test.mp4"
        output = tmp_path / "frame.png"

        with patch("subprocess.run") as mock_run:
            extract_frame(video, output, 5.0)

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "ffmpeg"
        assert "-ss" in args
        assert "5.0" in args
        assert "-vframes" in args
        assert "1" in args


class TestGetBrightness:
    """Tests for get_brightness function."""

    def test_parses_brightness_value(self):
        """Should parse brightness from magick output."""
        from scripts.generate_video import get_brightness

        mock_result = MagicMock()
        mock_result.stdout = "0.75"

        with patch("scripts.generate_video.run_cmd", return_value=mock_result):
            brightness = get_brightness(Path("/fake/image.png"))

        assert brightness == 0.75

    def test_calls_magick_with_correct_args(self):
        """Should call magick with grayscale mean calculation."""
        from scripts.generate_video import get_brightness

        mock_result = MagicMock()
        mock_result.stdout = "0.5"

        with patch("scripts.generate_video.run_cmd", return_value=mock_result) as mock_run:
            get_brightness(Path("/test/image.png"))

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "magick"
        assert "-colorspace" in args
        assert "Gray" in args


class TestCheckBlackFrames:
    """Tests for check_black_frames function."""

    def test_returns_tuple_of_bools(self):
        """Should return (start_ok, end_ok) tuple."""
        from scripts.generate_video import check_black_frames

        with (
            patch("scripts.generate_video.extract_frame"),
            patch("scripts.generate_video.get_brightness", return_value=0.5),
        ):
            result = check_black_frames(Path("/fake/video.mp4"), 100.0)

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert all(isinstance(v, bool) for v in result)

    def test_detects_black_start_frames(self):
        """Should detect black frames at start."""
        from scripts.generate_video import check_black_frames

        with (
            patch("scripts.generate_video.extract_frame"),
            patch("scripts.generate_video.get_brightness", return_value=0.01),
        ):
            start_ok, _end_ok = check_black_frames(Path("/fake/video.mp4"), 100.0)

        assert start_ok is False

    def test_passes_non_black_frames(self):
        """Should pass when frames are not black."""
        from scripts.generate_video import check_black_frames

        with (
            patch("scripts.generate_video.extract_frame"),
            patch("scripts.generate_video.get_brightness", return_value=0.5),
        ):
            start_ok, end_ok = check_black_frames(Path("/fake/video.mp4"), 100.0)

        assert start_ok is True
        assert end_ok is True


class TestFindEpisodeFiles:
    """Tests for find_episode_files function."""

    def test_returns_none_when_not_found(self, tmp_path):
        """Should return None when files not found."""
        from scripts.generate_video import find_episode_files

        with patch("scripts.generate_video.ASSETS_DIR", tmp_path):
            (tmp_path / "slides").mkdir()
            (tmp_path / "audio").mkdir()

            slides, audio = find_episode_files("99")

        assert slides is None
        assert audio is None

    def test_finds_matching_files(self, tmp_path):
        """Should find slides dir and audio file."""
        from scripts.generate_video import find_episode_files

        slides_dir = tmp_path / "slides" / "28-emergent-abilities"
        audio_dir = tmp_path / "audio"
        slides_dir.mkdir(parents=True)
        audio_dir.mkdir()

        audio_file = audio_dir / "28-emergent-abilities.m4a"
        audio_file.write_bytes(b"audio")

        with patch("scripts.generate_video.ASSETS_DIR", tmp_path):
            slides, audio = find_episode_files("28")

        assert slides == slides_dir
        assert audio == audio_file


class TestGenerateVideo:
    """Tests for generate_video function."""

    def test_calls_ffmpeg_with_correct_args(self, tmp_path):
        """Should call ffmpeg with concat and audio inputs."""
        from scripts.generate_video import generate_video

        concat = tmp_path / "concat.txt"
        audio = tmp_path / "audio.m4a"
        output = tmp_path / "output.mp4"
        concat.write_text("file slide.png\nduration 10\n")
        audio.write_bytes(b"audio")

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("scripts.generate_video.run_cmd", return_value=mock_result) as mock_run:
            generate_video(concat, audio, output)

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "ffmpeg"
        assert "-f" in args
        assert "concat" in args
        assert str(concat) in args
        assert str(audio) in args
        assert str(output) in args

    def test_includes_video_filter(self, tmp_path):
        """Should include scale/pad/fps video filter."""
        from scripts.generate_video import generate_video

        concat = tmp_path / "concat.txt"
        audio = tmp_path / "audio.m4a"
        output = tmp_path / "output.mp4"
        concat.write_text("file slide.png\nduration 10\n")
        audio.write_bytes(b"audio")

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("scripts.generate_video.run_cmd", return_value=mock_result) as mock_run:
            generate_video(concat, audio, output)

        args = mock_run.call_args[0][0]
        vf_idx = args.index("-vf")
        vf_value = args[vf_idx + 1]
        assert "scale=1920:1080" in vf_value
        assert "pad=" in vf_value
        assert "fps=30" in vf_value


class TestMain:
    """Tests for main function."""

    def test_shows_usage_when_no_args(self):
        """Should show usage and return error when missing arguments."""
        from scripts.generate_video import main

        with patch("sys.argv", ["generate_video.py"]), pytest.raises(SystemExit):
            main()

    def test_returns_1_when_slides_not_found(self, capsys):
        """Should return 1 when slides directory doesn't exist."""
        from scripts.generate_video import main

        with (
            patch("sys.argv", ["generate_video.py", "99"]),
            patch("scripts.generate_video.find_episode_files", return_value=(None, None)),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "No slides directory found" in captured.out

    def test_returns_1_when_audio_not_found(self, tmp_path, capsys):
        """Should return 1 when audio file doesn't exist."""
        from scripts.generate_video import main

        slides_dir = tmp_path / "28-test"
        slides_dir.mkdir()

        with (
            patch("sys.argv", ["generate_video.py", "28"]),
            patch(
                "scripts.generate_video.find_episode_files", return_value=(slides_dir, None)
            ),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "No audio file found" in captured.out

    def test_returns_1_when_concat_not_found(self, tmp_path, capsys):
        """Should return 1 when concat.txt doesn't exist."""
        from scripts.generate_video import main

        slides_dir = tmp_path / "28-test"
        slides_dir.mkdir()
        audio = tmp_path / "28-test.m4a"
        audio.write_bytes(b"audio")

        with (
            patch("sys.argv", ["generate_video.py", "28"]),
            patch(
                "scripts.generate_video.find_episode_files", return_value=(slides_dir, audio)
            ),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "concat.txt not found" in captured.out

    def test_uses_custom_concat_path(self, tmp_path, capsys):
        """Should use custom concat path when provided."""
        from scripts.generate_video import main

        slides_dir = tmp_path / "28-test"
        slides_dir.mkdir()
        audio = tmp_path / "28-test.m4a"
        audio.write_bytes(b"audio")

        custom_concat = tmp_path / "custom_concat.txt"
        custom_concat.write_text("file slide.png\nduration 10\n")

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "100.0"

        # get_duration called 3 times: audio, video, video (in verification)
        # audio=100, expected video=105 (audio+5), actual video=105
        duration_values = [100.0, 105.0]

        with (
            patch("sys.argv", ["generate_video.py", "28", "--concat", str(custom_concat)]),
            patch(
                "scripts.generate_video.find_episode_files", return_value=(slides_dir, audio)
            ),
            patch("scripts.generate_video.run_cmd", return_value=mock_result),
            patch("scripts.generate_video.get_duration", side_effect=duration_values),
            patch("scripts.generate_video.check_black_frames", return_value=(True, True)),
            patch("scripts.generate_video.OUTPUT_DIR", tmp_path),
        ):
            (tmp_path / "28-test.mp4").write_bytes(b"video")
            result = main()

        assert result == 0

    def test_skip_verify_flag(self, tmp_path, capsys):
        """Should skip verification when --skip-verify is used."""
        from scripts.generate_video import main

        slides_dir = tmp_path / "28-test"
        slides_dir.mkdir()
        concat = slides_dir / "concat.txt"
        concat.write_text("file slide.png\nduration 10\n")
        audio = tmp_path / "28-test.m4a"
        audio.write_bytes(b"audio")

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "100.0"

        with (
            patch("sys.argv", ["generate_video.py", "28", "--skip-verify"]),
            patch(
                "scripts.generate_video.find_episode_files", return_value=(slides_dir, audio)
            ),
            patch("scripts.generate_video.run_cmd", return_value=mock_result),
            patch("scripts.generate_video.get_duration", return_value=100.0),
            patch("scripts.generate_video.OUTPUT_DIR", tmp_path),
        ):
            (tmp_path / "28-test.mp4").write_bytes(b"video")
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Skipping verification" in captured.out

    def test_returns_1_when_ffmpeg_fails(self, tmp_path, capsys):
        """Should return 1 when ffmpeg fails."""
        from scripts.generate_video import main

        slides_dir = tmp_path / "28-test"
        slides_dir.mkdir()
        concat = slides_dir / "concat.txt"
        concat.write_text("file slide.png\nduration 10\n")
        audio = tmp_path / "28-test.m4a"
        audio.write_bytes(b"audio")

        mock_duration = MagicMock()
        mock_duration.stdout = "100.0"

        mock_ffmpeg = MagicMock()
        mock_ffmpeg.returncode = 1
        mock_ffmpeg.stderr = "ffmpeg error"

        def mock_run_cmd(cmd, check=True):
            if cmd[0] == "ffprobe":
                return mock_duration
            return mock_ffmpeg

        with (
            patch("sys.argv", ["generate_video.py", "28"]),
            patch(
                "scripts.generate_video.find_episode_files", return_value=(slides_dir, audio)
            ),
            patch("scripts.generate_video.run_cmd", side_effect=mock_run_cmd),
            patch("scripts.generate_video.OUTPUT_DIR", tmp_path),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "ffmpeg failed" in captured.out

    def test_returns_1_when_verification_fails(self, tmp_path, capsys):
        """Should return 1 when verification fails."""
        from scripts.generate_video import main

        slides_dir = tmp_path / "28-test"
        slides_dir.mkdir()
        concat = slides_dir / "concat.txt"
        concat.write_text("file slide.png\nduration 10\n")
        audio = tmp_path / "28-test.m4a"
        audio.write_bytes(b"audio")

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "100.0"

        with (
            patch("sys.argv", ["generate_video.py", "28"]),
            patch(
                "scripts.generate_video.find_episode_files", return_value=(slides_dir, audio)
            ),
            patch("scripts.generate_video.run_cmd", return_value=mock_result),
            patch("scripts.generate_video.get_duration", side_effect=[100.0, 90.0]),  # Wrong duration
            patch("scripts.generate_video.check_black_frames", return_value=(True, True)),
            patch("scripts.generate_video.OUTPUT_DIR", tmp_path),
        ):
            (tmp_path / "28-test.mp4").write_bytes(b"video")
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "verification failed" in captured.out
