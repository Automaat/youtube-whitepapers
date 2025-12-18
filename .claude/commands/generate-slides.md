Generate NotebookLM slide prompts for episode number $ARGUMENTS.

**Prerequisites (MUST exist before proceeding):**

- Transcript: youtube/pl/transcripts/{ep_num}-*.json

**CRITICAL: DO NOT read transcript JSON directly - use only analysis output.**

**STOP immediately if transcript is missing.**

Tasks:

1. **Run transcript analysis**
   - Execute: `mise run analyze-transcript -- $ARGUMENTS`
   - Review the printed analysis showing:
     - Episode name, duration, segment count
     - Final question extracted from podcast
     - Technical terms (sorted by frequency)
     - Suggested 10-slide outline with timestamps and sample text
   - Use this structured data to guide prompt creation

2. **Create NotebookLM prompt**

   Generate a complete prompt with this structure:

   ```text
   Generate 11 presentation slides based on the podcast about [PAPER NAME].

   ## Visual Style
   - Minimal, clean design with dark blue headers
   - White/light gray background
   - Sans-serif typography throughout
   - Simple outline icons only (no stock photos, no AI-generated images)
   - Consistent layout: title at top, bullets left-aligned
   - Same spacing and margins across all slides
   - Use diagrams/flowcharts for technical concepts where appropriate

   ---

   ## Slide 1: [Title matching first topic]
   - [detailed technical point 1]
   - [detailed technical point 2]
   - [detailed technical point 3]
   - [detailed technical point 4]

   ## Slide 2-10: [Topic titles]
   (each slide: title + 4-6 detailed bullet points)

   ## Slide 11: Question for You
   [Single question translated from analysis output to English]
   ```

3. **Content requirements**
   - **Language: ENGLISH** - all slide titles, bullets, and question must be in English (translate from Polish transcript)
   - Audience: technical Software Engineering experts
   - 11 slides total (slides 1-10 content, slide 11 single question only)
   - Each content slide (1-10): title + 4-6 detailed bullet points
   - Slide 11: title "Question for You" + single question (no bullets)
   - Use technical terms from analysis output (already sorted by frequency)
   - Include exact technical terms, specific numbers/results, key comparisons, named architectures
   - Base content on suggested outline with sample text from analysis output

4. **Save output**
   - Save the complete NotebookLM prompt to: youtube/prompts/slides/{ep_name}.md

Show the generated prompt and confirm it was saved.
