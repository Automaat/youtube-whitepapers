"""Tests for upload_youtube.py script."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

try:
    import googleapiclient.http  # noqa: F401

    HAS_GOOGLE_API = True
except ImportError:
    HAS_GOOGLE_API = False

requires_google_api = pytest.mark.skipif(
    not HAS_GOOGLE_API, reason="google-api-python-client not installed"
)


class TestFindEpisodeFiles:
    """Tests for find_episode_files function."""

    def test_finds_video_metadata_thumbnail(self, tmp_path):
        """Should find video, metadata, and optimized thumbnail."""
        from scripts.upload_youtube import find_episode_files

        output_dir = tmp_path / "output"
        thumbnails_dir = tmp_path / "thumbnails"
        output_dir.mkdir()
        thumbnails_dir.mkdir()

        video = output_dir / "28-emergent.mp4"
        metadata = output_dir / "28-emergent-metadata.txt"
        thumbnail = thumbnails_dir / "28-emergent-optimized.png"

        video.write_bytes(b"video")
        metadata.write_text("TYTUŁ:\nTest")
        thumbnail.write_bytes(b"png")

        with (
            patch("scripts.upload_youtube.OUTPUT_DIR", output_dir),
            patch("scripts.upload_youtube.THUMBNAILS_DIR", thumbnails_dir),
        ):
            v, m, t = find_episode_files("28")

        assert v == video
        assert m == metadata
        assert t == thumbnail

    def test_returns_none_for_missing_files(self, tmp_path):
        """Should return None when files not found."""
        from scripts.upload_youtube import find_episode_files

        output_dir = tmp_path / "output"
        thumbnails_dir = tmp_path / "thumbnails"
        output_dir.mkdir()
        thumbnails_dir.mkdir()

        with (
            patch("scripts.upload_youtube.OUTPUT_DIR", output_dir),
            patch("scripts.upload_youtube.THUMBNAILS_DIR", thumbnails_dir),
        ):
            v, m, t = find_episode_files("99")

        assert v is None
        assert m is None
        assert t is None

    def test_prefers_optimized_thumbnail(self, tmp_path):
        """Should prefer -optimized.png over regular thumbnail."""
        from scripts.upload_youtube import find_episode_files

        output_dir = tmp_path / "output"
        thumbnails_dir = tmp_path / "thumbnails"
        output_dir.mkdir()
        thumbnails_dir.mkdir()

        video = output_dir / "28-test.mp4"
        metadata = output_dir / "28-test-metadata.txt"
        regular_thumb = thumbnails_dir / "28-test.png"
        optimized_thumb = thumbnails_dir / "28-test-optimized.png"

        video.write_bytes(b"video")
        metadata.write_text("TYTUŁ:\nTest")
        regular_thumb.write_bytes(b"regular")
        optimized_thumb.write_bytes(b"optimized")

        with (
            patch("scripts.upload_youtube.OUTPUT_DIR", output_dir),
            patch("scripts.upload_youtube.THUMBNAILS_DIR", thumbnails_dir),
        ):
            _, _, t = find_episode_files("28")

        assert t == optimized_thumb

    def test_falls_back_to_regular_thumbnail(self, tmp_path):
        """Should fall back to regular thumbnail if no optimized."""
        from scripts.upload_youtube import find_episode_files

        output_dir = tmp_path / "output"
        thumbnails_dir = tmp_path / "thumbnails"
        output_dir.mkdir()
        thumbnails_dir.mkdir()

        video = output_dir / "28-test.mp4"
        metadata = output_dir / "28-test-metadata.txt"
        regular_thumb = thumbnails_dir / "28-test.png"

        video.write_bytes(b"video")
        metadata.write_text("TYTUŁ:\nTest")
        regular_thumb.write_bytes(b"regular")

        with (
            patch("scripts.upload_youtube.OUTPUT_DIR", output_dir),
            patch("scripts.upload_youtube.THUMBNAILS_DIR", thumbnails_dir),
        ):
            _, _, t = find_episode_files("28")

        assert t == regular_thumb


class TestParseMetadata:
    """Tests for parse_metadata function."""

    def test_extracts_title_from_tytul_section(self, tmp_path):
        """Should extract title from TYTUŁ section."""
        from scripts.upload_youtube import parse_metadata

        metadata_file = tmp_path / "test-metadata.txt"
        metadata_file.write_text("TYTUŁ:\nTest Title | Deep Dive\n\nOPIS:\nDescription")

        result = parse_metadata(metadata_file)

        assert result["title"] == "Test Title | Deep Dive"

    def test_extracts_multiline_description(self, tmp_path):
        """Should extract multiline description from OPIS section."""
        from scripts.upload_youtube import parse_metadata

        metadata_file = tmp_path / "test-metadata.txt"
        metadata_file.write_text("TYTUŁ:\nTitle\n\nOPIS:\nLine 1\nLine 2\n• Bullet\n\nTAGI:\n#test")

        result = parse_metadata(metadata_file)

        assert "Line 1" in result["description"]
        assert "Line 2" in result["description"]
        assert "• Bullet" in result["description"]

    def test_extracts_tags_strips_hashtags(self, tmp_path):
        """Should extract tags and strip # prefix."""
        from scripts.upload_youtube import parse_metadata

        metadata_file = tmp_path / "test-metadata.txt"
        metadata_file.write_text("TYTUŁ:\nTitle\n\nOPIS:\nDesc\n\nTAGI:\n#AI #ML #Test")

        result = parse_metadata(metadata_file)

        assert "AI" in result["tags"]
        assert "ML" in result["tags"]
        assert "Test" in result["tags"]
        assert "#AI" not in result["tags"]

    def test_handles_missing_sections(self, tmp_path):
        """Should return empty values for missing sections."""
        from scripts.upload_youtube import parse_metadata

        metadata_file = tmp_path / "test-metadata.txt"
        metadata_file.write_text("TYTUŁ:\nTitle Only")

        result = parse_metadata(metadata_file)

        assert result["title"] == "Title Only"
        assert result["description"] == ""
        assert result["tags"] == []


class TestDetectCategory:
    """Tests for detect_category function."""

    def test_detects_llm_from_whitepaper_location(self, tmp_path):
        """Should detect llm category from whitepaper location."""
        from scripts.upload_youtube import detect_category

        llm_dir = tmp_path / "whitepapers" / "llm"
        llm_dir.mkdir(parents=True)
        (llm_dir / "28-emergent-abilities.pdf").write_bytes(b"pdf")

        with patch("scripts.upload_youtube.WHITEPAPERS_DIR", tmp_path / "whitepapers"):
            category = detect_category("28-emergent-abilities")

        assert category == "llm"

    def test_detects_distributed_computing(self, tmp_path):
        """Should detect distributed-computing category."""
        from scripts.upload_youtube import detect_category

        dc_dir = tmp_path / "whitepapers" / "distributed-computing"
        dc_dir.mkdir(parents=True)
        (dc_dir / "64-raft.pdf").write_bytes(b"pdf")

        with patch("scripts.upload_youtube.WHITEPAPERS_DIR", tmp_path / "whitepapers"):
            category = detect_category("64-raft")

        assert category == "distributed-computing"

    def test_returns_none_when_not_found(self, tmp_path):
        """Should return None when no matching whitepaper found."""
        from scripts.upload_youtube import detect_category

        wp_dir = tmp_path / "whitepapers"
        (wp_dir / "llm").mkdir(parents=True)

        with patch("scripts.upload_youtube.WHITEPAPERS_DIR", wp_dir):
            category = detect_category("99-unknown")

        assert category is None


class TestGetPlaylistId:
    """Tests for get_playlist_id function."""

    def test_returns_env_var_value(self):
        """Should return playlist ID from env var."""
        from scripts.upload_youtube import get_playlist_id

        mock_settings = MagicMock()
        mock_settings.playlist_llm = "PLenv123"
        mock_settings.playlist_distributed_computing = None
        mock_settings.playlist_security = None

        with patch("scripts.upload_youtube.settings", mock_settings):
            result = get_playlist_id("llm")

        assert result == "PLenv123"

    def test_falls_back_to_config_file(self, tmp_path):
        """Should fall back to config.json when env var not set."""
        from scripts.upload_youtube import get_playlist_id

        config_file = tmp_path / "config.json"
        config_file.write_text('{"playlists": {"llm": "PLconfig456"}}')

        mock_settings = MagicMock()
        mock_settings.playlist_llm = None
        mock_settings.playlist_distributed_computing = None
        mock_settings.playlist_security = None

        with (
            patch("scripts.upload_youtube.settings", mock_settings),
            patch("scripts.upload_youtube.CONFIG_FILE", config_file),
        ):
            result = get_playlist_id("llm")

        assert result == "PLconfig456"

    def test_returns_none_when_not_configured(self, tmp_path):
        """Should return None when playlist not configured."""
        from scripts.upload_youtube import get_playlist_id

        mock_settings = MagicMock()
        mock_settings.playlist_llm = None
        mock_settings.playlist_distributed_computing = None
        mock_settings.playlist_security = None

        config_file = tmp_path / "config.json"

        with (
            patch("scripts.upload_youtube.settings", mock_settings),
            patch("scripts.upload_youtube.CONFIG_FILE", config_file),
        ):
            result = get_playlist_id("llm")

        assert result is None


@requires_google_api
class TestUploadVideo:
    """Tests for upload_video function."""

    def test_uses_resumable_upload(self):
        """Should use resumable upload with MediaFileUpload."""
        from scripts.upload_youtube import upload_video

        mock_youtube = MagicMock()
        mock_request = MagicMock()
        mock_request.next_chunk.return_value = (None, {"id": "video123"})
        mock_youtube.videos().insert.return_value = mock_request

        mock_settings = MagicMock()
        mock_settings.chunk_size_mb = 10

        with (
            patch("scripts.upload_youtube.settings", mock_settings),
            patch("googleapiclient.http.MediaFileUpload") as mock_media,
        ):
            mock_media.return_value = MagicMock()
            result = upload_video(
                mock_youtube, Path("/fake/video.mp4"), "Title", "Desc", ["tag"], "private"
            )

        mock_media.assert_called_once()
        call_kwargs = mock_media.call_args[1]
        assert call_kwargs["resumable"] is True
        assert call_kwargs["chunksize"] == 10 * 1024 * 1024
        assert result == "video123"

    def test_sets_privacy_status(self):
        """Should set correct privacy status."""
        from scripts.upload_youtube import upload_video

        mock_youtube = MagicMock()
        mock_request = MagicMock()
        mock_request.next_chunk.return_value = (None, {"id": "video123"})
        mock_youtube.videos().insert.return_value = mock_request

        mock_settings = MagicMock()
        mock_settings.chunk_size_mb = 10

        with (
            patch("scripts.upload_youtube.settings", mock_settings),
            patch("googleapiclient.http.MediaFileUpload"),
        ):
            upload_video(
                mock_youtube, Path("/fake/video.mp4"), "Title", "Desc", ["tag"], "unlisted"
            )

        call_kwargs = mock_youtube.videos().insert.call_args[1]
        assert call_kwargs["body"]["status"]["privacyStatus"] == "unlisted"

    def test_sets_polish_language_metadata(self):
        """Should set Polish as default language."""
        from scripts.upload_youtube import upload_video

        mock_youtube = MagicMock()
        mock_request = MagicMock()
        mock_request.next_chunk.return_value = (None, {"id": "video123"})
        mock_youtube.videos().insert.return_value = mock_request

        mock_settings = MagicMock()
        mock_settings.chunk_size_mb = 10

        with (
            patch("scripts.upload_youtube.settings", mock_settings),
            patch("googleapiclient.http.MediaFileUpload"),
        ):
            upload_video(mock_youtube, Path("/fake/video.mp4"), "Title", "Desc", ["tag"], "private")

        call_kwargs = mock_youtube.videos().insert.call_args[1]
        assert call_kwargs["body"]["snippet"]["defaultLanguage"] == "pl"
        assert call_kwargs["body"]["snippet"]["defaultAudioLanguage"] == "pl"


@requires_google_api
class TestUploadThumbnail:
    """Tests for upload_thumbnail function."""

    def test_calls_thumbnails_set(self):
        """Should call thumbnails().set() with video ID."""
        from scripts.upload_youtube import upload_thumbnail

        mock_youtube = MagicMock()

        with patch("googleapiclient.http.MediaFileUpload"):
            upload_thumbnail(mock_youtube, "video123", Path("/fake/thumb.png"))

        mock_youtube.thumbnails().set.assert_called_once()
        call_kwargs = mock_youtube.thumbnails().set.call_args[1]
        assert call_kwargs["videoId"] == "video123"


class TestAddToPlaylist:
    """Tests for add_to_playlist function."""

    def test_inserts_to_playlist(self):
        """Should insert video to playlist."""
        from scripts.upload_youtube import add_to_playlist

        mock_youtube = MagicMock()

        add_to_playlist(mock_youtube, "video123", "playlist456")

        mock_youtube.playlistItems().insert.assert_called_once()
        call_kwargs = mock_youtube.playlistItems().insert.call_args[1]
        assert call_kwargs["body"]["snippet"]["playlistId"] == "playlist456"
        assert call_kwargs["body"]["snippet"]["resourceId"]["videoId"] == "video123"


class TestMain:
    """Tests for main function."""

    def test_dry_run_validates_without_upload(self, tmp_path, capsys):
        """Should validate and exit without uploading in dry-run mode."""
        from scripts.upload_youtube import main

        output_dir = tmp_path / "output"
        thumbnails_dir = tmp_path / "thumbnails"
        output_dir.mkdir()
        thumbnails_dir.mkdir()

        video = output_dir / "28-test.mp4"
        metadata = output_dir / "28-test-metadata.txt"
        thumbnail = thumbnails_dir / "28-test-optimized.png"

        video.write_bytes(b"video" * 1000)
        metadata.write_text("TYTUŁ:\nTest Title\n\nOPIS:\nDesc\n\nTAGI:\n#test")
        thumbnail.write_bytes(b"png")

        with (
            patch("sys.argv", ["upload_youtube.py", "28", "--dry-run"]),
            patch("scripts.upload_youtube.OUTPUT_DIR", output_dir),
            patch("scripts.upload_youtube.THUMBNAILS_DIR", thumbnails_dir),
            patch("scripts.upload_youtube.detect_category", return_value=None),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Dry run complete" in captured.out

    def test_exits_1_when_video_missing(self, tmp_path, capsys):
        """Should exit 1 when video file not found."""
        from scripts.upload_youtube import main

        output_dir = tmp_path / "output"
        thumbnails_dir = tmp_path / "thumbnails"
        output_dir.mkdir()
        thumbnails_dir.mkdir()

        with (
            patch("sys.argv", ["upload_youtube.py", "99"]),
            patch("scripts.upload_youtube.OUTPUT_DIR", output_dir),
            patch("scripts.upload_youtube.THUMBNAILS_DIR", thumbnails_dir),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Video not found" in captured.out

    def test_exits_1_when_metadata_missing(self, tmp_path, capsys):
        """Should exit 1 when metadata file not found."""
        from scripts.upload_youtube import main

        output_dir = tmp_path / "output"
        thumbnails_dir = tmp_path / "thumbnails"
        output_dir.mkdir()
        thumbnails_dir.mkdir()

        video = output_dir / "28-test.mp4"
        video.write_bytes(b"video")

        with (
            patch("sys.argv", ["upload_youtube.py", "28"]),
            patch("scripts.upload_youtube.OUTPUT_DIR", output_dir),
            patch("scripts.upload_youtube.THUMBNAILS_DIR", thumbnails_dir),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Metadata not found" in captured.out

    def test_warns_when_playlist_not_configured(self, tmp_path, capsys):
        """Should warn when playlist ID not configured for category."""
        from scripts.upload_youtube import main

        output_dir = tmp_path / "output"
        thumbnails_dir = tmp_path / "thumbnails"
        output_dir.mkdir()
        thumbnails_dir.mkdir()

        video = output_dir / "28-test.mp4"
        metadata = output_dir / "28-test-metadata.txt"
        thumbnail = thumbnails_dir / "28-test-optimized.png"

        video.write_bytes(b"video" * 1000)
        metadata.write_text("TYTUŁ:\nTest Title\n\nOPIS:\nDesc\n\nTAGI:\n#test")
        thumbnail.write_bytes(b"png")

        with (
            patch("sys.argv", ["upload_youtube.py", "28", "--dry-run"]),
            patch("scripts.upload_youtube.OUTPUT_DIR", output_dir),
            patch("scripts.upload_youtube.THUMBNAILS_DIR", thumbnails_dir),
            patch("scripts.upload_youtube.detect_category", return_value="llm"),
            patch("scripts.upload_youtube.get_playlist_id", return_value=None),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "No playlist ID configured" in captured.out

    def test_shows_usage_when_no_args(self):
        """Should show usage when no arguments provided."""
        from scripts.upload_youtube import main

        with patch("sys.argv", ["upload_youtube.py"]), pytest.raises(SystemExit):
            main()
