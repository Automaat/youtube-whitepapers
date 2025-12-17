Generate a YouTube video for episode {ep_name}.

Input files:

- Audio: youtube/pl/audio/{ep_name}.m4a
- Slides PDF: youtube/pl/slides/{ep_name}.pdf
- Transcript: youtube/pl/transcripts/{ep_name}.json

Tasks:

1. **Prepare slides (extracts PDF + ensures image consistency)**

   ```bash
   mise run prepare -- {ep_name}
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

3. **Generate video with ffmpeg**
   - Create concat.txt with **absolute paths** and durations
   - **5-second thumbnail intro**: thumbnail.png for 5s (during audio start)
   - **5-second silent outro**: last-slide.png for 5s after audio ends
   - Video = audio duration + 5 seconds
   - Get audio duration first:

     ```bash
     ffprobe -v error -show_entries format=duration -of csv=p=0 youtube/pl/audio/{ep_name}.m4a
     ```

   - Generate video (replace DURATION with audio_duration + 5):

     ```bash
     ffmpeg -y -f concat -safe 0 -i concat.txt -i youtube/pl/audio/{ep_name}.m4a \
       -c:v libx264 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
       -pix_fmt yuv420p -af "apad=pad_dur=5" -c:a aac -b:a 192k \
       -t DURATION youtube/output/{ep_name}.mp4
     ```

   - Key flags:
     - `-af "apad=pad_dur=5"`: Adds 5s silence after audio ends
     - `-t DURATION`: Ensures exact output duration

4. **Create metadata file**
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

     TAGI:
     #AI #MachineLearning #DeepLearning #[relevant tags]
     ```

5. **Verify video**

   ```bash
   mise run verify -- youtube/output/{ep_name}.mp4 youtube/pl/audio/{ep_name}.m4a
   ```

   Script checks:
   - Duration: video = audio + 5s (±0.5s tolerance)
   - No black frames in first 3 seconds (should show thumbnail)
   - No black frames in last 3 seconds (should show last-slide.png)

   If verification fails: fix concat file and regenerate video.

Show the final slide timing table and confirm video was generated successfully.
