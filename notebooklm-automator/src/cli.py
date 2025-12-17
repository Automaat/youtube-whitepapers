"""CLI entry point using Typer."""

from __future__ import annotations

import asyncio
import logging

from pathlib import Path
from typing import Annotated

import typer

from rich.console import Console
from rich.logging import RichHandler

from src.audio import AudioManager, AudioStatus
from src.browser import BrowserManager, browser_session
from src.config import settings
from src.notebook import NotebookManager
from src.slides import SlidesManager
from src.sources import SourcesManager
from src.ui_selectors import Selectors


app = typer.Typer(
    name="notebooklm-automator",
    help="Automate NotebookLM interactions via browser automation",
    no_args_is_help=True,
)

console = Console()


def setup_logging(verbose: bool = False) -> None:
    """Configure logging with rich handler."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, show_path=False)],
    )


# --- Init & Login Commands ---


@app.command()
def init(
    profile_dir: Annotated[
        Path | None,
        typer.Option("--profile-dir", "-p", help="Chrome profile directory"),
    ] = None,
) -> None:
    """Initialize Chrome profile directory."""
    profile = profile_dir or settings.chrome_profile_dir
    profile.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]Created profile directory:[/] {profile}")
    console.print("\n[yellow]Next steps:[/]")
    console.print("1. Run [bold]notebooklm-automator login[/] to authenticate")
    console.print("2. Sign in with your Google account in the browser")


@app.command()
def login(
    port: Annotated[
        int,
        typer.Option("--port", "-p", help="Chrome debug port"),
    ] = 9222,
    timeout: Annotated[
        int,
        typer.Option("--timeout", "-t", help="Login timeout in seconds"),
    ] = 300,
) -> None:
    """Launch Chrome for manual Google login."""
    setup_logging()

    manager = BrowserManager()

    console.print("[yellow]Launching Chrome...[/]")
    manager.launch_chrome_debug(port)

    console.print("\n[bold]Please sign in to your Google account in the browser.[/]")
    console.print(f"[dim]Timeout: {timeout}s[/]\n")

    async def wait_login() -> bool:
        await asyncio.sleep(3)  # Wait for Chrome to start
        await manager.connect_cdp(port)
        page = await manager.get_page()
        result = await manager.wait_for_login(page, timeout)
        await manager.close()
        return result

    success = asyncio.run(wait_login())

    if success:
        console.print("[green]Login successful![/]")
    else:
        console.print("[red]Login timeout or failed[/]")
        raise typer.Exit(1)


# --- Notebook Commands ---

notebook_app = typer.Typer(help="Notebook management commands")
app.add_typer(notebook_app, name="notebook")


@notebook_app.command("create")
def notebook_create(
    name: Annotated[str, typer.Option("--name", "-n", help="Notebook name")],
    source: Annotated[
        str | None,
        typer.Option("--source", "-s", help="Source URL"),
    ] = None,
    file: Annotated[
        Path | None,
        typer.Option("--file", "-f", help="Local file to upload (PDF)"),
    ] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Create a new notebook with optional source URL or file."""
    setup_logging(verbose)

    if file and not file.exists():
        console.print(f"[red]File not found:[/] {file}")
        raise typer.Exit(1)

    async def run() -> str | None:
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return None

            notebook = NotebookManager()
            url = await notebook.create_notebook(page, name)

            if url:
                sources = SourcesManager()
                if file:
                    await sources.add_file(page, file)
                    await sources.wait_for_processing(page)
                elif source:
                    await sources.add_url(page, source)
                    await sources.wait_for_processing(page)

            return url

    url = asyncio.run(run())
    if url:
        console.print(f"[green]Notebook created:[/] {url}")
    else:
        raise typer.Exit(1)


@notebook_app.command("list")
def notebook_list(
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """List all notebooks."""
    setup_logging(verbose)

    async def run() -> list[dict[str, str]]:
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return []

            notebook = NotebookManager()
            return await notebook.list_notebooks(page)

    notebooks = asyncio.run(run())
    for nb in notebooks:
        console.print(f"[bold]{nb['name']}[/]")
        console.print(f"  [dim]{nb['url']}[/]")


# --- Audio Commands ---

audio_app = typer.Typer(help="Audio Overview commands")
app.add_typer(audio_app, name="audio")


PROMPT_FILE = (
    Path(__file__).parent.parent.parent
    / "youtube/prompts/notebooklm-research-paper-podcast.md"
)


@audio_app.command("generate")
def audio_generate(
    notebook_url: Annotated[str, typer.Option("--notebook-url", "-u")],
    language: Annotated[
        str,
        typer.Option("--language", "-l", help="Audio language (e.g., Polish, English)"),
    ] = "Polish",
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Start Audio Overview generation with custom prompt and language."""
    setup_logging(verbose)

    # Load prompt from file
    if not PROMPT_FILE.exists():
        console.print(f"[red]Prompt file not found:[/] {PROMPT_FILE}")
        raise typer.Exit(1)
    prompt = PROMPT_FILE.read_text().strip()

    async def run() -> bool:
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return False

            notebook = NotebookManager()
            if not await notebook.open_notebook(page, notebook_url):
                console.print("[red]Failed to open notebook[/]")
                return False

            audio = AudioManager()
            return await audio.generate(page, prompt=prompt, language=language)

    success = asyncio.run(run())
    if success:
        console.print(f"[green]Audio generation started[/] (language: {language})")
    else:
        raise typer.Exit(1)


@audio_app.command("status")
def audio_status(
    notebook_url: Annotated[str, typer.Option("--notebook-url", "-u")],
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Check Audio Overview generation status."""
    setup_logging(verbose)

    async def run() -> str:
        async with browser_session() as (_, page):
            notebook = NotebookManager()
            await notebook.open_notebook(page, notebook_url)

            audio = AudioManager()
            status = await audio.get_status(page)
            return status.value

    status = asyncio.run(run())
    console.print(f"Audio status: [bold]{status}[/]")


@audio_app.command("download")
def audio_download(
    notebook_url: Annotated[str, typer.Option("--notebook-url", "-u")],
    output: Annotated[Path, typer.Option("--output", "-o")],
    timeout: Annotated[
        int,
        typer.Option("--timeout", "-t", help="Wait timeout in seconds"),
    ] = 900,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Wait for audio generation and download when ready."""
    setup_logging(verbose)

    async def run() -> Path | None:
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return None

            notebook = NotebookManager()
            if not await notebook.open_notebook(page, notebook_url):
                console.print("[red]Failed to open notebook[/]")
                return None

            audio = AudioManager()
            status = await audio.get_status(page)

            if status != AudioStatus.READY:
                console.print(f"[yellow]Status: {status.value}, waiting...[/]")
                if not await audio.wait_for_completion(page, timeout):
                    console.print("[red]Audio generation timed out or failed[/]")
                    return None

            return await audio.download(page, output)

    result = asyncio.run(run())
    if result:
        console.print(f"[green]Audio saved:[/] {result}")
    else:
        raise typer.Exit(1)


# --- Slides Commands ---

slides_app = typer.Typer(help="Slides generation commands")
app.add_typer(slides_app, name="slides")


@slides_app.command("generate")
def slides_generate(
    notebook_url: Annotated[str, typer.Option("--notebook-url", "-u")],
    prompt_file: Annotated[Path, typer.Option("--prompt-file", "-p")],
    output: Annotated[Path, typer.Option("--output", "-o")],
    timeout: Annotated[
        int,
        typer.Option("--timeout", "-t", help="Generation timeout in seconds"),
    ] = 180,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Generate slides from prompt and export as PDF."""
    setup_logging(verbose)

    if not prompt_file.exists():
        console.print(f"[red]Prompt file not found:[/] {prompt_file}")
        raise typer.Exit(1)

    async def run() -> Path | None:
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return None

            notebook = NotebookManager()
            if not await notebook.open_notebook(page, notebook_url):
                console.print("[red]Failed to open notebook[/]")
                return None

            slides = SlidesManager()
            return await slides.generate_from_file(page, prompt_file, output, timeout)

    result = asyncio.run(run())
    if result:
        console.print(f"[green]Slides saved:[/] {result}")
    else:
        raise typer.Exit(1)


# --- Pipeline Command ---


@app.command()
def pipeline(
    source: Annotated[str, typer.Option("--source", "-s", help="Source URL")],
    name: Annotated[str, typer.Option("--name", "-n", help="Episode name")],
    output_dir: Annotated[
        Path,
        typer.Option("--output-dir", "-o", help="Output directory"),
    ],
    audio: Annotated[
        bool,
        typer.Option("--audio/--no-audio", help="Generate audio"),
    ] = True,
    slides_prompt: Annotated[
        Path | None,
        typer.Option("--slides-prompt", help="Slides prompt file"),
    ] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Run full pipeline: create notebook, add source, generate audio/slides."""
    setup_logging(verbose)

    output_dir.mkdir(parents=True, exist_ok=True)

    async def run() -> bool:
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return False

            # Create notebook
            console.print(f"[yellow]Creating notebook:[/] {name}")
            notebook_mgr = NotebookManager()
            notebook_url = await notebook_mgr.create_notebook(page, name)
            if not notebook_url:
                console.print("[red]Failed to create notebook[/]")
                return False
            console.print(f"[green]Notebook:[/] {notebook_url}")

            # Add source
            console.print(f"[yellow]Adding source:[/] {source}")
            sources_mgr = SourcesManager()
            await sources_mgr.add_url(page, source)
            await sources_mgr.wait_for_processing(page)
            console.print("[green]Source processed[/]")

            # Generate audio
            if audio:
                console.print("[yellow]Generating audio...[/]")
                audio_mgr = AudioManager()
                audio_path = output_dir / f"{name}.m4a"
                result = await audio_mgr.generate_and_download(page, audio_path)
                if result:
                    console.print(f"[green]Audio:[/] {result}")
                else:
                    console.print("[red]Audio generation failed[/]")

            # Generate slides
            if slides_prompt and slides_prompt.exists():
                console.print("[yellow]Generating slides...[/]")
                slides_mgr = SlidesManager()
                slides_path = output_dir / f"{name}.pdf"
                result = await slides_mgr.generate_from_file(
                    page,
                    slides_prompt,
                    slides_path,
                )
                if result:
                    console.print(f"[green]Slides:[/] {result}")
                else:
                    console.print("[red]Slides generation failed[/]")

            return True

    success = asyncio.run(run())
    if not success:
        raise typer.Exit(1)


# --- Utility Commands ---


@app.command()
def test_selectors(
    notebook_url: Annotated[
        str | None,
        typer.Option("--notebook-url", "-u"),
    ] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Test if selectors can find elements on the page."""
    setup_logging(verbose)

    async def run() -> None:
        async with browser_session() as (_, page):
            if notebook_url:
                await page.goto(notebook_url)
                await page.wait_for_load_state("networkidle")

            console.print("[bold]Testing selectors...[/]\n")

            for name, selector in Selectors.get_all().items():
                try:
                    element = await page.query_selector(selector)
                    status = "[green]FOUND[/]" if element else "[dim]not found[/]"
                except Exception as e:
                    status = f"[red]ERROR: {e}[/]"
                console.print(f"{name}: {status}")

    asyncio.run(run())


@app.command()
def config() -> None:
    """Show current configuration."""
    console.print("[bold]Configuration:[/]\n")
    console.print(f"Profile dir:    {settings.chrome_profile_dir}")
    console.print(f"Debug port:     {settings.chrome_debug_port}")
    console.print(f"Headless:       {settings.headless}")
    console.print(f"Output dir:     {settings.output_dir}")
    console.print(f"Base URL:       {settings.notebooklm_base_url}")
    console.print("\n[bold]Timeouts:[/]")
    console.print(f"Page load:      {settings.page_load_timeout}s")
    console.print(f"Source proc:    {settings.source_processing_timeout}s")
    console.print(f"Audio gen:      {settings.audio_generation_timeout}s")
    console.print(f"Slides gen:     {settings.slides_generation_timeout}s")


if __name__ == "__main__":
    app()
