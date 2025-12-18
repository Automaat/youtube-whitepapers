# NotebookLM Automator - Implementation Plan

## 🎯 Goal

Standalone CLI tool to automate NotebookLM interactions via Playwright browser automation.

**Capabilities:**

- Add sources (URLs, PDFs)
- Generate Audio Overview (podcast) + download
- Generate Slides via prompt + export PDF

---

## 📁 Project Structure

```text
notebooklm-automator/
├── src/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point (click/typer)
│   ├── config.py           # Settings, paths, defaults
│   ├── browser.py          # Chrome CDP connection management
│   ├── selectors.py        # UI selectors (centralized, easy to update)
│   ├── notebook.py         # Create/open notebooks
│   ├── sources.py          # Add URL/PDF sources
│   ├── audio.py            # Audio overview generation + download
│   └── slides.py           # Slides generation via prompt + PDF export
├── tests/
├── pyproject.toml
├── README.md
└── .env.example
```

---

## 🔧 Tech Stack

| Component | Choice | Reason |
|-----------|--------|--------|
| Browser automation | Playwright | Async, CDP support, reliable |
| CLI framework | Typer | Simple, type hints |
| Config | pydantic-settings | Env vars + validation |
| Package manager | uv | Fast, modern |

---

## 🧩 Core Components

### 1. Browser Manager (`browser.py`)

```python
class BrowserManager:
    """Manages Chrome connection via CDP."""

    async def connect(self) -> Browser
    async def attach_to_existing(self, port: int) -> Browser
    async def launch_with_profile(self, profile_dir: str) -> Browser
    async def get_page(self) -> Page
```

**Modes:**

- Attach to existing Chrome with `--remote-debugging-port=9222`
- Launch new Chrome with persistent profile (pre-authenticated)

### 2. Selectors (`selectors.py`)

```python
SELECTORS = {
    # Notebook management
    "new_notebook_btn": 'button[aria-label="Create new notebook"]',
    "notebook_title_input": 'input[aria-label="Notebook title"]',

    # Sources
    "add_source_btn": 'button:has-text("Add source")',
    "source_url_option": 'button:has-text("Website")',
    "source_url_input": 'input[placeholder*="URL"]',
    "source_add_confirm": 'button:has-text("Insert")',

    # Audio
    "audio_overview_btn": 'button:has-text("Audio Overview")',
    "audio_generate_btn": 'button:has-text("Generate")',
    "audio_ready_indicator": '[data-testid="audio-ready"]',
    "audio_download_btn": 'button[aria-label="Download"]',

    # Slides/Chat
    "chat_input": 'textarea[placeholder*="Ask"]',
    "chat_send_btn": 'button[aria-label="Send"]',
    "export_pdf_btn": 'button:has-text("Export")',
}
```

**Note:** Selectors require manual discovery via browser DevTools. Will need updates when UI changes.

### 3. Sources Manager (`sources.py`)

```python
class SourcesManager:
    async def add_url(self, page: Page, url: str) -> bool
    async def add_pdf_url(self, page: Page, pdf_url: str) -> bool
    async def wait_for_processing(self, page: Page, timeout: int = 60) -> bool
    async def list_sources(self, page: Page) -> list[str]
```

### 4. Audio Manager (`audio.py`)

```python
class AudioManager:
    async def generate_audio_overview(self, page: Page) -> bool
    async def wait_for_completion(self, page: Page, timeout: int = 600) -> bool
    async def download_audio(self, page: Page, output_path: Path) -> Path
    async def get_audio_status(self, page: Page) -> str  # pending/generating/ready
```

**Challenges:**

- Audio generation takes 5-15 minutes
- Need polling strategy with configurable timeout
- Download interception via CDP or profile downloads folder

### 5. Slides Manager (`slides.py`)

```python
class SlidesManager:
    async def send_prompt(self, page: Page, prompt: str) -> bool
    async def wait_for_response(self, page: Page, timeout: int = 120) -> bool
    async def export_pdf(self, page: Page, output_path: Path) -> Path
```

**Flow:**

1. Paste slide generation prompt into chat
2. Wait for NotebookLM to generate slides
3. Click export → PDF
4. Intercept download

---

## 🖥️ CLI Interface

```bash
# Initialize (one-time setup)
notebooklm-automator init --profile-dir ~/.notebooklm-chrome

# Open browser for manual Google login
notebooklm-automator login

# Create notebook with source
notebooklm-automator notebook create \
  --name "GLaM Paper" \
  --source "https://arxiv.org/abs/2112.06905"

# Generate audio
notebooklm-automator audio generate \
  --notebook-url "https://notebooklm.google.com/notebook/xxx" \
  --output ./audio/15-glam.m4a

# Generate slides
notebooklm-automator slides generate \
  --notebook-url "https://notebooklm.google.com/notebook/xxx" \
  --prompt-file ./prompts/slides/15-glam.md \
  --output ./slides/15-glam.pdf

# Full pipeline
notebooklm-automator pipeline run \
  --source "https://arxiv.org/abs/2112.06905" \
  --name "15-glam" \
  --output-dir ./output \
  --audio \
  --slides-prompt ./prompts/slides/15-glam.md
```

---

## 📋 Implementation Steps

### Phase 1: Foundation

- [ ] Project setup (uv, pyproject.toml, structure)
- [ ] Browser manager with CDP connection
- [ ] Basic page navigation to NotebookLM
- [ ] Auth verification (detect logged-in state)

### Phase 2: Source Management

- [ ] Discover selectors via DevTools inspection
- [ ] Implement `add_url` flow
- [ ] Handle source processing wait
- [ ] Error handling for invalid URLs

### Phase 3: Audio Generation

- [ ] Audio overview button interaction
- [ ] Generation status polling
- [ ] Download interception/handling
- [ ] Timeout and retry logic

### Phase 4: Slides Generation

- [ ] Chat prompt submission
- [ ] Response wait strategy
- [ ] PDF export flow
- [ ] Download handling

### Phase 5: CLI & Polish

- [ ] Typer CLI with all commands
- [ ] Config file support (.env)
- [ ] Logging and progress indicators
- [ ] Error messages and troubleshooting hints

---

## ⚠️ Known Challenges

| Challenge | Solution |
|-----------|----------|
| Selectors change with UI updates | Centralized `selectors.py`, version tracking |
| Auth session expiry | Persistent Chrome profile, `login` command |
| Long audio generation (10+ min) | Configurable timeout, progress polling |
| Download interception | CDP download events or profile downloads dir |
| Rate limiting | Respectful delays between operations |
| ToS gray area | Personal use only, not for automation at scale |

---

## 🔍 Selector Discovery Process

1. Open NotebookLM in Chrome
2. DevTools → Elements → inspect target buttons/inputs
3. Find stable selectors (prefer `aria-label`, `data-testid`, `:has-text()`)
4. Test with `document.querySelector()` in console
5. Document in `selectors.py` with comments

**Priority elements to discover:**

- [ ] "Add source" button and modal
- [ ] URL input field
- [ ] "Audio Overview" section in Studio panel
- [ ] Generate/Download buttons for audio
- [ ] Chat input textarea
- [ ] Export/Download for generated content

---

## 📚 References

- [notebooklm-podcast-automator](https://github.com/israelbls/notebooklm-podcast-automator) - FastAPI + Playwright reference
- [notebooklm_source_automation](https://github.com/DataNath/notebooklm_source_automation) - Source addition patterns
- [Playwright Python docs](https://playwright.dev/python/docs/intro)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)

---

## 🚀 Next Steps

1. Create repo: `notebooklm-automator`
2. Manual selector discovery session in browser
3. Implement Phase 1 (browser connection)
4. Iterate through phases with testing
