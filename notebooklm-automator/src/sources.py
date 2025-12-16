"""Source management for NotebookLM notebooks."""

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


class SourcesManager:
    """Manages adding and tracking sources in NotebookLM."""

    async def _try_click_any(
        self, page: Page, selectors: list[str], timeout: int = 2000
    ) -> bool:
        """Try to click any of the given selectors."""
        for selector in selectors:
            try:
                await page.click(selector, timeout=timeout)
                logger.debug("Clicked: %s", selector)
                return True
            except Exception:  # noqa: S110
                pass
        return False

    async def add_url(self, page: Page, url: str) -> bool:
        """Add a URL source to the notebook.

        Args:
            page: Browser page on a notebook
            url: URL to add as source

        Returns:
            True if source added successfully

        """
        logger.info("Adding URL source: %s", url)

        # Click add source button
        await page.click(Selectors.ADD_SOURCE_BTN)
        await asyncio.sleep(0.5)

        # Select URL/Website option
        await page.click(Selectors.SOURCE_URL_OPTION)
        await asyncio.sleep(0.5)

        # Enter URL
        url_input = await page.wait_for_selector(
            Selectors.SOURCE_URL_INPUT, timeout=5000
        )
        if url_input:
            await url_input.fill(url)
        else:
            logger.error("URL input not found")
            return False

        # Confirm add
        await page.click(Selectors.SOURCE_ADD_CONFIRM)

        # Wait for processing to start
        await asyncio.sleep(2)

        return True

    async def add_pdf_url(self, page: Page, pdf_url: str) -> bool:
        """Add a PDF URL source to the notebook.

        Args:
            page: Browser page on a notebook
            pdf_url: URL to PDF file

        Returns:
            True if source added successfully

        """
        logger.info("Adding PDF source: %s", pdf_url)

        # Click add source button
        await page.click(Selectors.ADD_SOURCE_BTN)
        await asyncio.sleep(0.5)

        # Try PDF option first, fall back to URL
        try:
            await page.click(Selectors.SOURCE_PDF_OPTION, timeout=2000)
        except Exception:
            await page.click(Selectors.SOURCE_URL_OPTION)

        await asyncio.sleep(0.5)

        # Enter URL
        url_input = await page.wait_for_selector(
            Selectors.SOURCE_URL_INPUT, timeout=5000
        )
        if url_input:
            await url_input.fill(pdf_url)
        else:
            logger.error("URL input not found")
            return False

        # Confirm add
        await page.click(Selectors.SOURCE_ADD_CONFIRM)
        await asyncio.sleep(2)

        return True

    async def add_file(self, page: Page, file_path: Path) -> bool:
        """Add a local file as source to the notebook.

        Args:
            page: Browser page on a notebook
            file_path: Path to local file (PDF, etc.)

        Returns:
            True if source added successfully

        """
        if not file_path.exists():
            logger.error("File not found: %s", file_path)
            return False

        logger.info("Adding file source: %s", file_path)
        logger.debug("Current URL: %s", page.url)

        # Open add source dialog
        try:
            add_btn = page.locator('button:has-text("Add source")').first
            if await add_btn.count() > 0:
                await add_btn.click(timeout=5000)
                logger.debug("Clicked 'Add source' button")
                await asyncio.sleep(1)
            else:
                logger.warning("Add source button not found")
        except Exception as e:
            logger.debug("Add source click failed: %s", e)

        # Click upload option and handle file chooser dialog
        upload_selectors = [
            Selectors.SOURCE_FILE_UPLOAD_OPTION,
            Selectors.SOURCE_PDF_OPTION,
            'button:has-text("Upload file")',
            'button:has-text("upload")',
            '[aria-label*="upload"]',
        ]

        # Use file chooser expectation to intercept native dialog
        async with page.expect_file_chooser() as fc_info:
            await self._try_click_any(page, upload_selectors)

        file_chooser = await fc_info.value
        await file_chooser.set_files(str(file_path))
        logger.info("File selected: %s", file_path.name)

        await asyncio.sleep(2)
        logger.info("File upload completed: %s", file_path.name)

        return True

    async def wait_for_processing(
        self,
        page: Page,
        timeout: int | None = None,
    ) -> bool:
        """Wait for all sources to finish processing.

        Args:
            page: Browser page on a notebook
            timeout: Max wait time in seconds

        Returns:
            True if all sources processed successfully

        """
        timeout = timeout or settings.source_processing_timeout
        logger.info("Waiting for source processing (timeout: %ds)...", timeout)

        start_time = asyncio.get_event_loop().time()
        poll_interval = 5

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed > timeout:
                logger.warning("Source processing timeout")
                return False

            # Check if still processing
            processing = await page.query_selector(Selectors.SOURCE_PROCESSING)
            if not processing:
                logger.info("Source processing complete")
                return True

            logger.debug("Still processing... (%.0fs elapsed)", elapsed)
            await asyncio.sleep(poll_interval)

    async def list_sources(self, page: Page) -> list[dict[str, str]]:
        """List all sources in the notebook.

        Args:
            page: Browser page on a notebook

        Returns:
            List of sources with id, name, status

        """
        sources = []
        elements = await page.query_selector_all(Selectors.SOURCE_LIST_ITEM)

        for element in elements:
            source_id = await element.get_attribute("data-source-id")
            name = await element.inner_text()
            status = await element.get_attribute("data-source-status") or "unknown"

            if source_id:
                sources.append(
                    {
                        "id": source_id,
                        "name": name.strip(),
                        "status": status,
                    }
                )

        return sources

    async def get_source_count(self, page: Page) -> int:
        """Get number of sources in notebook.

        Args:
            page: Browser page on a notebook

        Returns:
            Number of sources

        """
        elements = await page.query_selector_all(Selectors.SOURCE_LIST_ITEM)
        return len(elements)
