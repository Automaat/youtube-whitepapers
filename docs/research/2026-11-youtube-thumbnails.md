# Research: YouTube thumbnails for Głęboki Odczyt

Date: 2026-11-20. Goal: decide what thumbnails the channel should use once it moves to
diagram-first videos (`docs/design/visual-style.md`), and how to test that decision with
YouTube Test & Compare.

## Evidence labels

| Label | Meaning |
|---|---|
| **[Y]** | YouTube's own documentation or blog |
| **[D]** | Data analysis (vendor or academic); observational unless stated |
| **[C]** | Creator or consultant opinion, anecdote, or single-channel test |
| **[I]** | Inference by the author of this note; not tested |

Caveat on all [D] items: none of the large studies measure CTR. They use views relative to
the channel median ("outlier score") or views per day. They show what successful
thumbnails have in common, not what causes success. Effects are small, and the studies
disagree with each other.

---

## 1. TL;DR

- No single visual feature (face, text, color, brightness) reliably separates winning from
  losing thumbnails in the large 2025–2026 studies. Differences are within a few points. [D]
- YouTube's A/B tool picks winners by **watch time share**, not CTR. A thumbnail that sets
  wrong expectations loses even if it gets more clicks. [Y]
- For this channel the biggest problems are structural, not stylistic [I]:
  - the anime dog looks the same on every episode, so the topic is carried by one word;
  - the dog thumbnails no longer match the diagram-first videos (expectation mismatch);
  - the white background merges with YouTube's light-mode UI, and the new dark canvas
    (`#0E1B17`) merges with dark mode (contrast 1.08:1 against `#0F0F0F`);
  - the current `Thumbnail` Remotion still is a title card: subtitle, authors and episode
    number become unreadable at feed size.
- Recommendation: build a code-rendered "diagram hero" template (one diagram + 1–2 words)
  as the default, and A/B test it against the current dog thumbnail and a light-canvas
  variant on the back catalog before committing.

---

## 2. Evidence on CTR drivers

### 2.1 YouTube's own guidance

| Topic | What YouTube says | Label |
|---|---|---|
| Test & Compare metric | Winner = highest **watch time share**; "we optimize tests for overall watch time over other metrics, like click-through-rate". Watch time "includes both" CTR and retention. | [Y] |
| What can be tested | Up to 3 variants: title only, thumbnail only, or title + thumbnail. | [Y] |
| Availability | Desktop YouTube Studio only; requires **advanced features**; long-form only (no Shorts, no scheduled lives; Premieres after conversion). Not for made-for-kids, mature-audience or private videos. Gradual rollout. | [Y] |
| Traffic split | Variants are shown concurrently, roughly equal shares; one variant per viewer account; a small control group sees only the default and is excluded from results. | [Y] |
| Duration | "A few days or up to 2 weeks". Ends early when one variant has significantly higher watch time share. | [Y] |
| Result labels | **Winner** (statistically significant), **Performed same** (pick what you prefer), **Inconclusive** (first-uploaded option becomes default). Older help text used "Preferred". | [Y] |
| Pitfalls | Editing the title or thumbnail during a test stops it. Low-impression channels are less likely to reach significance. Variants below 1280×720 force all variants to be downscaled. | [Y] |
| YouTube's tips | Test older videos first; make variants meaningfully different (layout, main element) before testing details; run a second test 72+ h after publish to reach the broader audience; treat results as learning about the audience. | [Y] |
| Impressions CTR range | "Half of all channels and videos on YouTube have an impressions CTR that can range between 2% and 10%." | [Y] |
| CTR interpretation | CTR naturally drops when impressions grow (e.g. Home); channel-page traffic has higher CTR; compare CTR between videos over the long term; small variations are not cause for action. | [Y] |
| Clickbait signal | High CTR + low average view duration + lower-than-expected impressions. | [Y] |
| Thumbnail spec | 1280×720 recommended, min width 640 px. | [Y] |
| AI disclosure | Generating or improving a thumbnail with AI is "production assistance" and needs no disclosure; non-realistic AI content needs none either. | [Y] |
| Localized thumbnails | Per-language thumbnails exist but attach to multi-language audio tracks (own dub or auto-dub); access tied to MLA rollout. | [D, secondary: vidIQ] |

### 2.2 Large data analyses (2025–2026)

| Study | Sample / metric | Faces | Text | Color / brightness |
|---|---|---|---|---|
| **1of10** (2025) | 300k+ high-performing videos, 52k channels; views ÷ channel median | Face vs no face "similar overall"; helps only channels with 200k+ subs; helps Finance/Beauty/Vlogs, hurts Fitness, Movies & TV; multiple faces > single face | 84% have text; text thumbnails get ~19% fewer views; best: no text, or <10 characters covering <7% of the image | Cyan, green, yellow/orange dominant colors do best (cyan ~+36%); views rise with brightness; **dark thumbnails consistently underperform** |
| **Eden** (2026) | 507k videos, 8.7k channels; 1,486 breakouts (≥2× baseline) vs 1,474 underperformers | Face 84.2% vs 82.2% (noise); eye contact 32.4% vs 29.2% (borderline) | 4–6 words 30.6% vs 26.5% (small edge); only ~6% repeat the title verbatim; ~39% share no word with the title | Brightness, contrast, saturation, warm share: no measurable difference (<1 point) |
| **vidIQ** (June 2026) | 500 breakout videos, 30 niches; channels ≥10k subs | Face in 69% of all, 80% of top 50 | 72% use text, median 5 words; 28% none | High contrast 56% overall, 46% of top 50 ("baseline, not differentiator"); FAQ: avoid YouTube's red, white and black |
| **Thumbnail Bench** (Sept 2026) | 11,223 covers, 1,043 channels ≥100k subs; views per day | Top vs other: 72% vs 70% | Top covers repeat the title slightly less (33% vs 35%) | "No single feature clearly separated winning covers" |

Education and Tech niche specifics (Thumbnail Bench, descriptive only) [D]:

| | Education | Tech |
|---|---|---|
| Face on cover | 57% | 61% |
| No text | 16% | 18% |
| Median words (when text) | 6 | 4 |
| Repeats title | 41% | 41% |
| Number on cover | 33% | 31% |

- Larger channels use **less** text and fewer arrows/screenshots (32% of 2M+ covers have
  no text vs 19% at 100k–500k). [D]
- Conflicts to keep in mind: 1of10 says text and darkness hurt; Eden finds no brightness
  effect and a slight edge for 4–6 words. Treat both as weak priors and test.

### 2.3 Academic work

- Koh & Cui, *Decision Support Systems* (2022), branded videos: thumbnail informativeness
  (number of design elements: product, person, text; object complexity) vs aesthetic cues
  (colorfulness, brightness, image quality) and view-through. Reported takeaway in
  secondary listings: aesthetic cues (brightness, colorfulness, quality) did not
  significantly influence engagement; informativeness did. Full text not verified. [D]
- Other academic papers found are small (≤30 videos) or report negligible correlations
  between brightness/colorfulness and views. No peer-reviewed causal CTR study of
  thumbnail features was found. [D]

### 2.4 Creator practice

- **Linus Tech Tips** (June 2024, own Test & Compare results) [C]:
  - most tests ended close to 50/50;
  - closed-mouth or natural expressions beat big open-mouth grins by ~1–2% watch time share;
  - mood fit beat intensity (frustrated beat smiling for a server-disaster video);
  - a calm dark blue background beat a loud green one for a calm topic;
  - arrows only help when the subject is small or unclear;
  - "packaging" earns the click; homepage viewers need clarity or they leave early.
- **Veritasium**, "Clickbait is Unreasonably Effective" (2021): accurate but enticing
  packaging ("legitbait") is fine; misleading packaging is not. Titles alone moved views
  by large factors in his experiments. [C]
- **Paddy Galloway** (via Colin and Samir summary) [C]:
  - "The difference between a million views and 28 million views is how you package it";
  - "be familiar, but unexpected": recognizable format plus a twist;
  - re-thumbnailing an old video gave one creator ~40× daily views (anecdote);
  - simplicity / "glance test", 1–3 elements (secondary summaries).
- 1of10's educational-thumbnail advice (no data): curiosity gap (cropped diagram with a
  missing piece), before/after, misconception with ✕, one icon + one word, series
  consistency; warns against "teaching instead of teasing" and overly academic visuals. [C]

### 2.5 Driver-by-driver summary

| Driver | Verdict | Label |
|---|---|---|
| Faces / emotion | Neutral to small positive in aggregate; depends on niche and channel size; genuine > exaggerated | [D] [C] |
| Text amount | Short wins or ties; long text is common but not better; big channels use less | [D] |
| Text size | Must read at feed size; no study quantifies it | [I] |
| Contrast / color | Baseline requirement, not a differentiator; dark thumbnails may underperform (1of10 only) | [D] |
| Curiosity gap | Consistently recommended; no thumbnail-level data | [C] |
| Title–thumbnail complementarity | Most successful thumbnails do not repeat the title verbatim (~94%); top covers repeat slightly less | [D] |
| Simplicity at mobile size | Consistently recommended (1–3 elements); no data | [C] |
| Consistency vs novelty | "Familiar but unexpected"; series consistency helps recognition; identical thumbnails hide the topic | [C] [I] |
| Accuracy | Required by the A/B metric (watch time) | [Y] |

---

## 3. Educational and technical channels: observed patterns

Source: the author's recollection of these channels' recent thumbnails, **not verified in
this session** [I]. Browse each channel's Videos tab before copying a pattern.

| Channel | Composition | Text | Face / character | Color |
|---|---|---|---|---|
| 3Blue1Brown | One striking frame from the video's own animation, centered | 0–4 words, sometimes a question | Occasional pi-creature mascot | Near-black background, saturated blue/yellow/brown accents |
| Computerphile | Photo of the interviewee and handwritten paper notes | Topic phrase + channel logo; very consistent | Real expert face | Photo colors, fixed layout |
| Fireship | Huge technology logo or single object | 1–3 words, meme-like | Rarely a face | Dark background, high-saturation accent |
| ByteByteGo | Simplified system diagram or icon set | Big bold topic name | No face | Light background, colorful flat illustration |
| Two Minute Papers | Most striking result image from the paper | Short hook phrase | Host face sometimes | Result-image colors |
| Veritasium | One object or phenomenon, often with presenter | 0–3 words | Presenter, natural expression | Bright, clean |
| Asianometry | Photo of the chip, fab, company or person | Few words | Rarely | Muted, photographic |
| Hussein Nasser | Host face plus technology logos/diagram fragment | Few words | Host face | Varies |

Common thread [I]:

- The picture is **the subject itself** (the result, the mechanism, the object), not a
  generic mascot standing next to it.
- 0–4 words; the title carries the promise.
- A recognizable channel look comes from palette, type and layout, not from repeating
  the same figure.

---

## 4. Mascot vs diagram, and AI imagery risk

- No study compares mascot thumbnails with diagram thumbnails. [D: none found]
- Faces: aggregate effect near zero; eye contact borderline positive (Eden). The dog's
  **visor hides its eyes**, removing the one face cue with any signal. [D] [I]
- Sameness: the dog appears on 200+ thumbnails in similar poses; the topic differs only in
  one word and background props, so a returning viewer cannot tell episodes apart at a
  glance. [I]
- Expectation mismatch: diagram-first videos with dog thumbnails promise a cartoon and
  deliver a diagram lecture. Test & Compare's watch-time metric penalises this. [Y] [I]
- AI imagery perception:
  - experiment (N = 1,171, *Journalism & Mass Communication Quarterly*): AI-generated
    images lowered trust compared with real photos, regardless of disclosure strategy; [D]
  - surveys (Clutch 2025, others; vendor, self-reported): a large minority trust brands
    less when AI images are used undisclosed; [D, weak]
  - creator backlash against AI thumbnail tools (MrBeast / ViewStats, June 2025) shows
    hostility among creators; no viewer CTR data. [C]
  - Inference: a technical audience reading about Raft or GFS is likely to recognise the
    current glossy anime/AI rendering style and may associate it with low-effort content.
    Code-rendered diagrams signal "made by someone who understood the paper". [I]
- Brand value of the dog: real but unmeasured. It is the only cross-episode recognition
  cue today. Removing it is a bet; test it rather than assume. [I]

---

## 5. CTR benchmarks for a small niche channel

- YouTube: half of channels/videos sit between **2% and 10%** impressions CTR. [Y]
- Interpretation rules for this channel [Y] [I]:
  - compare a video only with **this channel's own** videos, over 28–90 days;
  - split by traffic source (Browse, Suggested, Search, Channel page); search CTR for an
    exact paper name ("Raft consensus") is naturally higher than Browse CTR;
  - a video that starts reaching Browse will show **falling CTR with rising impressions**:
    this is good news, not a thumbnail failure;
  - low-impression videos have noisy CTR; ignore differences under ~1 percentage point
    unless impressions are in the thousands;
  - watch CTR together with average view duration; high CTR + low AVD = misleading
    packaging.
- Small channels have fewer impressions per video, so Test & Compare will more often end
  **Inconclusive**. Plan for that (section 7).

---

## 6. Language on the thumbnail

- No data found on thumbnail text language for non-English audiences. [D: none found]
- Existing practice: Polish titles and narration, English technical terms (style guide:
  "technical terms stay in English"). [repo]
- Recommendations [I]:
  - Thumbnail word = the **canonical English name** (RAFT, GFS, MapReduce, Transformer,
    LOCK-FREE). Polish engineers know these terms, they match what people search, and
    they are short.
  - Polish goes in the **title**, which carries the promise or the question ("Jak pięć
    serwerów wybiera nowego lidera, gdy stary padnie?"). Thumbnail and title must not repeat
    each other. [D: complementarity]
  - Polish words on the thumbnail only as a tested variant (e.g. a 1–2 word hook such as
    "BEZ LOCKÓW?"), and watch diacritics at small sizes (ą, ę, ł, ż survive in Fraunces
    600 at ≥200 px; check at 168 px width).
  - Localized thumbnails need multi-language audio tracks; not relevant until the channel
    dubs into English. [D]

---

## 7. Recommendations for this channel

### 7.1 Universal rules (all templates)

- One subject, at most three elements (word, diagram, optional character). [C]
- 1–2 words, ideally ≤10 characters, in Fraunces 600, cap height ≥140 px on a 1920×1080
  canvas (≈ 200 px+ font size). [D: 1of10 short text] [I: size]
- No subtitle, authors, year, episode number or channel name on the thumbnail. They are
  unreadable at feed size and repeat the title or channel info shown next to it. [I]
- Keep the **bottom-right ~25% × 20%** free of key content (duration badge, watched
  progress bar). [I]
- Light vs dark: the thumbnail needs a visible edge in both YouTube themes. Either use the
  light canvas, or on the dark canvas let a bright element (diagram, glow, pink word)
  occupy a large area and reach near the edges. [I, from contrast figures below]
- Color means role, as in the videos: raspberry `leader` = the protagonist of the paper,
  ochre `candidate` = the competing element, `danger` + ✕ = the failure the paper solves.
- Show **a state, not a legend**: a crashed node with ✕, two leaders in conflict, a log
  with one missing cell. This is the curiosity gap for a paper channel. [C] [I]

Contrast check of palette pairs (WCAG ratio, computed):

| Pair | Ratio | Note |
|---|---|---|
| `heading` `#F4C6CC` on dark canvas `#0E1B17` | 11.6 | Title word: excellent |
| `leader` `#DC5C8A` on dark canvas | 5.0 | OK for large shapes |
| `candidate` `#BF8530` on dark canvas | 5.6 | OK for large shapes |
| bottle green `#1F3B33` on light canvas `#F8E9E6` | 10.3 | Title word, light template |
| raspberry `#B4245D` on light canvas | 5.3 | OK for large shapes |
| dark canvas vs YouTube dark UI `#0F0F0F` | **1.08** | Thumbnail edge disappears in dark mode |
| light canvas vs YouTube light UI `#FFFFFF` | **1.18** | Edge weak in light mode (current white thumbnails: ~1.0) |
| dark canvas vs light UI / light canvas vs dark UI | 17.7 / 16.2 | Strong edge |

(YouTube UI colors are approximate; check against a current screenshot.)

### 7.2 Template options

| | A. Diagram hero (dark) | B. Dog + diagram hybrid | C. Big term (light) |
|---|---|---|---|
| Layout | Left 45%: 1–2 words, stacked, Fraunces 600 in `heading` pink. Right 55%: one diagram in its most telling state (Raft: 5-node ring, raspberry leader glowing, one node ✕) | Diagram as in A, smaller; dog (≤35% of height) interacting with it (pointing, pulling a wire); word top-left | Light canvas `#F8E9E6`; one huge word (≥45% width) in bottle green; one raspberry/ochre glyph from the diagram (one ✕, one arrow, one cell) |
| Canvas | `#0E1B17`, optionally lifted (radial glow behind diagram) to raise mean brightness | Dark or light | `#F8E9E6` |
| Text | English term, 1–2 words | Same | Same, or a 2–3 word hook (tested) |
| Dog | No | Yes, redrawn flat in the palette, **eyes visible**, fixed pose set | No (optional small corner mark, tested) |
| Production | 100% Remotion, from episode data | Image model for dog layer (transparent PNG); Remotion composites text and diagram | 100% Remotion |
| Matches new videos | Exactly (first 5 s of the video = thumbnail) | Mostly | Same palette, light theme |
| Pros | Honest, recognisable as "this channel", automated, cheap, consistent topic signal | Keeps 200 episodes of recognition, adds character | Bright (counters "dark underperforms"), strong edge in dark mode, cleanest at small size |
| Cons / risks | Dark; edge vanishes in dark mode; diagram may look "academic" or busy at 168 px | Two-tool pipeline; AI-look risk; dog consistency; more elements | Weak edge in light mode; less "cinematic"; less of the diagram story |
| Evidence base | [C] simplicity, [Y] accuracy; [D] dark risk (1of10) | [D] faces neutral; [I] brand value | [D] brightness (1of10), short text |

Default recommendation [I]: **A as the production default, C as its challenger, current
dog thumbnails as the control.** Build B only if the dog wins or ties clearly in phase 1.

### 7.3 A/B testing plan (Test & Compare)

Prerequisites:

- Enable advanced features; run tests from desktop Studio.
- Upload variants at 1280×720 or larger (all three, or the test downscales them).
- Never edit title or thumbnail of a video while its test runs.
- Log every test in one table: video, variants, start/end, result label, watch time
  shares, impressions during test, traffic source mix.

Phase 1: template choice (back catalog, ~3–4 weeks)

- Pick the 10–15 videos with the most impressions in the last 28 days (evergreen papers:
  Attention, GPT-3, Raft, GFS, MapReduce…). Low-impression videos will mostly end
  Inconclusive. [Y]
- On each: 3 variants = current dog (control) vs A vs C. Same title for all
  (thumbnail-only test).
- Let each test finish (≤2 weeks). Run them in parallel; they are independent videos.
- Decision rule [I]:
  - count Winner results per template across videos (a sign test, not one result);
  - adopt the template that wins most conclusive tests and is never a clear loser;
  - if most tests end **Performed same / Inconclusive**, the thumbnail style does not
    measurably matter for this audience: choose A (cheapest, consistent with the
    videos).
- Read watch time shares, not just the label: 55/45 repeated across many videos is a
  signal even if each single test is inconclusive.

Phase 2: details within the winning template (next 4–6 weeks)

- One factor per round, large differences first [Y]:
  1. English term vs Polish hook vs no text;
  2. light vs dark canvas (if A won) or diagram state vs neutral diagram;
  3. dog mark vs no dog;
  4. title tests (title-only) on new uploads once the thumbnail is fixed.

Phase 3: new uploads

- Start a Test & Compare on every new upload at publish time with 2–3 variants of the
  chosen template (the test starts on publish). Rerun one 72+ h later if the first ends
  inconclusive, to reach the broader audience. [Y]

Re-thumbnailing the back catalog

- After phase 1, re-thumbnail in batches of ~20 videos per week, newest-impression first.
- Measure: impressions and CTR 28 days before vs 28 days after, per traffic source,
  compared with not-yet-changed videos over the same weeks (simple
  difference-in-differences; seasonality and algorithm changes affect both groups). [I]
- Keep the old PNGs (`youtube/thumbnails/*-optimized.png`) for rollback.
- Expect small changes on most videos; a few videos may move a lot (Galloway anecdote).
  [C]

How to read results [Y] [I]:

- Winner by watch time share = more clicks **and/or** longer viewing. A variant that wins
  CTR but loses watch time over-promised.
- Check Studio CTR and AVD for the test period as a sanity check; a winner with much
  lower AVD is a warning sign.
- Re-test winners after ~6 months; preferences drift. [Y]

### 7.4 Pipeline

Option 1: Remotion still (recommended default)

- New `ThumbnailCard` component, separate from `TitleCard`. `TitleCard` stays as the
  in-video chapter/title design; the thumbnail is a different, simpler layout.
- Props in the episode timeline/storyboard JSON, e.g.
  `thumbnail: { words: ["RAFT"], form: "cluster", state: "leader-crash", theme: "dark" }`.
  The storyboard LLM step proposes 2–3 variants (word, diagram state, theme) for A/B.
- Reuse existing scene primitives (`RoleNode`, `Link`, `Badge`, `LogCell`, `StatePill`)
  scaled up 1.5–2× and with fewer nodes than in the video.
- Render each variant with `remotion still Thumbnail` at 1920×1080, then downscale to
  1280×720 and compress under the project's existing size limit
  (`scripts/compress_images.py`).
- The video intro (first 5 s) uses the winning variant, so thumbnail and video match.

Option 2: image model

- Use only for an illustrative layer (dog, or a physical metaphor such as a raft) on a flat
  or transparent background in palette colors.
- Never let the image model draw the text or the diagram: misspellings, wrong fonts and
  pseudo-diagrams undermine credibility with a technical audience. [I]
- Composite in Remotion (`<Img>`) so text, palette and layout stay code-controlled.
- Fix a seed/reference set for the character so episodes stay consistent.

Legibility checklist (run on every variant) [I]

- [ ] Downscale the 1280×720 PNG to **320×180** (mobile feed) and **168×94**
      (desktop sidebar / small surfaces); view both at 100% zoom.
- [ ] The word is readable at 168×94 without squinting. Optional automatic check: OCR
      (e.g. `tesseract`) on the 320×180 image must return the word.
- [ ] The diagram's main state (who is leader, what failed) is identifiable at 320×180.
- [ ] ≤3 elements; nothing smaller than ~100 px at 1920×1080 carries meaning.
- [ ] Paste each size on `#0F0F0F` and `#FFFFFF` backgrounds: the thumbnail's edge is
      visible in both.
- [ ] Grayscale version: word and key shape still separate from the background
      (luminance contrast, not only hue; also protects colorblind viewers).
- [ ] Text contrast ≥ 4.5:1 against its local background.
- [ ] Bottom-right ~25% × 20% has no key content.
- [ ] Thumbnail word does not repeat the title; together they say more than either alone.
- [ ] Montage the candidate next to 8–10 current thumbnails from the niche
      (e.g. `magick montage`) and check that it stands out and is recognisably this
      channel.
- [ ] The promise matches the first 30 s of the video.

---

## 8. Open questions

- Current channel numbers: impressions per video per week, traffic source split, share of
  viewers in YouTube dark mode. These decide how many tests can reach significance.
- Are advanced features enabled and is Test & Compare visible in Studio?
- Is the dog considered part of the brand identity beyond thumbnails (avatar, outro)? The
  new outro already drops it.
- Should the light theme become the thumbnail theme even if videos stay dark?

---

## Sources

YouTube (primary)

- Test & compare thumbnails: <https://support.google.com/youtube/answer/13861714>
- A/B test titles & thumbnails: <https://support.google.com/youtube/answer/16391400>
- YouTube blog, "René's top five" (June 14, 2024), why watch time not CTR:
  <https://blog.youtube/creator-and-artist-stories/renes-top-five-june-14-2024/>
- Impressions and click-through rate: <https://support.google.com/youtube/answer/7628154>
- Add video thumbnails: <https://support.google.com/youtube/answer/72431>
- Disclosing altered or synthetic content: <https://support.google.com/youtube/answer/14328491>

Data analyses

- 1of10, "What actually makes a YouTube video go viral in 2025":
  <https://1of10.com/blog/what-actually-makes-a-youtube-video-go-viral-in-2025>
- 1of10 data report 2025: <https://1of10.kit.com/data-report-2025>
- Search Engine Journal, "Do faces help YouTube thumbnails?":
  <https://www.searchenginejournal.com/do-faces-help-youtube-thumbnails-heres-what-the-data-says/563944/>
- Eden, "What makes a good YouTube thumbnail? We analyzed 507,478 videos":
  <https://eden.so/blog/what-makes-a-good-youtube-thumbnail/>
- vidIQ, YouTube thumbnail study (500 breakouts, June 2026):
  <https://vidiq.com/research/youtube-thumbnail-study/>
- Thumbnail Bench, YouTube thumbnail study 2026:
  <https://thumbnailbench.com/resources/youtube-thumbnail-study-2026>
- Net Influencer coverage of Thumbnail Bench:
  <https://www.netinfluencer.com/youtube-thumbnail-study-of-100k-channels-finds-shocked-faces-on-just-1-in-10-covers/>
- vidIQ, multilingual thumbnails: <https://vidiq.com/blog/post/multilingual-thumbnail-feature-youtube/>

Academic

- Koh & Cui (2022), "An exploration of the relation between the visual attributes of
  thumbnails and the view-through of videos: The case of branded video content",
  *Decision Support Systems*:
  <https://www.researchgate.net/publication/361270134_An_exploration_of_the_relation_between_the_visual_attributes_of_thumbnails_and_the_view-through_of_videos_The_case_of_branded_video_content>
- Koh & Cui, "Give a Gist: The Impact of Thumbnails on the View-Through of Videos"
  (preprint): <https://bohrium.dp.tech/paper/arxiv/2305.17051>
- "Perceived legitimacy matters: building public trust and acceptance of AI-generated
  news images through strategic AI disclosure" (*JMCQ*, N = 1,171):
  <https://mediawell.ssrc.org/citations/perceived-legitimacy-matters-building-public-trust-and-acceptance-of-ai-generated-news-images-through-strategic-ai-disclosure/>

Creators and industry

- Linus Tech Tips, "Why our Thumbnails Look Like This." (June 30, 2024):
  <https://www.youtube.com/watch?v=lHIWMmVoA44>
- Veritasium, "Clickbait is Unreasonably Effective" (2021):
  <https://www.youtube.com/watch?v=S2xHZPH5Sng>
- Colin and Samir, "The new rules of YouTube from Paddy Galloway":
  <https://www.colinandsamir.com/resources/the-new-rules-of-youtube-from-paddy-galloway>
- 1of10, "Thumbnail ideas for educational videos" (opinion):
  <https://1of10.com/blog/thumbnail-ideas-for-educational-videos>
- PetaPixel, MrBeast AI thumbnail tool backlash (June 2025):
  <https://petapixel.com/2025/06/24/mrbeast-faces-backlash-for-ai-thumbnail-generator-tool/>
- Clutch, AI imagery survey 2025: <https://clutch.co/press-releases/ai-imagery-survey-2025>

Repo context

- `docs/design/visual-style.md` (palette, typography)
- `youtube/remotion/src/design/cards.tsx` (`TitleCard`), `youtube/remotion/src/Episode.tsx`
  (`Thumbnail` still)
- `youtube/prompts/thumbnails/73-raft-thumbnail.md` (current image-model prompt)
