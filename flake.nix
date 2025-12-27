{
  description = "YouTube Whitepapers - Generate YouTube videos from NotebookLM podcasts";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        python = pkgs.python312;

        pythonEnv = python.withPackages (ps: with ps; [
          # Core dependencies
          openai-whisper
          ffmpeg-python
          pillow

          # Development dependencies
          ruff
          pytest
          pytest-mock
          pytest-cov

          # Additional useful packages
          ipython
          rich
          click
          pydantic
        ]);

      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Python environment
            pythonEnv

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
            echo "📦 Python: $(python --version)"
            echo "🎥 FFmpeg: $(ffmpeg -version | head -n 1)"
            echo "📄 Poppler: $(pdftoppm -v 2>&1 | head -n 1)"
            echo "🖼️  ImageMagick: $(convert -version | head -n 1)"
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

            # Ensure mise is configured
            if [ -f ".mise.toml" ]; then
              eval "$(mise activate zsh 2>/dev/null || true)"
            fi
          '';

          # Environment variables
          LANG = "en_US.UTF-8";
          LC_ALL = "en_US.UTF-8";

          # Whisper cache directory
          WHISPER_CACHE_DIR = "$PWD/.whisper-cache";
        };

        # Provide a package for the main scripts
        packages.default = pkgs.stdenv.mkDerivation {
          pname = "youtube-whitepapers";
          version = "0.1.0";

          src = ./.;

          buildInputs = with pkgs; [
            pythonEnv
            ffmpeg-full
            poppler_utils
            imagemagick
          ];

          installPhase = ''
            mkdir -p $out/bin $out/lib/python

            # Copy Python scripts
            cp -r scripts $out/lib/python/

            # Create wrapper scripts
            for script in prepare_slides generate_video transcribe verify_concat compress_images; do
              cat > $out/bin/$script << EOF
            #!/usr/bin/env bash
            exec ${pythonEnv}/bin/python $out/lib/python/scripts/\$script.py "\$@"
            EOF
              chmod +x $out/bin/$script
            done
          '';

          meta = with pkgs.lib; {
            description = "Generate YouTube videos from NotebookLM podcasts";
            license = licenses.mit;
            maintainers = [];
          };
        };

        # Provide individual apps
        apps = {
          prepare = flake-utils.lib.mkApp {
            drv = pkgs.writeShellScriptBin "prepare" ''
              ${pythonEnv}/bin/python scripts/prepare_slides.py "$@"
            '';
          };

          video = flake-utils.lib.mkApp {
            drv = pkgs.writeShellScriptBin "video" ''
              ${pythonEnv}/bin/python scripts/generate_video.py "$@"
            '';
          };

          transcribe = flake-utils.lib.mkApp {
            drv = pkgs.writeShellScriptBin "transcribe" ''
              ${pythonEnv}/bin/python scripts/transcribe.py "$@"
            '';
          };
        };
      });
}