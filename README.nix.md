# Nix Development Environment

This project uses:
- **Nix** for system tools (ffmpeg, poppler, imagemagick, etc.)
- **mise** for Python version management

## Prerequisites

- Nix with flakes enabled
- mise for Python management
- (Optional) direnv for automatic environment activation

### Enable Nix Flakes

Add to `~/.config/nix/nix.conf`:

```conf
experimental-features = nix-command flakes
```

## Quick Start

### 1. Install mise and Python

```bash
# Install mise (if not already installed)
curl https://mise.run | sh

# Install Python via mise
mise install

# Create Python virtual environment
python -m venv .venv
source .venv/bin/activate  # or use direnv to auto-activate

# Install Python dependencies
pip install -r requirements.txt  # or your preferred method
```

### 2. Enter Nix Shell for System Tools

```bash
# Enter the development shell (provides system tools)
nix develop

# Now all system tools are available
mise run prepare -- 136
mise run video -- 28
```

### Using direnv (Automatic - Recommended)

```bash
# Install direnv
brew install direnv

# Hook direnv into your shell
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc  # or bash/fish

# Allow direnv in this project
direnv allow

# Environment loads automatically when you cd into the directory
# This will:
# - Load Nix system tools
# - Activate mise Python
# - Activate Python venv if present
```

## Division of Responsibilities

### Python (managed by mise)
- Python interpreter version
- pip packages:
  - openai-whisper (transcription)
  - ffmpeg-python
  - pillow (image processing)
  - ruff (linting)
  - pytest (testing)

### System Tools (provided by Nix)
- **ffmpeg** - Video generation
- **poppler_utils** (pdftoppm) - PDF to PNG conversion
- **imagemagick** - Image processing
- **jq** - JSON processing
- **git** - Version control
- **gh** - GitHub CLI
- **mise** - Task runner and Python version manager

## Using the Tools

All commands should be run through mise after entering the Nix shell:

```bash
# Enter Nix shell (or use direnv)
nix develop

# Then use mise commands
mise run prepare -- 136
mise run video -- 28
mise run transcribe
```

## First Time Setup

```bash
# 1. Generate Nix lock file (requires internet)
nix flake lock

# 2. Install mise if not already installed
curl https://mise.run | sh

# 3. Configure Python via mise
mise install

# 4. Enter development shell
nix develop

# 5. Create Python virtual environment
python -m venv .venv
source .venv/bin/activate

# 6. Install Python dependencies
pip install openai-whisper ffmpeg-python pillow ruff pytest pytest-mock

# 7. Run tests to verify setup
mise run test
```

## Troubleshooting

### Network Issues

If `nix flake lock` fails with network errors:

1. Check your internet connection
2. Try using a different DNS server
3. Use `--offline` flag if you have cached dependencies

### Missing Tools

All required tools are provided by Nix. If something is missing:

1. Ensure you're in the Nix shell (`nix develop`)
2. Check that flake.nix includes the dependency
3. Run `nix flake update` to get latest packages

### direnv Not Loading

If direnv doesn't activate automatically:

```bash
# Reload direnv
direnv reload

# Check direnv status
direnv status

# Re-allow if needed
direnv allow
```

## Benefits of This Hybrid Approach

### Nix for System Tools
- **Reproducible:** Same ffmpeg, poppler, imagemagick versions everywhere
- **Isolated:** No system pollution with brew packages
- **Declarative:** System deps in flake.nix
- **Complex tools:** Handles tools with many system dependencies

### mise for Python
- **Flexibility:** Easy Python version switching
- **Standard workflow:** Use pip/venv as normal
- **Project-specific:** .mise.toml defines Python version
- **Fast iteration:** No Nix rebuilds for Python changes

## Updating Dependencies

```bash
# Update all flake inputs
nix flake update

# Update specific input
nix flake lock --update-input nixpkgs
```

## Without Nix (Alternative)

If you can't use Nix, install system tools manually:

```bash
# macOS - system tools only
brew install ffmpeg poppler imagemagick jq

# Python still managed by mise
mise install
python -m venv .venv
source .venv/bin/activate
pip install openai-whisper ffmpeg-python pillow ruff pytest pytest-mock
```

Note: Using Nix ensures everyone has the exact same versions of system tools!