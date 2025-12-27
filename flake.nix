{
  description = "YouTube Whitepapers - Generate YouTube videos from NotebookLM podcasts";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      devShells = forAllSystems (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        default = pkgs.mkShell {
          buildInputs = with pkgs; [

            # System tools
            ffmpeg-full
            poppler_utils  # provides pdftoppm
            imagemagick
            jq

            # Development tools
            git
            gh  # GitHub CLI
            mise  # Task runner

            # Shell enhancements
            zsh
            direnv

            # Additional utilities
            wget
            curl
            tree
            ripgrep
            fd
          ];

          shellHook = ''
            echo "🎬 YouTube Whitepapers Development Environment"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "🎥 FFmpeg: $(ffmpeg -version 2>/dev/null | head -n 1 || echo 'not found')"
            echo "📄 Poppler: $(pdftoppm -v 2>&1 | head -n 1 || echo 'not found')"
            echo "🖼️  ImageMagick: $(convert -version 2>/dev/null | head -n 1 || echo 'not found')"
            echo ""

            # Activate mise for Python management
            if command -v mise &> /dev/null; then
              eval "$(mise activate bash)"
              echo "📦 Python: managed by mise ($(mise current python 2>/dev/null || echo 'not configured'))"
            else
              echo "⚠️  mise not found - install it to manage Python"
            fi

            echo ""
            echo "Available commands:"
            echo "  mise run prepare -- <ep>     # Prepare slides"
            echo "  mise run video -- <ep>        # Generate video"
            echo "  mise run transcribe           # Transcribe audio"
            echo "  mise run lint                 # Run linter"
            echo "  mise run test                 # Run tests"
            echo ""

            # Set up Python path for local scripts
            export PYTHONPATH="$PWD:$PYTHONPATH"
          '';

          # Environment variables
          LANG = "en_US.UTF-8";
          LC_ALL = "en_US.UTF-8";

          # Whisper cache directory
          WHISPER_CACHE_DIR = "$PWD/.whisper-cache";
        };
      });

      # Packages section removed - Python managed by mise

      # Apps section removed - use mise run commands instead
    };
}