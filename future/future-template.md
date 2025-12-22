# Paper Download Template

Template for creating paper lists that can be auto-downloaded using `/download-papers` slash command.

---

## Format 1: Markdown (Recommended)

Use this format for structured paper collections with metadata:

```markdown
### Attention Is All You Need (2017)

- **PDF:** [arxiv.org](https://arxiv.org/abs/1706.03762)
- **Name:** attention-is-all-you-need
- **Category:** llm

### BERT: Pre-training of Deep Bidirectional Transformers (2018)

- **PDF:** [arxiv.org](https://arxiv.org/abs/1810.04805)
- **Name:** bert
- **Category:** llm

### Raft: In Search of an Understandable Consensus Algorithm (2014)

- **PDF:** [usenix.org](https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf)
- **Name:** raft
- **Category:** distributed-computing
```

**Fields:**

- `###` Title header (required) - extracted as paper title
- `**PDF:**` or `**URL:**` (required) - download source
- `**Name:**` (required) - slug format: `lowercase-with-hyphens`
- `**Category:**` (required) - one of: `llm`, `distributed-computing`, `security`, `networking`, `operating-systems`

---

## Format 2: JSON

For programmatic generation:

```json
[
  {
    "name": "attention-is-all-you-need",
    "category": "llm",
    "url": "https://arxiv.org/abs/1706.03762",
    "title": "Attention Is All You Need"
  },
  {
    "name": "bert",
    "category": "llm",
    "url": "https://arxiv.org/abs/1810.04805",
    "title": "BERT: Pre-training of Deep Bidirectional Transformers"
  }
]
```

---

## Format 3: Simple URL List

For quick imports (will auto-generate names from arxiv/openreview IDs):

```text
https://arxiv.org/abs/1706.03762
https://arxiv.org/abs/1810.04805
https://openreview.net/forum?id=BkUDW_lCb
```

**Note:** Auto-generated names may need manual cleanup. Category defaults to `llm`.

---

## Naming Conventions

Follow project naming standard: `{episode}-{paper-name}`

**Paper name format:**

- Lowercase only
- Use hyphens (not underscores or spaces)
- Keep concise but descriptive
- Use common abbreviations (bert, gpt, raft)

**Examples:**

- ✅ `attention-is-all-you-need`
- ✅ `bert`
- ✅ `gpt3`
- ✅ `raft`
- ❌ `Attention_Is_All_You_Need`
- ❌ `attention`
- ❌ `paper-1`

---

## Supported Download Sources

### Automatic Detection

- **arXiv:** `https://arxiv.org/abs/XXXX.XXXXX` or `https://arxiv.org/pdf/XXXX.XXXXX`
- **OpenReview:** `https://openreview.net/forum?id=XXXXXXXX`
- **Direct PDF:** Any URL ending in `.pdf`

### Fallback Strategy

Script tries multiple sources in order:

1. arXiv (primary + mirror)
2. OpenReview
3. Direct URL download

If all fail → added to manual download list

---

## Categories

Current categories (check `whitepapers/` directory for latest):

- `llm` - Language models, NLP
- `distributed-computing` - Distributed systems, consensus
- `security` - Security, cryptography, privacy
- `networking` - Network protocols, TCP/IP
- `operating-systems` - OS design, kernels, virtualization

---

## Usage

```bash
# Download papers from file
/download-papers future/my-papers.md

# Dry run (preview without downloading)
/download-papers future/my-papers.md --dry-run

# Or use mise task
mise run download -- future/my-papers.md
mise run download -- future/my-papers.md --dry-run
```

---

## What Gets Auto-Generated

1. **Episode numbers** - automatically assigned from first available slot in `status.json`
2. **File names** - `whitepapers/{category}/{episode}-{name}.pdf`
3. **Status entry** - added to `whitepapers/status.json`

**Example:**

Input:

```markdown
### Attention Is All You Need (2017)

- **PDF:** [arxiv.org](https://arxiv.org/abs/1706.03762)
- **Name:** attention-is-all-you-need
- **Category:** llm
```

Creates:

- File: `whitepapers/llm/54-attention-is-all-you-need.pdf` (assuming 54 is next available)
- Status:

```json
{
  "episode": "54",
  "name": "attention-is-all-you-need",
  "category": "llm",
  "source_url": "https://arxiv.org/abs/1706.03762",
  "title": "Attention Is All You Need (2017)"
}
```

---

## Tips

- **Check for duplicates** - script will skip papers already in `status.json`
- **Verify URLs** - test URLs manually if download fails
- **Use arxiv when possible** - most reliable download source
- **Group by category** - easier to manage in batches
- **Review dry-run first** - always check plan before downloading
