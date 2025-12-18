# NotebookLM Prompt

Generate 11 presentation slides based on the podcast about the FineWeb Dataset paper by Hugging Face.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Secret Recipe for LLM Training Data

Content to include:

- The real secret of training large language models (Llama 3, Mixtral) isn't architecture—it's the training data recipe
- Big labs treat data curation recipes as trade secrets, creating a gap with the open source community
- FineWeb paper by Hugging Face provides transparent, step-by-step documentation of the entire data curation process
- Goal: give the community "the fishing rod, not just the fish"—methodology, not just the dataset
- This fundamentally changes the game for open AI development

## Slide 2: Two Major Results - FineWeb and FineWeb-Edu

Content to include:

- FineWeb: 15 trillion tokens collected and filtered from 96 Common Crawl dumps
- Scale sufficient to train super-heavyweight models (500B+ parameters)
- FineWeb-Edu: carefully curated subset of 1.3 trillion tokens filtered for high educational value
- Analogy: extracting only the best books and articles from the chaotic internet library
- Both datasets publicly released with full documentation

## Slide 3: The Data Ablation Methodology

Content to include:

- Rigorous scientific approach: test every decision independently, not just trust the final result
- Analogy: baking multiple small cakes with single ingredient variations, then comparing results
- Trained series of 1.7B parameter models on different data variants
- Applied specific filter → trained model → compared against model without filter on benchmarks
- Transforms intuition into hard empirical data—each decision is statistically validated

## Slide 4: Text Extraction - The First Critical Step

Content to include:

- Common Crawl available in two formats: raw WARC files (with HTML) and preprocessed WET files
- Most projects use WET files for convenience
- Discovery: using Trafilatura on raw WARC files produces significantly better results
- Trafilatura carefully separates article content from menus, footers, ads
- This single "technical" decision already showed measurable improvement in model performance

## Slide 5: The Surprising Deduplication Discovery

Content to include:

- Initial intuition: aggressive global deduplication across all 96 dumps should maximize quality
- Shocking result: almost no improvement from global deduplication
- For older dumps (2013-2014), it actually preserved lower quality data while discarding valuable content
- Library analogy: removing all duplicated books would discard classics (copied millions of times) and keep obscure pamphlets
- Valuable content is more frequently duplicated on the internet—global deduplication treats it as junk

## Slide 6: Local Deduplication - The Solution

Content to include:

- Changed approach: treat each of 96 dumps as a separate library
- Applied deduplication within each dump individually, not globally
- Used MinHash algorithm for local deduplication
- This single change allowed FineWeb to match the performance of Refined Web (leading public dataset at the time)
- Key insight: less aggressive, more contextual deduplication outperforms brute-force approaches

## Slide 7: Learning from C4 Filters - Data-Driven Refinement

Content to include:

- Analyzed classic C4 dataset filters to understand what made it effective
- Discovery: punctuation filter (requiring each line to end with punctuation) was effective but too aggressive—rejected 30% of data
- Adopted less invasive C4 filters, skipped the punctuation requirement
- Created custom filters using statistical analysis of "good" vs "bad" data from deduplication experiments
- New intelligent filter: remove documents where <12% of lines end with punctuation marks
- Data-driven approach ultimately surpassed C4 quality while preserving more data

## Slide 8: Creating FineWeb-Edu - AI Teaching AI

Content to include:

- Inspired by speculation that Llama 3 was trained on specially curated high-quality/synthetic data
- Used Llama 3 70B Instruct to rate ~500,000 random web pages from FineWeb
- Rating scale: 0-5 for educational value, focused on school-level knowledge (not niche academic)
- These ratings became training data for a smaller, fast classifier model
- Small classifier then evaluated all 15 trillion tokens, selecting 1.3T with score ≥3
- Methodology: using one advanced AI to teach another how to recognize valuable content

## Slide 9: Spectacular Results of Educational Filtering

Content to include:

- FineWeb-Edu models dominate benchmarks measuring knowledge and reasoning (MMLU, ARC)
- Key finding: model trained on FineWeb-Edu achieved scores that required 10x more training data for competitors
- Hard proof that precision data curation brings disproportionately large benefits
- Not just removing junk—actively selecting "pearls" from the ocean of data
- Suggests high-quality educational data teaches better reasoning patterns, not just facts

## Slide 10: Limitations and Bias Analysis

Content to include:

- Still only web data—could be enhanced with books, transcripts, scientific articles
- All Data Ablation experiments done on 1.7B models (cost constraints); results at 500B+ scale may differ
- FineWeb reflects internet stereotypes: overrepresentation of "man," "Christian" terms
- Educational filtering changes bias character: "woman" associations shift from "dating" to "pregnancy, mother, family"
- Bias doesn't disappear, just transforms—data curation shapes model "worldview"
- Transparency about limitations is itself a contribution to the field

## Slide 11: Question for You

Can the open-source community escape the paradox of depending on closed commercial models (like Llama 3) to create open datasets—will future open models become powerful enough to label training data for the next generation, creating a self-sustaining flywheel that lets open AI catch up or even surpass closed systems?
