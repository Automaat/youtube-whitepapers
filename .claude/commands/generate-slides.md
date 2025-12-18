Generate NotebookLM slide prompts for episode number $ARGUMENTS.

First, find the episode name by looking for transcript file matching `youtube/pl/transcripts/$ARGUMENTS-*.json` and extract the full episode name (filename without extension).

**Prerequisites (MUST exist before proceeding):**

- Transcript: youtube/pl/transcripts/{ep_name}.json

**STOP immediately if transcript is missing.**

Tasks:

1. **Read the transcript file**
   - Analyze the full podcast content
   - Identify main topics and their order
   - Note specific technical terms, numbers, and results mentioned
   - Find the question asked at the end of the podcast

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
   [Extract exact question from end of podcast transcript]
   ```

3. **Content requirements**
   - Audience: technical Software Engineering experts
   - 11 slides total (slides 1-10 content, slide 11 question)
   - Each content slide: title + 4-6 detailed bullet points
   - Use original English names for technical terms, architectures, methods, and metrics
   - Include exact technical terms, specific numbers/results, key comparisons, named architectures

4. **Save output**
   - Save the complete NotebookLM prompt to: youtube/prompts/slides/{ep_name}.md

Show the generated prompt and confirm it was saved.
