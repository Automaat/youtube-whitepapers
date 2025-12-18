"""Audio Overview generation and download."""

from __future__ import annotations

import asyncio
import logging

from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

from src.config import settings
from src.ui_selectors import Selectors


if TYPE_CHECKING:
    from playwright.async_api import Page


logger = logging.getLogger(__name__)


class AudioStatus(Enum):
    """Audio generation status."""

    NOT_STARTED = "not_started"
    GENERATING = "generating"
    READY = "ready"
    ERROR = "error"


class AudioManager:
    """Manages Audio Overview generation and download."""

    async def get_status(self, page: Page) -> AudioStatus:
        """Get current audio generation status.

        Args:
            page: Browser page on a notebook

        Returns:
            Current audio status

        """
        # Check if ready
        ready = await page.query_selector(Selectors.AUDIO_READY_INDICATOR)
        if ready:
            return AudioStatus.READY

        # Check if generating
        generating = await page.query_selector(Selectors.AUDIO_GENERATING_INDICATOR)
        if generating:
            return AudioStatus.GENERATING

        return AudioStatus.NOT_STARTED

    async def generate(
        self,
        page: Page,
        prompt: str | None = None,
        language: str | None = None,
    ) -> bool:
        """Start audio overview generation.

        Args:
            page: Browser page on a notebook
            prompt: Custom instructions for audio generation
            language: Language for audio (e.g., "Polish", "English")

        Returns:
            True if generation started

        """
        logger.info("Starting Audio Overview generation")

        # Click Audio Overview button
        try:
            await page.click(Selectors.AUDIO_OVERVIEW_BTN, timeout=5000)
            await asyncio.sleep(1)
        except Exception:
            logger.debug("Audio Overview section might already be open")

        # If prompt or language specified, use customize flow
        if prompt or language:
            try:
                await page.click(Selectors.AUDIO_CUSTOMIZE_BTN, timeout=5000)
                await asyncio.sleep(1)
                logger.info("Opened customize dialog")

                # Enter prompt if provided
                if prompt:
                    await page.fill(Selectors.AUDIO_PROMPT_INPUT, prompt, timeout=5000)
                    logger.info("Entered custom prompt")

                # Select language if provided
                if language:
                    # Click language dropdown and select option
                    await page.click(Selectors.AUDIO_LANGUAGE_DROPDOWN, timeout=5000)
                    await asyncio.sleep(0.5)
                    lang_option = f'[role="option"]:has-text("{language}"), button:has-text("{language}")'
                    await page.click(lang_option, timeout=5000)
                    logger.info("Selected language: %s", language)

            except Exception as e:
                logger.warning("Customization failed: %s", e)

        # Click Generate button
        try:
            await page.click(Selectors.AUDIO_GENERATE_BTN, timeout=5000)
            logger.info("Generation started")
            return True
        except Exception:
            # Check if already generating or ready
            status = await self.get_status(page)
            if status in (AudioStatus.GENERATING, AudioStatus.READY):
                logger.info("Audio already %s", status.value)
                return True
            logger.error("Failed to start generation")
            return False

    async def wait_for_completion(
        self,
        page: Page,
        timeout: int | None = None,
        poll_interval: int = 30,
    ) -> bool:
        """Wait for audio generation to complete.

        Args:
            page: Browser page on a notebook
            timeout: Max wait time in seconds (default 15 min)
            poll_interval: Seconds between status checks

        Returns:
            True if audio ready

        """
        timeout = timeout or settings.audio_generation_timeout
        logger.info("Waiting for audio generation (timeout: %ds)...", timeout)

        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed > timeout:
                logger.error("Audio generation timeout after %ds", timeout)
                return False

            status = await self.get_status(page)
            logger.info("Audio status: %s (%.0fs elapsed)", status.value, elapsed)

            if status == AudioStatus.READY:
                return True

            if status == AudioStatus.ERROR:
                logger.error("Audio generation failed")
                return False

            await asyncio.sleep(poll_interval)

    async def _open_audio_player(self, page: Page) -> bool:
        """Click on generated audio item to open player."""
        selectors = [
            'button:has-text("Deep Dive")',
            'a:has-text("Deep Dive")',
            '[role="button"]:has-text("Deep Dive")',
            'div:has-text("Deep Dive"):has-text("source") >> nth=0',
        ]
        for sel in selectors:
            try:
                item = page.locator(sel).first
                if await item.is_visible(timeout=2000):
                    await item.dblclick(timeout=3000)
                    await asyncio.sleep(2)
                    logger.info("Double-clicked audio item: %s", sel)
                    return True
            except Exception:
                logger.debug("Audio item selector %s not found", sel)
        return False

    async def _click_download_button(self, page: Page) -> bool:
        """Click download via 3-dot menu or direct button."""
        menu_selectors = [
            '[aria-label="More options"]',
            '[aria-label="More actions"]',
            '[aria-label*="More"]',
            'button[aria-label*="menu" i]',
        ]
        for menu_sel in menu_selectors:
            try:
                menus = page.locator(menu_sel)
                count = await menus.count()
                logger.debug("Found %d elements for %s", count, menu_sel)
                for i in range(count):
                    menu = menus.nth(i)
                    if await menu.is_visible(timeout=500):
                        await menu.click(timeout=3000)
                        await asyncio.sleep(0.5)
                        download = page.locator(
                            '[role="menuitem"]:has-text("Download"), '
                            'button:has-text("Download"), '
                            ':text("Download")'
                        ).first
                        if await download.is_visible(timeout=2000):
                            await download.click(timeout=3000)
                            return True
                        await page.keyboard.press("Escape")
                        await asyncio.sleep(0.3)
            except Exception as e:
                logger.debug("Menu selector %s failed: %s", menu_sel, e)

        # Try direct download button as fallback
        for selector in ['button[aria-label="Download"]', 'button:has-text("Download")']:
            try:
                locator = page.locator(selector).first
                if await locator.is_visible(timeout=1000):
                    await locator.click(timeout=3000)
                    return True
            except Exception:
                logger.debug("Direct selector %s not found", selector)
        return False

    async def download(self, page: Page, output_path: Path) -> Path | None:
        """Download generated audio."""
        logger.info("Downloading audio to: %s", output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if not await self._open_audio_player(page):
            logger.warning("Could not find generated audio item")

        async with page.expect_download() as download_info:
            if not await self._click_download_button(page):
                logger.error("Could not find download button")
                return None

        download = await download_info.value
        await download.save_as(output_path)

        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            logger.info("Downloaded: %s (%.1f MB)", output_path, size_mb)
            return output_path

        logger.error("Download failed")
        return None

    async def generate_and_download(
        self,
        page: Page,
        output_path: Path,
        timeout: int | None = None,
    ) -> Path | None:
        """Generate audio and download when ready.

        Args:
            page: Browser page on a notebook
            output_path: Where to save the audio
            timeout: Max wait time for generation

        Returns:
            Path to downloaded file or None

        """
        # Check current status
        status = await self.get_status(page)

        if status == AudioStatus.NOT_STARTED and not await self.generate(page):
            return None

        if status != AudioStatus.READY and not await self.wait_for_completion(
            page, timeout
        ):
            return None

        return await self.download(page, output_path)
