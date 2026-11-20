# Layout step

You prepare shared geometry for the scene code of one episode of "Głęboki Odczyt",
a Polish YouTube channel that explains papers with animated diagrams. Several agents
will write the scenes in parallel next; your file keeps diagrams that continue
across scenes in the same place.

## Read first

- `docs/design/visual-style.md`: frame layout, grid, safe area, scene vocabulary.
- `youtube/remotion/src/design/tokens.ts` and `youtube/remotion/src/design/index.ts`.
- `youtube/remotion/src/episodes/73-raft/layout.ts`: an approved example.
- `{episode_dir}/storyboard.yaml`: every scene's `visual_form`, `visual` and
  `continues_from`.

## Task

Write `youtube/remotion/src/episodes/{slug}/layout.ts` with the Write tool. Export
named constants (and small pure helpers) for every diagram that appears in more
than one scene: actor names, node positions, lane and row coordinates, log or table
cell geometry, chart areas. Keep everything inside x 96–1824, y 150–960 and leave
x < 520, y > 950 free for the speaker chip. Import only from `"../../design"`.
No React components, no comments except a short "why".

Then run `npm --prefix youtube/remotion run typecheck`; errors in your file must be
fixed. Reply with one line per exported group and the scenes that use it.
