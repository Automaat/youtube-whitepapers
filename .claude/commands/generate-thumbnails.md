# Generate Thumbnail Prompts

Generate thumbnail prompts for papers that need them.

## Process

1. Run `mise status` to get JSON with all papers
2. Read `youtube/config.json` to get cape color for category
3. For each paper without a thumbnail prompt:
   - Search online for paper summary/key concepts
   - Create thumbnail prompt in Dandadan anime style
   - Save to `youtube/prompts/thumbnails/{episode}-{paper-name}-thumbnail.md`

## Thumbnail Prompt Template

```text
Create a YouTube thumbnail (16:9 aspect ratio) in Dandadan anime style.
Use the uploaded dog photo as reference - transform into anime style with
superhero {cape_color} tech cape and futuristic visor.
White background. The dog {visual_scene_description}.
Write the text "{text}" in bold, {text_color}, angular anime font in upper left.
{pose_description}, bold linework. No clutter.
```

**Text:** {text} | **Color:** {text_color}

## Rules

- ALWAYS search online for paper summary before creating prompt
- Visual scene must relate to paper's core concept
- Text should be short, punchy, paper-specific (not generic)
- Text color should complement visual theme
- Pose/energy should match paper's significance/mood
- NO placeholders - complete, specific descriptions only

## Examples

**Shannon's Secrecy Systems:**
- Visual: Guards glowing vault of encrypted messages, entropy symbols swirling
- Text: "PERFECT SECRECY" (Deep Purple)
- Energy: Cryptography guardian pose, information theory energy

**RFC 1 - Host Software:**
- Visual: Internet pioneer holds first RFC document glowing with historic significance
- Text: "RFC 1" (ARPANET Green)
- Energy: Pioneer pose, historic moment energy

## Output

For each paper, create file with:
1. Prompt block with specific visual description
2. Text and color specification
3. Ensure cape color matches category from config.json
