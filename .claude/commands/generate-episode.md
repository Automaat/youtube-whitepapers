Produce diagram-first episode $ARGUMENTS with the `odczyt` pipeline (docs/pipeline.md).

1. If `youtube/pl/episodes/$ARGUMENTS-*/` does not exist, run
   `uv run odczyt new $ARGUMENTS`. If no paper is found, ask for the PDF path and
   pass `--paper`.
2. Run `uv run odczyt run $ARGUMENTS` in the background and wait for it. It runs
   every stale stage and exits with code 2 at a gate or a failed check.
3. On `Gate: read review.md and script.yaml`:
   - Read `review.md`, `script.yaml` and `storyboard.yaml` of the episode.
   - Give the owner a short Polish summary: verdict, claim counts, anything
     `simplified-ok` that a viewer could misread, the skeptic questions, the
     thumbnail pick.
   - Ask for approval. Only after the owner says yes, run
     `uv run odczyt approve $ARGUMENTS script` and go back to step 2.
4. On `No ElevenLabs key`: ask the owner to run `export BW_SESSION=$(bw unlock --raw)`
   in the shell that runs the pipeline, or collect the key with the secret tool as a
   file and pass `--api-key-file <file>`. Never print the key.
5. On `Gate: watch the video, thumbnail and metadata`:
   - Show `build/thumbnail.png`, the video path and `build/metadata.txt`.
   - Ask the owner to watch the video. Only after the owner approves, run
     `uv run odczyt approve $ARGUMENTS video` and go back to step 2.
6. On any other stop: read the files the message names, explain the problem in
   Polish, and propose a fix (hand edit, `--force <stage>`, or a prompt change).
   Do not edit scene code or the script yourself unless the owner asks.
7. When the run ends with `next: mise run upload -- $ARGUMENTS`, report the LLM cost
   from the last line and stop. Uploading is the owner's call.
