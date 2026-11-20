# YouTube metadata step

Write the YouTube metadata for one episode of "Głęboki Odczyt" (Polish channel
explaining research papers). Read `{episode_dir}/episode.yaml`,
`{episode_dir}/script.yaml` and the first pages of `{episode_dir}/paper.txt`.
Do not edit files. Polish only; technical terms may stay in English.

- `title`: what the video teaches, specific and searchable, at most 70 characters,
  without the channel name and without "| Deep Dive" (added later). Pattern used on
  the channel: "<Polish topic> (<paper name>) - <first author> <year>".
- `intro`: 2–3 sentences that start with "🎙️ " and say what problem the paper
  solves and what the viewer will understand after watching. No hype words.
- `topics`: 5–8 short bullet texts in the order of the episode.
- `publication`: venue and year as in the paper (e.g. "USENIX ATC 2014").
- `tags`: 8–12 tags without "#", single words or CamelCase, Polish and English,
  e.g. "SystemyRozproszone", "Consensus", "Raft", "DeepDive".
