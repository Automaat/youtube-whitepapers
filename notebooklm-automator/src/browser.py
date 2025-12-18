"""Chrome browser management via CDP and Playwright."""

from __future__ import annotations

import asyncio
import contextlib
import logging
import subprocess
import sys

from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING

from playwright.async_api import async_playwright

from src.config import settings
from src.ui_selectors import Selectors


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from playwright.async_api import Browser, BrowserContext, Page, Playwright


logger = logging.getLogger(__name__)


class BrowserManager:
    """Manages Chrome browser connection for NotebookLM automation."""

    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._chrome_process: subprocess.Popen[bytes] | None = None
        self._is_cdp: bool = False

    async def _start_playwright(self) -> Playwright:
        if self._playwright is None:
            self._playwright = await async_playwright().start()
        return self._playwright

    async def connect_cdp(self, port: int | None = None) -> Browser:
        """Connect to existing Chrome instance via CDP.

        Args:
            port: Chrome debug port (default from settings)

        Returns:
            Connected browser instance

        """
        port = port or settings.chrome_debug_port
        pw = await self._start_playwright()

        endpoint = f"http://localhost:{port}"
        logger.info("Connecting to Chrome at %s", endpoint)

        self._browser = await pw.chromium.connect_over_cdp(endpoint)
        self._is_cdp = True
        return self._browser

    async def launch_with_profile(
        self,
        profile_dir: Path | None = None,
        *,
        headless: bool | None = None,
    ) -> BrowserContext:
        """Launch Chrome with persistent profile.

        Args:
            profile_dir: Chrome profile directory (default from settings)
            headless: Run in headless mode (default from settings)

        Returns:
            Browser context with persistent profile

        """
        profile_dir = profile_dir or settings.chrome_profile_dir
        headless = headless if headless is not None else settings.headless

        profile_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Launching Chrome with profile: %s", profile_dir)

        pw = await self._start_playwright()
        self._context = await pw.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
            ],
            ignore_default_args=["--enable-automation"],
        )
        return self._context

    def launch_chrome_debug(self, port: int | None = None) -> subprocess.Popen[bytes]:
        """Launch Chrome with remote debugging enabled.

        Args:
            port: Debug port (default from settings)

        Returns:
            Chrome subprocess

        """
        port = port or settings.chrome_debug_port
        profile_dir = settings.chrome_profile_dir
        profile_dir.mkdir(parents=True, exist_ok=True)

        chrome_paths = {
            "darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "linux": "google-chrome",
            "win32": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        }

        chrome_path = chrome_paths.get(sys.platform)
        if not chrome_path:
            msg = f"Unsupported platform: {sys.platform}"
            raise RuntimeError(msg)

        cmd = [
            chrome_path,
            f"--remote-debugging-port={port}",
            f"--user-data-dir={profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-sync",
            "--disable-background-networking",
            "--password-store=basic",
            "--use-mock-keychain",
            settings.notebooklm_base_url,
        ]

        logger.info("Launching Chrome: %s", " ".join(cmd))
        self._chrome_process = subprocess.Popen(cmd)  # noqa: S603
        return self._chrome_process

    async def get_page(self) -> Page:
        """Get the active page or create new one.

        Returns:
            Active browser page

        """
        if self._context:
            pages = self._context.pages
            if pages:
                return pages[0]
            return await self._context.new_page()

        if self._browser:
            contexts = self._browser.contexts
            if contexts:
                pages = contexts[0].pages
                if pages:
                    return pages[0]
                return await contexts[0].new_page()

        msg = "No browser or context available"
        raise RuntimeError(msg)

    async def navigate_to_notebooklm(self, page: Page | None = None) -> Page:
        """Navigate to NotebookLM homepage.

        Args:
            page: Existing page or None to get/create one

        Returns:
            Page at NotebookLM

        """
        if page is None:
            page = await self.get_page()

        # Skip navigation if already at NotebookLM
        current_url = page.url
        if current_url.startswith(settings.notebooklm_base_url):
            logger.info("Already at NotebookLM: %s", current_url)
            return page

        await page.goto(
            settings.notebooklm_base_url,
            timeout=settings.page_load_timeout * 1000,
            wait_until="domcontentloaded",
        )
        await asyncio.sleep(2)  # Allow page to stabilize
        return page

    async def is_logged_in(self, page: Page) -> bool:
        """Check if user is logged into Google/NotebookLM.

        Args:
            page: Page to check

        Returns:
            True if logged in

        """
        logger.debug("Checking login status, URL: %s", page.url)

        # If on a notebook page, we're logged in
        if "/notebook/" in page.url:
            logger.debug("On notebook page, assuming logged in")
            return True

        try:
            logger.debug("Looking for selector: %s", Selectors.LOGGED_IN_INDICATOR)
            await page.wait_for_selector(
                Selectors.LOGGED_IN_INDICATOR,
                timeout=5000,
            )
            logger.debug("Selector found, logged in")
            return True
        except Exception as e:
            logger.debug("Selector not found: %s", e)
            return False

    async def wait_for_login(self, page: Page, timeout: int = 300) -> bool:
        """Wait for user to complete manual login.

        Args:
            page: Page where login is happening
            timeout: Max wait time in seconds

        Returns:
            True if login successful

        """
        logger.info("Waiting for manual login (timeout: %ds)...", timeout)
        logger.debug("Looking for: %s", Selectors.LOGGED_IN_INDICATOR)
        try:
            await page.wait_for_selector(
                Selectors.LOGGED_IN_INDICATOR,
                timeout=timeout * 1000,
            )
            logger.info("Login successful")
            return True
        except Exception:
            logger.warning("Login timeout")
            # Debug: dump page info
            logger.debug("Final URL: %s", page.url)
            try:
                await page.screenshot(path="/tmp/notebooklm-login-fail.png")
                logger.debug("Screenshot saved to /tmp/notebooklm-login-fail.png")
            except Exception as e:
                logger.debug("Screenshot failed: %s", e)
            return False

    async def close(self, page: Page | None = None) -> None:
        """Close browser and cleanup resources."""
        # Navigate to home to clean up state (avoid leftover dialogs)
        if page and self._is_cdp:
            with contextlib.suppress(Exception):
                await page.goto(settings.notebooklm_base_url, wait_until="domcontentloaded")

        if self._context:
            await self._context.close()
            self._context = None

        # Don't close browser for CDP - just disconnect
        if self._browser and not self._is_cdp:
            await self._browser.close()
        self._browser = None

        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

        if self._chrome_process:
            self._chrome_process.terminate()
            self._chrome_process = None


@asynccontextmanager
async def browser_session(
    *,
    use_cdp: bool = False,
    port: int | None = None,
    profile_dir: Path | None = None,
    headless: bool | None = None,
) -> AsyncGenerator[tuple[BrowserManager, Page], None]:
    """Context manager for browser session.

    Args:
        use_cdp: Connect to existing Chrome via CDP
        port: CDP port (when use_cdp=True)
        profile_dir: Profile directory (when use_cdp=False)
        headless: Run headless (when use_cdp=False)

    Yields:
        Tuple of (BrowserManager, Page)

    """
    manager = BrowserManager()
    page: Page | None = None
    try:
        if use_cdp:
            await manager.connect_cdp(port)
        else:
            # Try CDP first in case Chrome is already running
            try:
                await manager.connect_cdp(port)
                logger.info("Connected to existing Chrome via CDP")
            except Exception:
                # No existing Chrome, launch with profile
                await manager.launch_with_profile(profile_dir, headless=headless)

        page = await manager.navigate_to_notebooklm()

        # Wait briefly for page to stabilize
        await asyncio.sleep(1)

        yield manager, page
    finally:
        await manager.close(page)
