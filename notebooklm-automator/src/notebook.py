"""Notebook creation and management."""

from __future__ import annotations

import asyncio
import logging
import re

from typing import TYPE_CHECKING

from src.config import settings
from src.ui_selectors import Selectors


if TYPE_CHECKING:
    from playwright.async_api import Page


logger = logging.getLogger(__name__)


class NotebookManager:
    """Manages NotebookLM notebook operations."""

    async def _close_dialogs(self, page: Page) -> None:
        """Close any open dialogs/modals."""
        # Press Escape to close any dialogs (safe, won't trigger actions)
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.5)

    async def create_notebook(self, page: Page, name: str) -> str | None:
        """Create a new notebook.

        Args:
            page: Browser page at NotebookLM
            name: Notebook name

        Returns:
            Notebook URL if successful, None otherwise

        """
        logger.info("Creating notebook: %s", name)

        # Navigate to home to get clean state
        await page.goto(settings.notebooklm_base_url, wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # Close any open dialogs
        await self._close_dialogs(page)

        # Click create new notebook - wait for button to be stable first
        create_btn = page.locator('button:has-text("New notebook")').first
        if await create_btn.count() == 0:
            create_btn = page.locator('button:has-text("Create")').first

        # Wait for button to be enabled and stable before clicking
        await create_btn.wait_for(state="visible", timeout=5000)
        await asyncio.sleep(0.3)  # Small delay to ensure UI is stable
        await create_btn.click(timeout=5000, click_count=1)
        logger.debug("Clicked create notebook button")

        # Wait for navigation to new notebook
        await page.wait_for_url("**/notebook/**", timeout=15000)
        await asyncio.sleep(2)

        # Close add source dialog if open (blocks title interaction)
        if "addSource=true" in page.url:
            # Press Escape multiple times to ensure dialog closes
            await page.keyboard.press("Escape")
            await asyncio.sleep(0.5)
            await page.keyboard.press("Escape")
            await asyncio.sleep(1)

        # Rename notebook - find and click on "Untitled notebook" text
        renamed = False

        # Try to find element containing "Untitled" text (default notebook name)
        try:
            untitled = page.locator('text="Untitled notebook"').first
            if await untitled.count() > 0:
                logger.debug("Found 'Untitled notebook' element")
                # Use force=True to click even if element appears hidden behind dialog
                await untitled.dblclick(force=True, timeout=5000)
                await asyncio.sleep(0.5)
                await page.keyboard.press("Meta+a")
                await page.keyboard.type(name)
                await page.keyboard.press("Enter")
                await asyncio.sleep(0.5)
                renamed = True
                logger.info("Notebook renamed to: %s", name)
        except Exception as e:
            logger.debug("Untitled locator failed: %s", e)

        # Fallback: try specific selectors
        if not renamed:
            title_selectors = [
                '[class*="notebook-title"]',
                '[class*="notebook-name"]',
                '[aria-label*="Rename"]',
                "header h1",
            ]
            for selector in title_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        await element.dblclick()
                        await asyncio.sleep(0.5)
                        await page.keyboard.press("Meta+a")
                        await page.keyboard.type(name)
                        await page.keyboard.press("Enter")
                        await asyncio.sleep(0.5)
                        renamed = True
                        logger.info("Notebook renamed to: %s", name)
                        break
                except Exception as e:
                    logger.debug("Selector %s failed: %s", selector, e)

        if not renamed:
            logger.warning("Could not rename notebook to: %s", name)

        await asyncio.sleep(1)

        # Extract notebook URL (remove query params for cleaner URL)
        url = page.url.split("?")[0]
        if "notebook" in url:
            logger.info("Notebook created: %s", url)
            return url

        logger.warning("Failed to create notebook")
        return None

    async def open_notebook(self, page: Page, url: str) -> bool:
        """Open existing notebook by URL.

        Args:
            page: Browser page
            url: Notebook URL

        Returns:
            True if notebook opened successfully

        """
        logger.info("Opening notebook: %s", url)

        await page.goto(url, timeout=settings.page_load_timeout * 1000)
        await page.wait_for_load_state("networkidle")

        # Verify we're on a notebook page
        return "notebook" in page.url

    async def get_notebook_id(self, page: Page) -> str | None:
        """Extract notebook ID from current page URL.

        Args:
            page: Browser page on a notebook

        Returns:
            Notebook ID or None

        """
        url = page.url
        match = re.search(r"/notebook/([a-zA-Z0-9_-]+)", url)
        return match.group(1) if match else None

    async def list_notebooks(self, page: Page) -> list[dict[str, str]]:
        """List all notebooks.

        Args:
            page: Browser page at NotebookLM home

        Returns:
            List of notebooks with id, name, url

        """
        await page.goto(settings.notebooklm_base_url)
        await page.wait_for_load_state("networkidle")

        notebooks = []
        elements = await page.query_selector_all(Selectors.NOTEBOOK_LIST_ITEM)

        for element in elements:
            notebook_id = await element.get_attribute("data-notebook-id")
            name = await element.inner_text()
            if notebook_id:
                notebooks.append(
                    {
                        "id": notebook_id,
                        "name": name.strip(),
                        "url": f"{settings.notebooklm_base_url}/notebook/{notebook_id}",
                    }
                )

        return notebooks

    async def delete_notebook(
        self,
        page: Page,  # noqa: ARG002
        notebook_id: str,  # noqa: ARG002
    ) -> bool:
        """Delete a notebook.

        Args:
            page: Browser page
            notebook_id: ID of notebook to delete

        Returns:
            True if deleted successfully

        """
        logger.warning("Delete notebook not implemented - requires manual action")
        return False
