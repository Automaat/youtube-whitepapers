# Głęboki Odczyt: visual style

Binding style guide for diagram-first episodes rendered with Remotion. Applies to every
scene, the intro and outro cards, and to the LLM steps that plan or code scenes.

- Source of truth for values: `youtube/remotion/src/design/tokens.ts`. This document
  explains them; if the two disagree, fix the document.
- Reference mockups: `docs/design/mockups/raft-style.html` (open in a browser; dark/light
  toggle).
- Palette origin: `Automaat/ohara` redesign (`docs/design/redesign/README.md` on
  `origin/main`): powder pink, bottle green, raspberry.

## 1. Principles

1. **Diagram first.** The picture carries the idea; text only labels it. Max ~12 words
   of on-screen text per scene besides labels. No burned-in narration (captions are
   CC from SRT).
2. **Concrete before abstract.** Show a specific run (S1…S5, term 2, index 5) before
   naming the rule.
3. **One idea per scene**, built progressively. New elements appear exactly when the
   narrator names them (cue timestamps from TTS).
4. **Signal the active element.** Active = full opacity + pink glow; everything else
   drops to 30% opacity. Never more than one glowing group at a time.
5. **Stable geometry.** A diagram that continues across scenes keeps node positions,
   colors and labels. Viewers track position, not names.
6. **Color means role, never decoration.** A color assigned in the glossary keeps its
   meaning for the whole episode.

## 2. Palette

Dark theme is the default for video. Light theme exists for thumbnails or a future
switch; both pass the dataviz palette validator.

| Token | Dark | Light | Use |
|---|---|---|---|
| `canvas` | `#0E1B17` | `#F8E9E6` | Frame background |
| `surface` | `#16261F` | `#FFF7F5` | Cards, follower nodes |
| `inset` | `#1E3029` | `#F1DAD6` | Chips, bars, empty slots |
| `line` | `#2B4038` | `#E6CBC6` | Lanes, grid, dividers, links |
| `ink` | `#F7E6E3` | `#1F3B33` | Body text, labels |
| `muted` | `#A9B3AE` | `#59635E` | Secondary text; neutral role (follower) |
| `heading` | `#F4C6CC` | `#1F3B33` | Titles, active outline, progress "now" |
| `glow` | `#F4C6CC` @ 55% | `#B4245D` @ 35% | Glow on the active element |
| `success` | `#6FBF97` | `#276B4E` | Committed, vote granted, ✓ |
| `successSoft` | `#183A2C` | `#D9ECDF` | Committed cell fill |
| `danger` | `#F08A7E` | `#A3322A` | Failure, rejected; always with ✕ |
| `leader` | `#DC5C8A` | `#B4245D` | Role 1 (raspberry); key chart series |
| `candidate` | `#BF8530` | `#A3620C` | Role 2 (ochre) |
| `c3` | `#4F97CF` | `#1F6FAE` | Role 3 (blue), reserved |
| `onRole` | `#0E1B17` | `#FFF7F5` | Text on a role-colored fill |
| `brandTint` | `#F4C6CC` | `#F4C6CC` | Skeptic chip and card |

Rules:

- At most three role colors per episode (`leader`, `candidate`, `c3`) plus neutral.
  Map the paper's main actors to them in the storyboard glossary.
- Ohara's accent `#F2779F` is not a role color: it fails against `danger` (ΔE 7.3)
  and against green for deuteranopes.
- `danger` and `success` always come with an icon (✕ / ✓), never color alone.
- Charts: the key series in `leader`, comparison series in `muted`; axis and grid in
  `line`.

## 3. Typography

| Role | Font | Size at 1080p |
|---|---|---|
| Titles, chapter cards, big numbers | Fraunces 600 | 72–250 px |
| Scene title (optional, top-left under brand) | Fraunces 600 | 56–72 px |
| Labels, body | Plus Jakarta Sans 500–700 | 24–46 px |
| Technical terms, values, ids (term 3, S1, index 5) | JetBrains Mono 500–700 | 22–40 px |

- Minimum text size 22 px. Labels on diagrams 26–32 px.
- Polish diacritics: fonts load the `latin-ext` subset.
- Technical terms stay in English (leader, term, commit); everything else Polish.

## 4. Frame layout

- Canvas 1920×1080, 30 fps. Safe margins 96 px.
- Layout grid 6×6 inside the margins (cell ≈ 288×148 px). Place diagram anchors on
  grid lines (`grid(col,row)` helper).
- Chrome on every content frame:
  - top-left: brand mark "Głęboki Odczyt · #NN Title" (Fraunces, `heading`);
  - top-right: chapter label + progress segments (done `muted`, now `heading`);
  - bottom-left: speaker chip with level bars; narrator neutral, skeptic `brandTint`.
- Diagram area: y 160–980. Keep the bottom-left chip area (x < 520, y > 960) clear.
- Chapter change: a chapter card overlay (2.5 s) slides in at the first scene of each
  chapter: "Rozdział N" + title, list of chapters on the right.

## 5. Scene vocabulary (`visual_form`)

| Form | Use for | Built from |
|---|---|---|
| `title` | Episode title card | `TitleCard` |
| `cluster` | Servers and their roles, failures, who talks to whom | `RoleNode`, `Link`, `Message`, `Badge` on a ring (`ring()`) |
| `state-machine` | States and transitions (e.g. follower/candidate/leader) | `StatePill`, `CurvedArrow`, moving dot |
| `swimlane` | Protocol over time: one lane per node, messages as arrows/dots, timers as bars | `Lane`, `TimerBar`, `Arrow`, `Message` |
| `log-grid` | Replicated logs: one row per server, cells with term + command, commit marker | `LogCell`, `IndexRuler`, `Marker` |
| `glossary` | Pre-training: 3–5 terms with icon and ≤6-word definition | `TermCard` |
| `list` | Guarantees, properties, steps (≤5 items, active one highlighted) | `ListItem` |
| `comparison` | Two approaches side by side, or a 2×2 | `Card`, `ListItem` |
| `bar-chart` | Results redrawn from the paper; title states the takeaway | `BarChart` |
| `quote` | One short paper quote with page reference (sparingly) | `Quote` |
| `recap` | Final diagram + one line per chapter | any of the above |

Motion rules:

- Elements enter with a 12–18 frame fade + 24 px rise (`enter()`); nothing bounces.
- Messages travel as a dot along the arrow over 18–30 frames, then the arrow stays.
- Timers grow linearly in real time when the narration describes time passing.
- Failure: node fades to `crashed` style (dashed outline, ✕ badge) over 10 frames.
- Hold the final state of a scene; never animate during the last 15 frames.
- Every change is tied to a cue from the script, not to a fixed frame offset, except
  continuous motion that starts at a cue.

## 6. Episode structure on screen

1. **Intro (first 5 s):** episode thumbnail, full frame, while the narrator greets
   ("Witamy ponownie w Głębokim Odczycie…"). Without a thumbnail file the title card
   design is used (`Thumbnail` composition).
2. Content scenes with chrome.
3. **Outro (last 5 s, silent):** "Polub i subskrybuj" card in the episode style
   (`Outro` composition): no mascot, brand pink on green, bell and thumb icons,
   pulsing ring. It replaces `youtube/pl/slides/last-slide.png` for diagram-first
   episodes.

## 7. Checks before render

- Every still at cue + 0.5 s is reviewed (stills-review step): no overlaps, text ≥22 px,
  nothing outside safe margins, numbers and labels match `claims.json` and the script.
- Contrast: text on `surface`/`canvas` uses `ink` or `muted` only; text on role fills
  uses `onRole`.
