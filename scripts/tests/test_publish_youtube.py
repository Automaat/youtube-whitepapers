"""Tests for publish_youtube.py script."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestExtractVideoId:
    """Tests for extract_video_id function."""

    def test_extracts_video_id_from_standard_url(self):
        """Should extract video ID from standard YouTube URL."""
        from scripts.publish_youtube import extract_video_id

        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = extract_video_id(url)

        assert result == "dQw4w9WgXcQ"

    def test_extracts_video_id_with_query_params(self):
        """Should extract video ID even with additional query params."""
        from scripts.publish_youtube import extract_video_id

        url = "https://www.youtube.com/watch?v=abc123XYZ&t=123"
        result = extract_video_id(url)

        assert result == "abc123XYZ"

    def test_returns_none_for_invalid_url(self):
        """Should return None for invalid URL format."""
        from scripts.publish_youtube import extract_video_id

        url = "https://youtube.com/invalid"
        result = extract_video_id(url)

        assert result is None


class TestGetVideoPrivacy:
    """Tests for get_video_privacy function."""

    def test_returns_privacy_status(self):
        """Should return current privacy status from API."""
        from scripts.publish_youtube import get_video_privacy

        mock_youtube = MagicMock()
        mock_youtube.videos().list().execute.return_value = {
            "items": [{"status": {"privacyStatus": "private"}}]
        }

        result = get_video_privacy(mock_youtube, "video123")

        assert result == "private"

    def test_returns_none_when_video_not_found(self):
        """Should return None when video not found."""
        from scripts.publish_youtube import get_video_privacy

        mock_youtube = MagicMock()
        mock_youtube.videos().list().execute.return_value = {"items": []}

        result = get_video_privacy(mock_youtube, "invalid123")

        assert result is None

    def test_returns_none_on_api_error(self, capsys):
        """Should return None and print error on API failure."""
        from scripts.publish_youtube import get_video_privacy

        mock_youtube = MagicMock()
        mock_youtube.videos().list().execute.side_effect = Exception("API Error")

        result = get_video_privacy(mock_youtube, "video123")

        assert result is None
        captured = capsys.readouterr()
        assert "Failed to get video status" in captured.out


class TestPublishVideo:
    """Tests for publish_video function."""

    def test_updates_privacy_to_public(self):
        """Should call videos().update() with public privacy."""
        from scripts.publish_youtube import publish_video

        mock_youtube = MagicMock()
        mock_update = MagicMock()
        mock_update.execute.return_value = {"id": "video123"}
        mock_youtube.videos().update.return_value = mock_update

        result = publish_video(mock_youtube, "video123")

        assert result is True
        mock_youtube.videos().update.assert_called_once_with(
            part="status",
            body={"id": "video123", "status": {"privacyStatus": "public"}},
        )

    def test_returns_false_on_api_error(self, capsys):
        """Should return False and print error on API failure."""
        from scripts.publish_youtube import publish_video

        mock_youtube = MagicMock()
        mock_youtube.videos().update().execute.side_effect = Exception("API Error")

        result = publish_video(mock_youtube, "video123")

        assert result is False
        captured = capsys.readouterr()
        assert "Failed to publish video" in captured.out


class TestMain:
    """Tests for main function."""

    def test_exits_0_when_already_published(self, capsys):
        """Should exit 0 and skip when already published."""
        from scripts.publish_youtube import main

        mock_status = {
            "papers": [
                {
                    "episode": "28",
                    "uploaded": True,
                    "published": True,
                    "youtube_url": "https://www.youtube.com/watch?v=test123",
                }
            ]
        }

        with (
            patch("sys.argv", ["publish_youtube.py", "28"]),
            patch("scripts.publish_youtube.load_status", return_value=mock_status),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "already published" in captured.out
        assert "Skipping" in captured.out

    def test_exits_1_when_episode_not_found(self, capsys):
        """Should exit 1 when episode not in status.json."""
        from scripts.publish_youtube import main

        mock_status = {"papers": []}

        with (
            patch("sys.argv", ["publish_youtube.py", "99"]),
            patch("scripts.publish_youtube.load_status", return_value=mock_status),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "not found in status.json" in captured.out

    def test_exits_1_when_not_uploaded(self, capsys):
        """Should exit 1 when video not uploaded yet."""
        from scripts.publish_youtube import main

        mock_status = {
            "papers": [
                {
                    "episode": "28",
                    "uploaded": False,
                }
            ]
        }

        with (
            patch("sys.argv", ["publish_youtube.py", "28"]),
            patch("scripts.publish_youtube.load_status", return_value=mock_status),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "not uploaded yet" in captured.out

    def test_exits_1_when_no_youtube_url(self, capsys):
        """Should exit 1 when youtube_url missing."""
        from scripts.publish_youtube import main

        mock_status = {
            "papers": [
                {
                    "episode": "28",
                    "uploaded": True,
                }
            ]
        }

        with (
            patch("sys.argv", ["publish_youtube.py", "28"]),
            patch("scripts.publish_youtube.load_status", return_value=mock_status),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "No youtube_url found" in captured.out

    def test_exits_1_when_invalid_youtube_url(self, capsys):
        """Should exit 1 when cannot extract video ID."""
        from scripts.publish_youtube import main

        mock_status = {
            "papers": [
                {
                    "episode": "28",
                    "uploaded": True,
                    "youtube_url": "https://invalid.url",
                }
            ]
        }

        with (
            patch("sys.argv", ["publish_youtube.py", "28"]),
            patch("scripts.publish_youtube.load_status", return_value=mock_status),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Could not extract video ID" in captured.out

    def test_dry_run_validates_without_publishing(self, capsys):
        """Should validate and exit without publishing in dry-run mode."""
        from scripts.publish_youtube import main

        mock_status = {
            "papers": [
                {
                    "episode": "28",
                    "uploaded": True,
                    "youtube_url": "https://www.youtube.com/watch?v=test123",
                }
            ]
        }

        mock_youtube = MagicMock()
        mock_youtube.videos().list().execute.return_value = {
            "items": [{"status": {"privacyStatus": "private"}}]
        }

        with (
            patch("sys.argv", ["publish_youtube.py", "28", "--dry-run"]),
            patch("scripts.publish_youtube.load_status", return_value=mock_status),
            patch("scripts.publish_youtube.get_authenticated_service", return_value=mock_youtube),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Dry run complete" in captured.out
        mock_youtube.videos().update.assert_not_called()

    def test_updates_status_when_already_public_on_youtube(self, capsys):
        """Should update status.json if video already public on YouTube."""
        from scripts.publish_youtube import main

        mock_status = {
            "papers": [
                {
                    "episode": "28",
                    "uploaded": True,
                    "youtube_url": "https://www.youtube.com/watch?v=test123",
                }
            ]
        }

        mock_youtube = MagicMock()
        mock_youtube.videos().list().execute.return_value = {
            "items": [{"status": {"privacyStatus": "public"}}]
        }

        with (
            patch("sys.argv", ["publish_youtube.py", "28"]),
            patch("scripts.publish_youtube.load_status", return_value=mock_status),
            patch("scripts.publish_youtube.get_authenticated_service", return_value=mock_youtube),
            patch("scripts.publish_youtube.update_episode_status") as mock_update,
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "already public on YouTube" in captured.out
        mock_update.assert_called_once_with("28", "published", True)

    def test_publishes_video_and_updates_status(self, capsys):
        """Should publish video and update status.json."""
        from scripts.publish_youtube import main

        mock_status = {
            "papers": [
                {
                    "episode": "28",
                    "uploaded": True,
                    "youtube_url": "https://www.youtube.com/watch?v=test123",
                }
            ]
        }

        mock_youtube = MagicMock()
        mock_youtube.videos().list().execute.return_value = {
            "items": [{"status": {"privacyStatus": "private"}}]
        }
        mock_youtube.videos().update().execute.return_value = {"id": "test123"}

        with (
            patch("sys.argv", ["publish_youtube.py", "28"]),
            patch("scripts.publish_youtube.load_status", return_value=mock_status),
            patch("scripts.publish_youtube.get_authenticated_service", return_value=mock_youtube),
            patch("scripts.publish_youtube.update_episode_status") as mock_update,
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Publish complete" in captured.out
        mock_update.assert_called_once_with("28", "published", True)

    def test_exits_1_on_publish_failure(self, capsys):
        """Should exit 1 when publish fails."""
        from scripts.publish_youtube import main

        mock_status = {
            "papers": [
                {
                    "episode": "28",
                    "uploaded": True,
                    "youtube_url": "https://www.youtube.com/watch?v=test123",
                }
            ]
        }

        mock_youtube = MagicMock()
        mock_youtube.videos().list().execute.return_value = {
            "items": [{"status": {"privacyStatus": "private"}}]
        }
        mock_youtube.videos().update().execute.side_effect = Exception("API Error")

        with (
            patch("sys.argv", ["publish_youtube.py", "28"]),
            patch("scripts.publish_youtube.load_status", return_value=mock_status),
            patch("scripts.publish_youtube.get_authenticated_service", return_value=mock_youtube),
        ):
            result = main()

        assert result == 1

    def test_zero_pads_episode_number(self, capsys):
        """Should zero-pad episode number to 2 digits."""
        from scripts.publish_youtube import main

        mock_status = {
            "papers": [
                {
                    "episode": "05",
                    "uploaded": True,
                    "published": True,
                    "youtube_url": "https://www.youtube.com/watch?v=test123",
                }
            ]
        }

        with (
            patch("sys.argv", ["publish_youtube.py", "5"]),
            patch("scripts.publish_youtube.load_status", return_value=mock_status),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Episode 05" in captured.out

    def test_shows_usage_when_no_args(self):
        """Should show usage when no arguments provided."""
        from scripts.publish_youtube import main

        with patch("sys.argv", ["publish_youtube.py"]), pytest.raises(SystemExit):
            main()
