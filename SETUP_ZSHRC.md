# Required ~/.zshrc Configuration

Add these lines to your `~/.zshrc` file:

```bash
# ============================================
# Nix (if using nix-darwin or home-manager)
# ============================================
# Usually handled by the installer, but verify you have:
if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
  . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
fi

# ============================================
# mise (for Python/Node version management)
# ============================================
eval "$(mise activate zsh)"

# ============================================
# direnv (for auto-loading environments)
# ============================================
eval "$(direnv hook zsh)"

# Optional but recommended - silence direnv logs
export DIRENV_LOG_FORMAT=""
```

## Installation Commands

If you haven't installed these tools yet:

```bash
# Install mise
curl https://mise.run | sh

# Install direnv
brew install direnv

# Nix should already be installed, but if not:
curl -L https://nixos.org/nix/install | sh
```

## After Adding to ~/.zshrc

```bash
# Reload your shell config
source ~/.zshrc

# Or start a new terminal

# Then in the project directory:
cd youtube-whitepapers
direnv allow  # One-time approval

# Now environment loads automatically!
```

## What Each Tool Does

- **Nix daemon**: Makes `nix` commands available
- **mise activate**: Manages Python/Node versions per project
- **direnv hook**: Auto-loads `.envrc` when entering directories

## Verify Everything Works

```bash
# Check all tools are available
which nix      # Should show /nix/var/nix/profiles/default/bin/nix
which mise     # Should show ~/.local/share/mise/bin/mise
which direnv   # Should show /opt/homebrew/bin/direnv or similar

# In the project directory
cd youtube-whitepapers
# Should see:
# ✅ Nix environment loaded (system tools)
# 📦 Python: ... (version info)
```

## Troubleshooting

If direnv doesn't activate:
- Make sure you ran `direnv allow` in the project directory
- Check `direnv status` for issues
- Ensure the direnv hook is AFTER mise activation in ~/.zshrc

If mise doesn't work:
- Ensure `~/.local/share/mise/bin` is in your PATH
- Run `mise doctor` to check for issues

If Nix doesn't work:
- Check that `/nix` exists
- Verify the daemon is running: `nix-daemon --version`