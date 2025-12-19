"""CLI entry point using Typer."""

from __future__ import annotations

import asyncio
import importlib.util
import json
import logging
import re
import shutil
import tempfile

from pathlib import Path
from typing import Annotated, Any

import typer

from rich.console import Console
from rich.logging import RichHandler

from src.audio import AudioManager, AudioStatus
from src.browser import BrowserManager, browser_session
from src.config import settings
from src.notebook import NotebookManager
from src.slides import SlidesManager, SlidesStatus
from src.sources import SourcesManager
from src.ui_selectors import Selectors


WHITEPAPERS_DIR = Path(__file__).parent.parent.parent / "whitepapers"
STATUS_FILE = WHITEPAPERS_DIR / "status.json"


def _get_status_utils() -> Any:
    """Lazy load status_utils module from parent project."""
    if not hasattr(_get_status_utils, "cached_module"):
        module_path = Path(__file__).parent.parent.parent / "scripts" / "status_utils.py"
        spec = importlib.util.spec_from_file_location("status_utils", module_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            _get_status_utils.cached_module = module
    return getattr(_get_status_utils, "cached_module", None)


def find_paper_pdf(episode: str) -> tuple[Path, str] | None:
    """Find PDF for episode number. Returns (pdf_path, name) or None."""
    ep_str = episode.zfill(2)

    if not STATUS_FILE.exists():
        return None

    status = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    for paper in status.get("papers", []):
        if paper.get("episode") == ep_str:
            name = paper.get("name", "")
            category = paper.get("category", "")
            if name and category:
                pdf_path = WHITEPAPERS_DIR / category / f"{ep_str}-{name}.pdf"
                if pdf_path.exists():
                    return pdf_path, name
    return None


def update_notebook_status(episode: str, notebook_url: str) -> None:
    """Update status.json with notebook_created and notebook_url."""
    utils = _get_status_utils()
    utils.update_episode_status(episode, "notebook_created", value=True)
    utils.update_episode_field(episode, "notebook_url", notebook_url)


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
    timeout: Annotated[
        int,
        typer.Option("--timeout", "-t", help="Login timeout in seconds"),
    ] = 300,
    fresh: Annotated[
        bool,
        typer.Option("--fresh", help="Use temporary profile (for testing)"),
    ] = False,
) -> None:
    """Launch browser for manual Google login."""
    setup_logging()

    console.print("[yellow]Launching browser...[/]")
    console.print("\n[bold]Please sign in to your Google account in the browser.[/]")
    console.print(f"[dim]Timeout: {timeout}s[/]\n")

    async def do_login() -> bool:
        manager = BrowserManager()
        if fresh:
            temp_dir = Path(tempfile.mkdtemp(prefix="notebooklm-"))
            console.print(f"[dim]Using temp profile: {temp_dir}[/]")
            await manager.launch_with_profile(profile_dir=temp_dir, headless=False)
        else:
            await manager.launch_with_profile(headless=False)
        page = await manager.navigate_to_notebooklm()
        result = await manager.wait_for_login(page, timeout)
        await manager.close()
        return result

    success = asyncio.run(do_login())

    if success:
        console.print("[green]Login successful![/]")
    else:
        console.print("[red]Login timeout or failed[/]")
        raise typer.Exit(1)


@app.command()
def logout(
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Skip confirmation prompt"),
    ] = False,
    profile_dir: Annotated[
        Path | None,
        typer.Option("--profile-dir", "-p", help="Chrome profile directory"),
    ] = None,
) -> None:
    """Logout by removing browser profile directory."""
    profile = profile_dir or settings.chrome_profile_dir

    if not profile.exists():
        console.print(f"[yellow]Profile directory not found:[/] {profile}")
        return

    if not force:
        confirm = typer.confirm(f"Remove browser profile at {profile}?")
        if not confirm:
            console.print("[dim]Cancelled[/]")
            raise typer.Exit(0)

    shutil.rmtree(profile)
    console.print(f"[green]Logged out.[/] Removed: {profile}")
    console.print("[dim]Run 'login' to authenticate again.[/]")


# --- Notebook Commands ---

notebook_app = typer.Typer(help="Notebook management commands")
app.add_typer(notebook_app, name="notebook")


def _resolve_notebook_inputs(
    episode: str,
    name: str | None,
    source: str | None,
    file: Path | None,
) -> tuple[str, Path | None]:
    """Resolve notebook name and PDF file from inputs. Exits on error."""
    notebook_name = name
    pdf_file = file

    if not source and not file:
        result = find_paper_pdf(episode)
        if not result:
            console.print(f"[red]Episode {episode} not found in status.json or PDF missing[/]")
            raise typer.Exit(1)
        pdf_file, paper_name = result
        console.print(f"[dim]Found: {pdf_file}[/]")
        notebook_name = notebook_name or f"{episode.zfill(2)} {paper_name}"

    if not notebook_name:
        console.print("[red]--name required when using --source or --file[/]")
        raise typer.Exit(1)

    if pdf_file and not pdf_file.exists():
        console.print(f"[red]File not found:[/] {pdf_file}")
        raise typer.Exit(1)

    return notebook_name, pdf_file


@notebook_app.command("create")
def notebook_create(
    episode: Annotated[str, typer.Argument(help="Episode number or 'all' for batch creation")],
    name: Annotated[
        str | None,
        typer.Option("--name", "-n", help="Notebook name (default: from status.json)"),
    ] = None,
    source: Annotated[
        str | None,
        typer.Option("--source", "-s", help="Source URL (overrides auto PDF)"),
    ] = None,
    file: Annotated[
        Path | None,
        typer.Option("--file", "-f", help="Local file (overrides auto PDF)"),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Preview without creating (only for 'all')"),
    ] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Create notebook from episode number or 'all' for batch creation."""
    setup_logging(verbose)

    if episode.lower() == "all":
        _notebook_create_all(dry_run)
        return

    notebook_name, pdf_file = _resolve_notebook_inputs(episode, name, source, file)

    async def run() -> str | None:
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return None

            notebook = NotebookManager()
            url = await notebook.create_notebook(page, notebook_name)

            if url:
                sources = SourcesManager()
                if pdf_file:
                    await sources.add_file(page, pdf_file)
                    await sources.wait_for_processing(page)
                elif source:
                    await sources.add_url(page, source)
                    await sources.wait_for_processing(page)

            return url

    url = asyncio.run(run())
    if url:
        console.print(f"[green]Notebook created:[/] {url}")
        update_notebook_status(episode, url)
        console.print(f"[green]Status updated for episode {episode}[/]")
    else:
        raise typer.Exit(1)


def _notebook_create_all(dry_run: bool) -> None:
    """Create notebooks for all papers missing notebooks."""
    papers = _get_papers_missing_notebooks()
    if not papers:
        console.print("[yellow]No papers missing notebooks[/]")
        return

    console.print(f"[bold]Found {len(papers)} papers missing notebooks[/]")

    if dry_run:
        for paper in papers:
            ep = paper.get("episode", "??")
            name = paper.get("name", "unknown")
            category = paper.get("category", "")
            pdf_path = WHITEPAPERS_DIR / category / f"{ep.zfill(2)}-{name}.pdf"
            console.print(f"  {ep}-{name}")
            console.print(f"    [dim]PDF: {pdf_path}[/]")
        return

    created = 0
    failed = 0

    async def run() -> tuple[int, int]:
        nonlocal created, failed
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return (0, len(papers))

            notebook_mgr = NotebookManager()
            sources_mgr = SourcesManager()

            for paper in papers:
                ep = paper.get("episode", "??")
                name = paper.get("name", "unknown")
                category = paper.get("category", "")
                pdf_path = WHITEPAPERS_DIR / category / f"{ep.zfill(2)}-{name}.pdf"
                notebook_name = f"{ep.zfill(2)} {name}"

                console.print(f"[bold]Creating {ep}-{name}...[/]")

                url = await notebook_mgr.create_notebook(page, notebook_name)
                if not url:
                    console.print("  [red]Failed to create notebook[/]")
                    failed += 1
                    continue

                await sources_mgr.add_file(page, pdf_path)
                await sources_mgr.wait_for_processing(page)

                update_notebook_status(ep, url)
                console.print(f"  [green]Created:[/] {url}")
                created += 1

        return (created, failed)

    created, failed = asyncio.run(run())
    console.print(f"\n[bold]Summary:[/] {created} created, {failed} failed")


def _extract_episode_from_name(name: str) -> str | None:
    """Extract episode number from notebook name like '72-viewstamped' or '65 generals'."""
    match = re.match(r"^(\d+)[\s\-]", name)
    return match.group(1) if match else None


@notebook_app.command("list")
def notebook_list(
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
    sync: Annotated[bool, typer.Option("--sync", "-s", help="Update status.json with notebook URLs")] = False,
) -> None:
    """List all notebooks. Use --sync to update status.json."""
    setup_logging(verbose)

    async def run() -> list[dict[str, str]]:
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return []

            notebook = NotebookManager()
            return await notebook.list_notebooks(page)

    notebooks = asyncio.run(run())
    updated = 0
    skipped_archived = 0

    # Load status once to check archived
    utils = _get_status_utils()
    status = utils.load_status()
    papers = status.get("papers", [])

    for nb in notebooks:
        console.print(f"[bold]{nb['name']}[/]")
        console.print(f"  [dim]{nb['url']}[/]")

        if sync:
            episode = _extract_episode_from_name(nb["name"])
            if episode:
                paper = utils.find_paper_by_episode(papers, episode)
                if not paper:
                    continue
                if paper.get("archived"):
                    skipped_archived += 1
                    continue
                update_notebook_status(episode, nb["url"])
                updated += 1

    if sync:
        msg = f"\n[green]Updated {updated} episodes in status.json[/]"
        if skipped_archived:
            msg += f" [dim](skipped {skipped_archived} archived)[/]"
        console.print(msg)


# --- Audio Commands ---

audio_app = typer.Typer(help="Audio Overview commands")
app.add_typer(audio_app, name="audio")


PROMPT_FILE = (
    Path(__file__).parent.parent.parent / "youtube/prompts/generate-podcast.md"
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

    async def run() -> AudioStatus:
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return AudioStatus.ERROR

            notebook = NotebookManager()
            if not await notebook.open_notebook(page, notebook_url):
                console.print("[red]Failed to open notebook[/]")
                return AudioStatus.ERROR

            audio = AudioManager()
            return await audio.generate(page, prompt=prompt, language=language)

    result = asyncio.run(run())
    if result == AudioStatus.LIMIT_REACHED:
        console.print("[yellow]Daily audio generation limit reached[/]")
        raise typer.Exit(1)
    if result in (AudioStatus.GENERATING, AudioStatus.READY):
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


# --- Audio Download Sub-Commands ---

audio_download_app = typer.Typer(help="Audio download commands")
audio_app.add_typer(audio_download_app, name="download")


@audio_download_app.command("single")
def audio_download_single(
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


AUDIO_OUTPUT_DIR = Path(__file__).parent.parent.parent / "youtube" / "pl" / "audio"


def _get_audio_output_path(episode: str, name: str) -> Path:
    """Get output path for audio file."""
    return AUDIO_OUTPUT_DIR / f"{episode.zfill(2)}-{name}.m4a"


def _get_papers_missing_audio() -> list[dict[str, Any]]:
    """Get papers from status.json that need audio download (audio_scheduled but no audio)."""
    if not STATUS_FILE.exists():
        return []
    status = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    papers = []
    for paper in status.get("papers", []):
        if paper.get("archived"):
            continue
        if paper.get("audio"):
            continue
        if not paper.get("audio_scheduled"):
            continue
        if not paper.get("notebook_url"):
            continue
        papers.append(paper)
    return papers


def _get_papers_needing_audio_schedule() -> list[dict[str, Any]]:
    """Get papers that need audio generation scheduled."""
    if not STATUS_FILE.exists():
        return []
    status = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    papers = []
    for paper in status.get("papers", []):
        if paper.get("archived"):
            continue
        if not paper.get("notebook_created"):
            continue
        if paper.get("audio_scheduled"):
            continue
        if paper.get("audio"):
            continue
        if not paper.get("notebook_url"):
            continue
        papers.append(paper)
    return papers


def _get_papers_missing_notebooks() -> list[dict[str, Any]]:
    """Get papers from status.json that need notebook creation."""
    if not STATUS_FILE.exists():
        return []
    status = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    papers = []
    for paper in status.get("papers", []):
        if paper.get("archived"):
            continue
        if paper.get("notebook_created"):
            continue
        ep = paper.get("episode", "").zfill(2)
        name = paper.get("name", "")
        category = paper.get("category", "")
        if not (ep and name and category):
            continue
        pdf_path = WHITEPAPERS_DIR / category / f"{ep}-{name}.pdf"
        if not pdf_path.exists():
            continue
        papers.append(paper)
    return papers


@audio_download_app.command("all")
def audio_download_all(
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", "-n", help="Preview without downloading"),
    ] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Download ready audio for all episodes missing audio."""
    setup_logging(verbose)

    papers = _get_papers_missing_audio()
    if not papers:
        console.print("[yellow]No episodes missing audio[/]")
        return

    console.print(f"[bold]Found {len(papers)} episodes missing audio[/]")

    if dry_run:
        for paper in papers:
            ep = paper.get("episode", "??")
            name = paper.get("name", "unknown")
            url = paper.get("notebook_url", "")
            output = _get_audio_output_path(ep, name)
            console.print(f"  {ep}-{name}")
            console.print(f"    [dim]URL: {url}[/]")
            console.print(f"    [dim]Output: {output}[/]")
        return

    downloaded = 0
    skipped = 0
    failed = 0

    async def run() -> tuple[int, int, int]:
        nonlocal downloaded, skipped, failed
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return (0, 0, len(papers))

            notebook_mgr = NotebookManager()
            audio_mgr = AudioManager()
            utils = _get_status_utils()

            for paper in papers:
                ep = paper.get("episode", "??")
                name = paper.get("name", "unknown")
                url = paper.get("notebook_url", "")

                console.print(f"[bold]Processing {ep}-{name}...[/]")

                if not await notebook_mgr.open_notebook(page, url):
                    console.print("  [red]Failed to open notebook[/]")
                    failed += 1
                    continue

                status = await audio_mgr.get_status(page)
                if status != AudioStatus.READY:
                    console.print(f"  [yellow]Audio not ready ({status.value}), skipping[/]")
                    skipped += 1
                    continue

                output = _get_audio_output_path(ep, name)
                result = await audio_mgr.download(page, output)
                if result:
                    size_mb = result.stat().st_size / (1024 * 1024)
                    console.print(f"  [green]Downloaded: {result} ({size_mb:.1f} MB)[/]")
                    utils.update_episode_status(ep, "audio", value=True)
                    downloaded += 1
                else:
                    console.print("  [red]Download failed[/]")
                    failed += 1

        return (downloaded, skipped, failed)

    downloaded, skipped, failed = asyncio.run(run())
    console.print(f"\n[bold]Summary:[/] {downloaded} downloaded, {skipped} skipped, {failed} failed")


async def _schedule_audio_for_papers(
    papers: list[dict[str, Any]], prompt: str
) -> tuple[int, int, int, bool]:
    """Schedule audio generation for papers."""
    scheduled = 0
    skipped = 0
    failed = 0
    limit_reached = False

    async with browser_session() as (manager, page):
        if not await manager.is_logged_in(page):
            console.print("[red]Not logged in. Run 'login' first.[/]")
            return (0, 0, len(papers), False)

        notebook_mgr = NotebookManager()
        audio_mgr = AudioManager()
        utils = _get_status_utils()

        for paper in papers:
            ep = paper.get("episode", "??")
            name = paper.get("name", "unknown")
            url = paper.get("notebook_url", "")

            console.print(f"[bold]Processing {ep}-{name}...[/]")

            if not await notebook_mgr.open_notebook(page, url):
                console.print("  [red]Failed to open notebook[/]")
                failed += 1
                continue

            status = await audio_mgr.get_status(page)
            if status in (AudioStatus.READY, AudioStatus.GENERATING):
                console.print(f"  [yellow]Audio already {status.value}[/]")
                skipped += 1
                continue
            if status == AudioStatus.LIMIT_REACHED:
                console.print("  [yellow]Limit already reached[/]")
                limit_reached = True
                break

            result = await audio_mgr.generate(page, prompt=prompt, language="Polish")
            if result == AudioStatus.LIMIT_REACHED:
                console.print("  [red]Limit reached after Generate click, stopping[/]")
                limit_reached = True
                break
            if result in (AudioStatus.GENERATING, AudioStatus.READY):
                console.print("  [green]Audio scheduled[/]")
                utils.update_episode_status(ep, "audio_scheduled", value=True)
                scheduled += 1
            else:
                console.print("  [red]Generation failed, stopping[/]")
                failed += 1
                break

    return (scheduled, skipped, failed, limit_reached)


@audio_app.command("schedule")
def audio_schedule(
    episode: Annotated[
        str | None,
        typer.Option("--episode", "-e", help="Single episode number to schedule"),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", "-n", help="Preview without scheduling"),
    ] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Schedule audio generation for papers with notebooks but no audio."""
    setup_logging(verbose)

    papers = _get_papers_needing_audio_schedule()
    if episode:
        ep_str = episode.zfill(2)
        papers = [p for p in papers if p.get("episode") == ep_str]
    if not papers:
        console.print("[yellow]No papers needing audio scheduling[/]")
        return

    console.print(f"[bold]Found {len(papers)} papers to schedule[/]")

    if not PROMPT_FILE.exists():
        console.print(f"[red]Prompt file not found:[/] {PROMPT_FILE}")
        raise typer.Exit(1)
    prompt = PROMPT_FILE.read_text().strip()

    if dry_run:
        for paper in papers:
            ep = paper.get("episode", "??")
            name = paper.get("name", "unknown")
            url = paper.get("notebook_url", "")
            console.print(f"  {ep}-{name}")
            console.print(f"    [dim]URL: {url}[/]")
        return

    scheduled, skipped, failed, limit_reached = asyncio.run(
        _schedule_audio_for_papers(papers, prompt)
    )
    console.print(
        f"\n[bold]Summary:[/] {scheduled} scheduled, {skipped} skipped, {failed} failed"
    )
    if limit_reached:
        console.print("[yellow]Stopped: daily audio generation limit reached[/]")


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


SLIDES_OUTPUT_DIR = Path(__file__).parent.parent.parent / "youtube" / "pl" / "slides"


def _get_slides_output_path(episode: str, name: str) -> Path:
    """Get output path for slides PDF."""
    return SLIDES_OUTPUT_DIR / f"{episode.zfill(2)}-{name}.pdf"


def _get_papers_needing_slides() -> list[dict[str, Any]]:
    """Get papers that have audio but no slides."""
    if not STATUS_FILE.exists():
        return []
    status = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    papers = []
    for paper in status.get("papers", []):
        if paper.get("archived"):
            continue
        if paper.get("slides"):
            continue
        if not paper.get("audio"):
            continue
        if not paper.get("notebook_url"):
            continue
        papers.append(paper)
    return papers


SLIDES_PROMPTS_DIR = Path(__file__).parent.parent.parent / "youtube" / "prompts" / "slides"


def _get_slides_prompt_path(episode: str, name: str) -> Path:
    """Get path to slides prompt file."""
    return SLIDES_PROMPTS_DIR / f"{episode.zfill(2)}-{name}.md"


def _get_papers_needing_slides_schedule() -> list[dict[str, Any]]:
    """Get papers that need slides generation scheduled."""
    if not STATUS_FILE.exists():
        return []
    status = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    papers = []
    for paper in status.get("papers", []):
        if paper.get("archived"):
            continue
        if not paper.get("notebook_created"):
            continue
        if paper.get("slides_scheduled"):
            continue
        if paper.get("slides"):
            continue
        if not paper.get("notebook_url"):
            continue
        ep = paper.get("episode", "").zfill(2)
        name = paper.get("name", "")
        if not (ep and name):
            continue
        prompt_path = _get_slides_prompt_path(ep, name)
        if not prompt_path.exists():
            continue
        papers.append(paper)
    return papers


@slides_app.command("download")
def slides_download(
    notebook_url: Annotated[str, typer.Option("--notebook-url", "-u")],
    output: Annotated[Path, typer.Option("--output", "-o")],
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Download generated slides as PDF."""
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

            slides = SlidesManager()
            return await slides.download(page, output)

    result = asyncio.run(run())
    if result:
        console.print(f"[green]Slides saved:[/] {result}")
    else:
        raise typer.Exit(1)


@slides_app.command("batch-download")
def slides_batch_download(
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", "-n", help="Preview without downloading"),
    ] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Download slides for all episodes with audio but no slides."""
    setup_logging(verbose)

    papers = _get_papers_needing_slides()
    if not papers:
        console.print("[yellow]No episodes needing slides download[/]")
        return

    console.print(f"[bold]Found {len(papers)} episodes needing slides[/]")

    if dry_run:
        for paper in papers:
            ep = paper.get("episode", "??")
            name = paper.get("name", "unknown")
            url = paper.get("notebook_url", "")
            output = _get_slides_output_path(ep, name)
            console.print(f"  {ep}-{name}")
            console.print(f"    [dim]URL: {url}[/]")
            console.print(f"    [dim]Output: {output}[/]")
        return

    downloaded = 0
    skipped = 0
    failed = 0

    async def run() -> tuple[int, int, int]:
        nonlocal downloaded, skipped, failed
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return (0, 0, len(papers))

            notebook_mgr = NotebookManager()
            slides_mgr = SlidesManager()
            utils = _get_status_utils()

            for paper in papers:
                ep = paper.get("episode", "??")
                name = paper.get("name", "unknown")
                url = paper.get("notebook_url", "")

                console.print(f"[bold]Processing {ep}-{name}...[/]")

                if not await notebook_mgr.open_notebook(page, url):
                    console.print("  [red]Failed to open notebook[/]")
                    failed += 1
                    continue

                status = await slides_mgr.get_status(page)
                if status != SlidesStatus.READY:
                    console.print(f"  [yellow]Slides not ready ({status.value}), skipping[/]")
                    skipped += 1
                    continue

                output = _get_slides_output_path(ep, name)
                result = await slides_mgr.download(page, output)
                if result:
                    size_kb = result.stat().st_size / 1024
                    console.print(f"  [green]Downloaded: {result} ({size_kb:.1f} KB)[/]")
                    utils.update_episode_status(ep, "slides", value=True)
                    downloaded += 1
                else:
                    console.print("  [red]Download failed[/]")
                    failed += 1

        return (downloaded, skipped, failed)

    downloaded, skipped, failed = asyncio.run(run())
    console.print(f"\n[bold]Summary:[/] {downloaded} downloaded, {skipped} skipped, {failed} failed")


async def _schedule_slides_for_papers(
    papers: list[dict[str, Any]],
) -> tuple[int, int, int, bool]:
    """Schedule slides generation for papers."""
    scheduled = 0
    skipped = 0
    failed = 0
    limit_reached = False

    async with browser_session() as (manager, page):
        if not await manager.is_logged_in(page):
            console.print("[red]Not logged in. Run 'login' first.[/]")
            return (0, 0, len(papers), False)

        notebook_mgr = NotebookManager()
        slides_mgr = SlidesManager()
        utils = _get_status_utils()

        for paper in papers:
            ep = paper.get("episode", "??")
            name = paper.get("name", "unknown")
            url = paper.get("notebook_url", "")

            console.print(f"[bold]Processing {ep}-{name}...[/]")

            prompt_path = _get_slides_prompt_path(ep, name)
            if not prompt_path.exists():
                console.print(f"  [yellow]No prompt file: {prompt_path}[/]")
                skipped += 1
                continue

            if not await notebook_mgr.open_notebook(page, url):
                console.print("  [red]Failed to open notebook[/]")
                failed += 1
                continue

            status = await slides_mgr.get_status(page)
            if status == SlidesStatus.READY:
                console.print("  [yellow]Slides already ready[/]")
                skipped += 1
                continue
            if status == SlidesStatus.LIMIT_REACHED:
                console.print("  [red]Generation limit reached, stopping[/]")
                limit_reached = True
                break

            prompt = prompt_path.read_text().strip()
            if not await slides_mgr.send_prompt(page, prompt):
                console.print("  [red]Limit reached after Generate click, stopping[/]")
                limit_reached = True
                break

            console.print("  [green]Slides scheduled[/]")
            utils.update_episode_status(ep, "slides_scheduled", value=True)
            scheduled += 1

    return (scheduled, skipped, failed, limit_reached)


@slides_app.command("schedule")
def slides_schedule(
    episode: Annotated[
        str | None,
        typer.Option("--episode", "-e", help="Single episode number to schedule"),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", "-n", help="Preview without scheduling"),
    ] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Schedule slides generation for papers with notebooks and prompt files."""
    setup_logging(verbose)

    papers = _get_papers_needing_slides_schedule()
    if episode:
        ep_str = episode.zfill(2)
        papers = [p for p in papers if p.get("episode") == ep_str]
    if not papers:
        console.print("[yellow]No papers needing slides scheduling[/]")
        return

    console.print(f"[bold]Found {len(papers)} papers to schedule[/]")

    if dry_run:
        for paper in papers:
            ep = paper.get("episode", "??")
            name = paper.get("name", "unknown")
            url = paper.get("notebook_url", "")
            prompt_path = _get_slides_prompt_path(ep, name)
            console.print(f"  {ep}-{name}")
            console.print(f"    [dim]URL: {url}[/]")
            console.print(f"    [dim]Prompt: {prompt_path}[/]")
        return

    scheduled, skipped, failed, limit_reached = asyncio.run(
        _schedule_slides_for_papers(papers)
    )
    console.print(
        f"\n[bold]Summary:[/] {scheduled} scheduled, {skipped} skipped, {failed} failed"
    )
    if limit_reached:
        console.print("[yellow]Stopped: generation limit reached or error[/]")


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
    episode: Annotated[
        str | None,
        typer.Option("--episode", "-e", help="Episode number to update status"),
    ] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Run full pipeline: create notebook, add source, generate audio/slides."""
    setup_logging(verbose)

    output_dir.mkdir(parents=True, exist_ok=True)

    async def run() -> str | None:
        async with browser_session() as (manager, page):
            if not await manager.is_logged_in(page):
                console.print("[red]Not logged in. Run 'login' first.[/]")
                return None

            # Create notebook
            console.print(f"[yellow]Creating notebook:[/] {name}")
            notebook_mgr = NotebookManager()
            notebook_url = await notebook_mgr.create_notebook(page, name)
            if not notebook_url:
                console.print("[red]Failed to create notebook[/]")
                return None
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

            return notebook_url

    notebook_url = asyncio.run(run())
    if notebook_url:
        if episode:
            update_notebook_status(episode, notebook_url)
            console.print(f"[green]Status updated for episode {episode}[/]")
    else:
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
