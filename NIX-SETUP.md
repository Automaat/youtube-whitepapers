# Nix Environment Setup

## ✅ Issue Fixed

The problem was that `poppler_utils` has been renamed to `poppler-utils` in nixpkgs. This has been fixed in `flake.nix`.

## 🛠️ Current Status

All tools are now available in the Nix shell:
- ✅ ffmpeg (video processing)
- ✅ pdftoppm (PDF to PNG conversion)
- ✅ ImageMagick (convert, magick, mogrify, identify)
- ✅ jq, git, gh, mise, wget, curl, tree, fd
- ✅ ripgrep (available as `rg`)
- ✅ Python tools via mise (python3, ruff, pytest, whisper)

## 📋 Usage Options

### Option 1: Manual Activation (Current)
Enter the Nix shell manually each time:
```bash
nix develop
```

### Option 2: Automatic Activation with direnv (Recommended)

1. Install direnv globally (if not already installed):
   ```bash
   # On macOS with Homebrew:
   brew install direnv

   # Or with Nix globally:
   nix-env -iA nixpkgs.direnv
   ```

2. Add direnv hook to your shell (~/.zshrc or ~/.bashrc):
   ```bash
   # For zsh:
   echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
   source ~/.zshrc

   # For bash:
   echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. Allow direnv for this project:
   ```bash
   cd /Users/marcin.skalski@konghq.com/sideprojects/youtube-whitepapers
   direnv allow
   ```

Now the Nix environment will automatically activate when you enter the directory!

## 🚀 Verify Installation

Test that all tools work:
```bash
# Enter Nix shell
nix develop

# Test critical tools
ffmpeg -version
pdftoppm -v
convert -version
mise --version
python3 --version
```

## 📝 Notes

- The flake.lock file has been created to pin dependencies
- Python is managed by mise (as intended in your setup)
- System tools come from Nix
- The environment is reproducible across machines