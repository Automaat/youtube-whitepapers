"""Slides generation via chat prompt and PDF export."""

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


class SlidesStatus(Enum):
    """Slides generation status."""

    NOT_FOUND = "not_found"
    READY = "ready"
    LIMIT_REACHED = "limit_reached"
    ERROR = "error"


class SlidesManager:
    """Manages slides generation via NotebookLM chat."""

    async def _select_language(self, page: Page, language: str) -> bool:
        """Select language from dropdown."""
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
        textarea_selectors = [
            'textarea:below(:text("Add more details"))',
            'textarea:below(:text("instructions"))',
            'textarea:below(:text("optional"))',
            "mat-form-field textarea",
            '[class*="cdk-overlay"] textarea',
            '[role="dialog"] textarea',
            'textarea[placeholder*="Add"]',
            'textarea[placeholder*="instruction"]',
            "textarea",
        ]

        for sel in textarea_selectors:
            try:
                textarea = page.locator(sel).first
                if await textarea.is_visible(timeout=500):
                    await textarea.click(timeout=2000)
                    await textarea.fill(prompt)
                    logger.info("Entered custom prompt using: %s", sel)
                    return True
            except Exception:
                continue

        logger.warning("Could not find instructions textarea")
        return False

    async def send_prompt(self, page: Page, prompt: str) -> bool:
        """Generate slides via Studio panel.

        Args:
            page: Browser page on a notebook
            prompt: The prompt to send

        Returns:
            True if prompt sent successfully

        """
        logger.info("Sending prompt (%d chars)", len(prompt))

        # Wait for page to fully load
        await asyncio.sleep(3)

        # Click on Slide Deck card in Studio panel
        slide_deck_selectors = [
            '[aria-label="Customize Slide Deck"]',
            'button:has-text("Slide Deck")',
            ':text("Slide Deck") >> xpath=ancestor::button',
            'div:has-text("Slide Deck") >> nth=0',
        ]

        clicked_edit = False
        for sel in slide_deck_selectors:
            try:
                btn = page.locator(sel).first
                if await btn.is_visible(timeout=2000):
                    await btn.click(timeout=3000)
                    await asyncio.sleep(2)
                    logger.info("Clicked Slide Deck button: %s", sel)
                    clicked_edit = True
                    break
            except Exception:
                logger.debug("Slide Deck selector %s not found", sel)

        if not clicked_edit:
            logger.error("Could not find Slide Deck button")
            return False

        # Select Polish language first
        await self._select_language(page, "Polish")
        await asyncio.sleep(0.5)

        # Enter prompt in popup
        if prompt:
            await self._enter_prompt(page, prompt)

        # Click Generate button
        try:
            gen_btn = page.locator('button:has-text("Generate")').last
            await gen_btn.click(timeout=5000)
            logger.info("Clicked Generate button")
        except Exception as e:
            logger.error("Failed to click Generate: %s", e)
            return False

        # Poll for limit indicators (check multiple times)
        for i in range(5):
            await asyncio.sleep(1)
            logger.debug("Checking for limit (attempt %d/5)...", i + 1)

            # Check for limit using locator-based detection
            if await self._check_limit_reached(page):
                logger.warning("Daily slides generation limit reached")
                return False

            # Check page text for limit phrases
            page_text = await page.inner_text("body")
            page_text_lower = page_text.lower()
            logger.debug("Page text sample: %s", page_text_lower[:500])

            limit_phrases = [
                "reached your daily slides limits",
                "come back later",
                "reached your limit",
                "daily limit",
                "generation limit",
                "quota exceeded",
                "too many requests",
                "try again later",
                "rate limit",
                "limit reached",
                "come back tomorrow",
            ]
            for phrase in limit_phrases:
                if phrase in page_text_lower:
                    logger.warning("Limit phrase found: %s", phrase)
                    return False

        return True

    async def wait_for_response(
        self,
        page: Page,
        timeout: int | None = None,
    ) -> bool:
        """Wait for chat response to complete.

        Args:
            page: Browser page on a notebook
            timeout: Max wait time in seconds

        Returns:
            True if response received

        """
        timeout = timeout or settings.slides_generation_timeout
        logger.info("Waiting for response (timeout: %ds)...", timeout)

        start_time = asyncio.get_event_loop().time()
        poll_interval = 3

        # Wait for loading indicator to appear
        await asyncio.sleep(2)

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed > timeout:
                logger.error("Response timeout after %ds", timeout)
                return False

            # Check if still loading
            loading = await page.query_selector(Selectors.CHAT_LOADING)
            if not loading:
                # Check for response
                response = await page.query_selector(Selectors.CHAT_RESPONSE)
                if response:
                    logger.info("Response received")
                    return True

            logger.debug("Waiting for response... (%.0fs elapsed)", elapsed)
            await asyncio.sleep(poll_interval)

    async def export_pdf(self, page: Page, output_path: Path) -> Path | None:
        """Export chat response/slides as PDF.

        Args:
            page: Browser page with generated content
            output_path: Where to save the PDF

        Returns:
            Path to exported PDF or None

        """
        logger.info("Exporting PDF to: %s", output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Set up download handler
        async with page.expect_download() as download_info:
            # Click export button
            await page.click(Selectors.EXPORT_BTN)
            await asyncio.sleep(0.5)

            # Select PDF format
            await page.click(Selectors.EXPORT_PDF_OPTION)

        download = await download_info.value

        # Save to output path
        await download.save_as(output_path)

        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            logger.info("Exported: %s (%.1f KB)", output_path, size_kb)
            return output_path

        logger.error("Export failed")
        return None

    async def generate_slides(
        self,
        page: Page,
        prompt: str,
        output_path: Path,
        timeout: int | None = None,
    ) -> Path | None:
        """Generate slides from prompt and export as PDF.

        Args:
            page: Browser page on a notebook
            prompt: Slide generation prompt
            output_path: Where to save the PDF
            timeout: Max wait time for generation

        Returns:
            Path to exported PDF or None

        """
        if not await self.send_prompt(page, prompt):
            return None

        if not await self.wait_for_response(page, timeout):
            return None

        return await self.export_pdf(page, output_path)

    async def generate_from_file(
        self,
        page: Page,
        prompt_file: Path,
        output_path: Path,
        timeout: int | None = None,
    ) -> Path | None:
        """Generate slides from prompt file.

        Args:
            page: Browser page on a notebook
            prompt_file: Path to file containing prompt
            output_path: Where to save the PDF
            timeout: Max wait time for generation

        Returns:
            Path to exported PDF or None

        """
        if not prompt_file.exists():
            logger.error("Prompt file not found: %s", prompt_file)
            return None

        prompt = prompt_file.read_text()
        return await self.generate_slides(page, prompt, output_path, timeout)

    async def _check_limit_reached(self, page: Page) -> bool:
        """Check if generation limit is reached."""
        limit_selectors = [
            ':has-text("reached your daily Slides limits")',
            ':has-text("Come back later")',
            ':has-text("reached your limit")',
            ':has-text("daily limit")',
            ':has-text("generation limit")',
            ':has-text("quota exceeded")',
            ':has-text("try again later")',
            ':has-text("limit reached")',
            ':has-text("come back tomorrow")',
            '[role="dialog"]:has-text("limit")',
            '[role="alertdialog"]:has-text("limit")',
            '.mat-snack-bar-container:has-text("limit")',
            '.cdk-overlay-pane:has-text("limit")',
            '[class*="snackbar"]:has-text("limit")',
            '[class*="toast"]:has-text("limit")',
            '[class*="error"]:has-text("limit")',
        ]
        for sel in limit_selectors:
            try:
                elem = page.locator(sel).first
                if await elem.is_visible(timeout=300):
                    logger.warning("Limit indicator visible: %s", sel)
                    return True
            except Exception:
                continue
        return False

    async def get_status(self, page: Page) -> SlidesStatus:
        """Check if slides are available in notebook."""
        # Check if limit reached first
        if await self._check_limit_reached(page):
            return SlidesStatus.LIMIT_REACHED

        selectors = [
            'button:has-text("Briefing doc")',
            '[role="button"]:has-text("Briefing doc")',
            'div:has-text("Briefing doc") >> nth=0',
        ]
        for sel in selectors:
            try:
                item = page.locator(sel).first
                if await item.is_visible(timeout=2000):
                    return SlidesStatus.READY
            except Exception:
                logger.debug("Slides status selector %s not found", sel)
        return SlidesStatus.NOT_FOUND

    async def _open_slides_panel(self, page: Page) -> bool:
        """Click on Briefing doc to open slides panel."""
        selectors = [
            'button:has-text("Briefing doc")',
            'a:has-text("Briefing doc")',
            '[role="button"]:has-text("Briefing doc")',
            'div:has-text("Briefing doc") >> nth=0',
        ]
        for sel in selectors:
            try:
                item = page.locator(sel).first
                if await item.is_visible(timeout=2000):
                    await item.dblclick(timeout=3000)
                    await asyncio.sleep(2)
                    logger.info("Double-clicked slides item: %s", sel)
                    return True
            except Exception:
                logger.debug("Slides selector %s not found", sel)
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
        """Download generated slides as PDF."""
        logger.info("Downloading slides to: %s", output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if not await self._open_slides_panel(page):
            logger.warning("Could not find slides item")

        async with page.expect_download() as download_info:
            if not await self._click_download_button(page):
                logger.error("Could not find download button")
                return None

        download = await download_info.value
        await download.save_as(output_path)

        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            logger.info("Downloaded: %s (%.1f KB)", output_path, size_kb)
            return output_path

        logger.error("Download failed")
        return None
