Download whitepapers from $ARGUMENTS file with automatic indexing and verification.

**Prerequisites:**

- Input file exists (supports JSON, Markdown, or plain URL list)
- See `future/future-template.md` for format specifications

**What this does:**

1. Parses input file for paper metadata (name, category, URL)
2. Checks `whitepapers/status.json` for:
   - Next available episode numbers (including gaps)
   - Duplicate papers (by name or URL)
3. Downloads papers from multiple sources:
   - arXiv (primary + mirror)
   - OpenReview
   - Direct URL
4. Verifies PDFs are valid
5. Saves to `whitepapers/{category}/{episode}-{name}.pdf`
6. Updates `whitepapers/status.json`
7. Reports failed downloads for manual intervention

**Usage:**

```bash
# Download papers
/download-papers future/my-papers.md

# Dry run (preview only)
/download-papers future/my-papers.md --dry-run
```

**Example input formats:**

See `future/future-template.md` for complete documentation.

**Markdown format (recommended):**

```markdown
### Attention Is All You Need (2017)

- **PDF:** [arxiv.org](https://arxiv.org/abs/1706.03762)
- **Name:** attention-is-all-you-need
- **Category:** llm
```

**JSON format:**

```json
[
  {
    "name": "attention-is-all-you-need",
    "category": "llm",
    "url": "https://arxiv.org/abs/1706.03762"
  }
]
```

**Simple URL list:**

```text
https://arxiv.org/abs/1706.03762
https://arxiv.org/abs/1810.04805
```

---

Execute: `python scripts/download_papers.py $ARGUMENTS`

Show output and report:

- Number of papers found
- Duplicates skipped
- Downloads successful
- Failed downloads (with URLs for manual download)
- Status.json update confirmation
