Generate a YouTube video for episode [EPISODE_NUMBER]-[EPISODE_NAME].

Input files:

- Audio: milestone-papers/youtube/audio/[EPISODE_NUMBER]-[EPISODE_NAME].m4a
- Slides PDF: milestone-papers/youtube/slides/[EPISODE_NUMBER]-[EPISODE_NAME].pdf
- Transcript: milestone-papers/youtube/transcripts/[EPISODE_NUMBER]-[EPISODE_NAME].json

Tasks:

1. **Extract slides from PDF to PNG images**
   - Use pdftoppm to extract slides to milestone-papers/youtube/slides/[EPISODE_NUMBER]-[EPISODE_NAME]/
   - Resolution: 150 DPI
   - **Check file sizes**: If any PNG is ~2MB or larger, compress it:
     - Use ImageMagick: `convert input.png -quality 85 -resize 1920x1080\> output.png`
     - Or reduce colors: `pngquant --quality=70-80 --ext .png --force input.png`
   - Target: Keep each slide under 1MB for efficient processing

2. **Analyze transcript and slides to create timing**
   - Read each slide image to understand its content/topic
   - Search transcript for timestamps where each topic is discussed
   - Create precise slide timing that matches when topics change in the podcast
   - Map each slide to start/end timestamps based on content alignment

3. **Generate video with ffmpeg**
   - Create concat file with slide paths and durations
   - **5-second silent outro**: Use `milestone-papers/youtube/slides/last-slide.png` as final slide for 5s after audio ends
   - Video = audio duration + 5 seconds (last 5s silent with last-slide.png)
   - Combine slides + audio using:
     ffmpeg -y -f concat -safe 0 -i [concat_file] -i [audio] \
       -c:v libx264 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
       -pix_fmt yuv420p -c:a aac -b:a 192k [output.mp4]
   - Note: Remove `-shortest` flag to allow video to extend beyond audio
   - Output to: milestone-papers/youtube/output/[EPISODE_NUMBER]-[EPISODE_NAME].mp4

4. **Create metadata file**
   - Generate Polish title and description based on transcript content
   - Include link to original paper (search for arxiv link or paper name)
   - Save to: milestone-papers/youtube/output/[EPISODE_NUMBER]-[EPISODE_NAME]-metadata.txt
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

5. **Verify video duration**
   - Get audio duration: `ffprobe -v error -show_entries format=duration -of csv=p=0 [audio]`
   - Get video duration: `ffprobe -v error -show_entries format=duration -of csv=p=0 [output.mp4]`
   - Expected: video_duration = audio_duration + 5 seconds (±0.5s tolerance)
   - If mismatch: recalculate concat timings and regenerate video

Show the final slide timing table and confirm video was generated successfully.
