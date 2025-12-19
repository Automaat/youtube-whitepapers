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
    LIMIT_REACHED = "limit_reached"


class AudioManager:
    """Manages Audio Overview generation and download."""

    async def _select_language(self, page: Page, language: str) -> bool:
        """Select language from dropdown."""
        # Click on the mat-select dropdown (shows current language like "English")
        dropdown_selectors = [
            'mat-select:below(:text("Choose language"))',
            '.mat-mdc-select:below(:text("Choose language"))',
            '[role="combobox"]:below(:text("Choose language"))',
            'mat-form-field:has-text("English") mat-select',
            'mat-form-field:has-text("Polish") mat-select',
        ]

        for sel in dropdown_selectors:
            try:
                dropdown = page.locator(sel).first
                if await dropdown.is_visible(timeout=1000):
                    await dropdown.click(timeout=3000)
                    await asyncio.sleep(1)
                    logger.debug("Clicked language dropdown: %s", sel)
                    break
            except Exception:
                continue
        else:
            logger.warning("Could not find language dropdown")
            return False

        # Try different language name formats and selectors
        lang_variants = [language, "Polski", "Polish (Poland)"]
        option_selectors = [
            'mat-option:has-text("{lang}")',
            '[role="option"]:has-text("{lang}")',
            '.mat-mdc-option:has-text("{lang}")',
        ]

        for lang_name in lang_variants:
            for sel_template in option_selectors:
                try:
                    sel = sel_template.format(lang=lang_name)
                    opt = page.locator(sel).first
                    if await opt.is_visible(timeout=1000):
                        await opt.click(timeout=2000)
                        logger.info("Selected language: %s", lang_name)
                        return True
                except Exception:
                    continue

        logger.warning("Could not find language: %s", language)
        await page.keyboard.press("Escape")
        return False

    async def _enter_prompt(self, page: Page, prompt: str) -> bool:
        """Enter prompt in the instructions textarea."""
        # The popup has a textarea for custom instructions
        # Try various selectors to find it
        textarea_selectors = [
            'textarea:below(:text("Add more details"))',
            'textarea:below(:text("instructions"))',
            'textarea:below(:text("optional"))',
            "mat-form-field textarea",
            '[class*="cdk-overlay"] textarea',
            '[role="dialog"] textarea',
            'textarea[placeholder*="Add"]',
            'textarea[placeholder*="instruction"]',
            "textarea",  # fallback: any textarea in visible popup
        ]

        for sel in textarea_selectors:
            try:
                textarea = page.locator(sel).first
                if await textarea.is_visible(timeout=500):
                    await textarea.click(timeout=2000)
                    await textarea.fill("")
                    await textarea.type(prompt, delay=5)
                    logger.info("Entered custom prompt using: %s", sel)
                    return True
            except Exception:
                continue

        logger.warning("Could not find instructions textarea")
        return False

    async def _customize_audio(
        self, page: Page, language: str | None, prompt: str | None
    ) -> bool:
        """Fill in customize popup with language and prompt."""
        try:
            await page.wait_for_selector("text=Choose language", timeout=5000)
            logger.debug("Popup loaded")

            if language:
                await self._select_language(page, language)
                await asyncio.sleep(0.5)

            if prompt:
                await self._enter_prompt(page, prompt)

            return True
        except Exception as e:
            logger.warning("Customization failed: %s", e)
            return False

    async def get_status(self, page: Page) -> AudioStatus:
        """Get current audio generation status.

        Args:
            page: Browser page on a notebook

        Returns:
            Current audio status

        """
        # Check if limit reached
        limit = await page.query_selector(Selectors.AUDIO_LIMIT_INDICATOR)
        if limit:
            return AudioStatus.LIMIT_REACHED

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
    ) -> AudioStatus:
        """Start audio overview generation.

        Args:
            page: Browser page on a notebook
            prompt: Custom instructions for audio generation
            language: Language for audio (e.g., "Polish", "English")

        Returns:
            AudioStatus indicating result (GENERATING, READY, LIMIT_REACHED, ERROR)

        """
        logger.info("Starting Audio Overview generation")

        # Wait for page to fully load
        await asyncio.sleep(3)

        # Click pen/edit icon on Audio Overview card to open customize popup
        try:
            # Find the edit button by aria-label (more reliable)
            edit_btn = page.locator('[aria-label="Customize Audio Overview"]').first
            # Wait for button to be enabled
            await edit_btn.wait_for(state="visible", timeout=10000)
            await asyncio.sleep(1)
            await edit_btn.click(timeout=5000)
            await asyncio.sleep(2)
            logger.info("Clicked Audio Overview edit button")
        except Exception as e:
            logger.warning("Failed to click edit button: %s", e)

        # Now in customize popup - set language and prompt
        if prompt or language:
            await self._customize_audio(page, language, prompt)

        # Click Generate button
        try:
            gen_btn = page.locator('button:has-text("Generate")').last
            await gen_btn.click(timeout=5000)
            await asyncio.sleep(3)
        except Exception as e:
            logger.warning("Failed to click generate: %s", e)

        # Check for limit message more thoroughly (may appear in dialog/toast)
        limit_phrases = [
            "reached your limit",
            "daily limit",
            "generation limit",
            "quota exceeded",
            "too many requests",
            "try again later",
            "rate limit",
        ]
        page_text = await page.content()
        page_text_lower = page_text.lower()
        for phrase in limit_phrases:
            if phrase in page_text_lower:
                logger.warning("Limit indicator found in page: %s", phrase)
                return AudioStatus.LIMIT_REACHED

        # Check actual status after clicking
        status = await self.get_status(page)
        logger.info("Status after generate click: %s", status.value)

        if status == AudioStatus.LIMIT_REACHED:
            logger.warning("Daily audio generation limit reached")
            return AudioStatus.LIMIT_REACHED

        if status in (AudioStatus.GENERATING, AudioStatus.READY):
            logger.info("Audio %s", status.value)
            return status

        # NOT_STARTED means generation didn't actually start
        logger.error("Generation did not start, status: %s", status.value)
        return AudioStatus.ERROR

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

        if status == AudioStatus.NOT_STARTED:
            gen_result = await self.generate(page)
            if gen_result in (AudioStatus.ERROR, AudioStatus.LIMIT_REACHED):
                return None
            status = gen_result

        if status != AudioStatus.READY and not await self.wait_for_completion(
            page, timeout
        ):
            return None

        return await self.download(page, output_path)
