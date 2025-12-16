#!/bin/bash
# Parallel transcription script for NotebookLM podcasts
# Uses whisper small model for Polish audio

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
AUDIO_DIR="$SCRIPT_DIR/audio"
OUTPUT_DIR="$SCRIPT_DIR/transcripts"
MODEL="small"
LANGUAGE="pl"
PARALLEL_JOBS="${1:-3}"

mkdir -p "$OUTPUT_DIR"

echo "🎙️ Transcription Script"
echo "========================"
echo "Audio dir: $AUDIO_DIR"
echo "Output dir: $OUTPUT_DIR"
echo "Model: $MODEL"
echo "Language: $LANGUAGE"
echo "Parallel jobs: $PARALLEL_JOBS"
echo ""

# Count audio files
FILE_COUNT=$(find "$AUDIO_DIR" -type f \( -name "*.m4a" -o -name "*.mp3" -o -name "*.wav" \) | wc -l | tr -d ' ')
echo "Found $FILE_COUNT audio files"
echo ""

# Transcribe function for xargs
transcribe_file() {
    file="$1"
    output_dir="$2"
    model="$3"
    language="$4"

    bname=$(basename "$file" | sed 's/\.[^.]*$//')
    output_file="$output_dir/${bname}.json"

    if [ -f "$output_file" ]; then
        echo "⏭️  Skip: $bname (exists)"
        return 0
    fi

    echo "🔄 Start: $bname"
    if whisper "$file" \
        --model "$model" \
        --language "$language" \
        --output_format json \
        --output_dir "$output_dir" \
        2>/dev/null; then
        echo "✅ Done: $bname"
    else
        echo "❌ Failed: $bname"
        return 1
    fi
}

export -f transcribe_file

# Run in parallel
find "$AUDIO_DIR" -type f \( -name "*.m4a" -o -name "*.mp3" -o -name "*.wav" \) | sort | \
    xargs -P "$PARALLEL_JOBS" -I {} bash -c 'transcribe_file "$1" "$2" "$3" "$4"' _ {} "$OUTPUT_DIR" "$MODEL" "$LANGUAGE"

echo ""
echo "🎉 All transcriptions complete!"
echo "Output files in: $OUTPUT_DIR"
