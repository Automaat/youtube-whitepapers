"""Slides generation via chat prompt and PDF export."""

from __future__ import annotations

import asyncio
import logging

from pathlib import Path
from typing import TYPE_CHECKING

from src.config import settings
from src.ui_selectors import Selectors


if TYPE_CHECKING:
    from playwright.async_api import Page


logger = logging.getLogger(__name__)


class SlidesManager:
    """Manages slides generation via NotebookLM chat."""

    async def send_prompt(self, page: Page, prompt: str) -> bool:
        """Send a prompt to the chat interface.

        Args:
            page: Browser page on a notebook
            prompt: The prompt to send

        Returns:
            True if prompt sent successfully

        """
        logger.info("Sending prompt (%d chars)", len(prompt))

        # Find chat input
        chat_input = await page.wait_for_selector(Selectors.CHAT_INPUT, timeout=10000)
        if not chat_input:
            logger.error("Chat input not found")
            return False

        # Enter prompt
        await chat_input.fill(prompt)
        await asyncio.sleep(0.5)

        # Send
        await page.click(Selectors.CHAT_SEND_BTN)
        logger.info("Prompt sent")

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
