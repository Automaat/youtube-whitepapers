Generate a YouTube video for episode number $ARGUMENTS.

First, find the episode name by looking for audio file matching `youtube/pl/audio/$ARGUMENTS-*.m4a` and extract the full episode name (filename without extension).

**Prerequisites (MUST exist before proceeding):**

- Audio: youtube/pl/audio/{ep_name}.m4a
- Slides PDF: youtube/pl/slides/{ep_name}.pdf
- Transcript: youtube/pl/transcripts/{ep_name}.json

**STOP immediately if any prerequisite file is missing.** Report which files are missing and do not proceed with video generation.

Tasks:

1. **Prepare slides (extracts PDF + ensures image consistency)**

   ```bash
   mise run prepare -- $ARGUMENTS
   ```

   This creates youtube/pl/slides/{ep_name}/ with:
   - thumbnail.png (scaled to match slide dimensions)
   - slide-01.png ... slide-NN.png
   - last-slide.png (scaled to match slide dimensions)

2. **Analyze transcript and slides to create timing**
   - Read each slide image to understand its content/topic
   - Search transcript for timestamps where each topic is discussed
   - Create precise slide timing that matches when topics change in the podcast
   - Map each slide to start/end timestamps based on content alignment

3. **Generate concat.txt using template**

   Use the `generate-concat` script which automatically handles intro/outro:

   ```bash
   mise run generate-concat -- $ARGUMENTS --durations slide-01:180,slide-02:150,...
   ```

   The script automatically adds:
   - 5s thumbnail intro (duplicated to avoid ffmpeg drop bug)
   - Your content slides with specified durations
   - 5s silent outro with last-slide.png

   You only provide the middle content slide durations.

4. **Verify concat.txt** (before generating video)

   ```bash
   mise run verify-concat -- $ARGUMENTS
   mise run verify-concat -- $ARGUMENTS --check-dims  # Also verify image dimensions
   ```

   This checks:
   - All referenced files exist
   - Total duration = audio + 5s (±0.5s tolerance)
   - Structure (thumbnail first, last-slide at end)
   - No very short (<3s) or very long (>180s) slides

5. **Generate video**

   ```bash
   mise run video -- $ARGUMENTS
   ```

   This runs ffmpeg and verifies output (duration + black frame detection).

6. **Create metadata file**
   - Generate Polish title and description based on transcript content
   - Include link to original paper (search for arxiv link or paper name)
   - Save to: youtube/output/{ep_name}-metadata.txt
   - Format:

     ```text
     TYTUŁ:
     [Polish title] | Deep Dive

     OPIS:
     🎙️ [Polish description of what the podcast covers]

     W tym odcinku omawiamy:
     • [Key topic 1]
     • [Key topic 2]
     • [Key topic 3]
     • [Key topic 4]
     • [Key topic 5]

     📄 Oryginalny artykuł: [arxiv URL or paper URL]

     Autorzy: [Author names] ([Institution])

     💡 Masz propozycję artykułu? Zgłoś: https://github.com/Automaat/youtube-whitepapers/issues

     TAGI:
     #AI #MachineLearning #DeepLearning #[relevant tags]
     ```

7. **Verify video** (automatic with step 5, or manual)

   ```bash
   mise run verify -- youtube/output/{ep_name}.mp4 youtube/pl/audio/{ep_name}.m4a
   ```

   If verification fails: fix concat.txt and rerun `mise run video`.

Show the final slide timing table and confirm video was generated successfully.
