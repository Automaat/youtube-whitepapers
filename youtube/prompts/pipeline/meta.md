# Episode metadata step

Read `{episode_dir}/paper.txt` (the first two pages are usually enough) and return
the facts for the episode title card. Do not edit files.

- `title`: the short name viewers know the paper by, as in the paper (e.g. "Raft",
  "MapReduce", "GPT-3"). At most 3 words.
- `subtitle`: Polish translation or paraphrase of the paper title, at most 8 words,
  technical terms in English.
- `authors`: up to three authors as "First Last, First Last" (add "i in." when there
  are more), then " · " institution of the first author, then " · " year. Example:
  "Diego Ongaro, John Ousterhout · Stanford · 2014".
- `paper_url`: the canonical public URL of the paper (arXiv abs page, ACM DOI or the
  authors' page) when the text names one or it is well known; otherwise "".
