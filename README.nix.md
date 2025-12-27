# Nix Development Environment

This project provides a reproducible development environment using Nix flakes.

## Prerequisites

- Nix with flakes enabled
- (Optional) direnv for automatic environment activation

### Enable Nix Flakes

Add to `~/.config/nix/nix.conf`:

```conf
experimental-features = nix-command flakes
```

## Quick Start

### Using Nix Develop (Manual)

```bash
# Enter the development shell
nix develop

# All dependencies are now available
mise run prepare -- 136
mise run video -- 28
```

### Using direnv (Automatic)

```bash
# Install direnv
brew install direnv

# Hook direnv into your shell
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc  # or bash/fish

# Allow direnv in this project
direnv allow

# Environment loads automatically when you cd into the directory
```

## Available Commands

Inside the Nix shell, all dependencies are available:

- **Python 3.12** with packages:
  - openai-whisper (transcription)
  - ffmpeg-python
  - pillow (image processing)
  - ruff (linting)
  - pytest (testing)

- **System tools:**
  - ffmpeg (video generation)
  - pdftoppm (PDF to PNG conversion)
  - imagemagick (image processing)
  - jq (JSON processing)

- **Development tools:**
  - git
  - gh (GitHub CLI)
  - mise (task runner)

## Nix Apps

You can also run specific commands directly without entering the shell:

```bash
# Run prepare slides script
nix run .#prepare -- 136

# Generate video
nix run .#video -- 28

# Transcribe audio
nix run .#transcribe
```

## First Time Setup

```bash
# Generate the lock file (requires internet)
nix flake lock

# Enter development shell
nix develop

# Initialize mise (if not already done)
mise install

# Run tests to verify setup
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

## Benefits of Nix

- **Reproducible:** Same environment across all machines
- **Isolated:** No system pollution, dependencies contained
- **Declarative:** All dependencies in one file (flake.nix)
- **Rollbackable:** Easy to revert to previous versions

## Updating Dependencies

```bash
# Update all flake inputs
nix flake update

# Update specific input
nix flake lock --update-input nixpkgs
```

## Without Nix (Alternative)

If you can't use Nix, install dependencies manually:

```bash
# macOS
brew install python@3.12 ffmpeg poppler imagemagick jq

# Python packages
pip install openai-whisper ffmpeg-python pillow ruff pytest pytest-mock
```

But Nix is recommended for consistency!