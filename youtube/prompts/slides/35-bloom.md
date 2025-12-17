# NotebookLM Prompt

Generate 11 presentation slides based on the podcast about the BLOOM paper (BigScience Large Open-science Open-access Multilingual Language Model).

## Slide 1: Introduction to BLOOM
Content to include:
- BLOOM: 176 billion parameter open multilingual language model
- Created by BigScience project - over 1,000 researchers from 38 countries
- Not just ML specialists: linguists, lawyers, philosophers, sociologists
- Open collaboration model vs closed corporate development
- Fully Open Access from day one
- New paradigm for AI development - radically open approach

## Slide 2: The Problem BLOOM Addresses
Content to include:
- Pre-BLOOM: LLMs exclusive to wealthy organizations behind closed doors
- Massive barrier for external researchers
- Near-total focus on English language
- Authors explicitly address "social limitations of LLM development"
- Goal: democratization of LLM technology
- Model must be Open Access AND truly multilingual

## Slide 3: Ethical Charter in Practice
Content to include:
- BigScience governed by Ethical Charter from the start
- Not just a PDF on a website - actually enforced
- Manual, intentional curation of data sources instead of scraping the web
- Collaboration with Masakhane (African languages) and Latinx in AI
- Conscious inclusion of underrepresented languages
- Technical decisions driven by values - cost time and money but maintained principles

## Slide 4: The ROOTS Corpus
Content to include:
- 1.61 terabytes of curated text data
- 46 natural languages + 13 programming languages
- Human-supervised data collection process
- Contrast with typical automatic filtering that removes LGBTQ+ content or African American English
- Official permissions from some publishers (e.g., Le Monde newspaper)
- Different level of source care than industry standard

## Slide 5: Architecture - Decoder-Only Transformer
Content to include:
- Base architecture: Decoder-Only Transformer (similar to GPT series)
- Pragmatic choice: experiments showed best zero-shot generalization post-training
- Two key modifications for stability at scale
- Engineering reality: keeping training alive is the priority
- "Don't break it" over "maximize benchmark scores"

## Slide 6: ALiBi Positional Embeddings
Content to include:
- Traditional methods: assign fixed "address" to each word (position 1, 2, 3...)
- ALiBi: relative approach - "this word is nearby, that one is far away"
- Directly weakens attention scores based on distance
- More flexible than absolute position encoding
- Research shows more stable training and better results
- Key innovation for handling long sequences

## Slide 7: Embedding Layer Norm Trade-off
Content to include:
- Additional Layer Normalization after input embedding layer
- Added to improve training stability at massive scale
- Counterintuitive: slightly WORSE zero-shot performance in smaller model tests
- Consciously added despite performance hit
- Priority: guarantee training completes vs squeeze extra benchmark points
- Example of theory vs engineering reality at scale

## Slide 8: Tokenization Strategy
Content to include:
- Byte Level BPE algorithm with ~250,680 token vocabulary
- Byte-level: never encounters unknown characters (critical for 46 languages)
- No text normalization (e.g., NFKC) - model learns raw, uncleaned data
- Rejected Anglo-centric rules (e.g., around contractions like "n't", "'ll")
- Goal: maximum language neutrality
- Handles diverse scripts and symbols naturally

## Slide 9: Benchmark Results and Multilingual Performance
Content to include:
- SuperGLUE (English-only): comparable to OPT and similar scale models
- Multilingual training didn't hurt English performance
- Zero-shot to one-shot: larger improvement than competitors (context helps focus)
- FLORES-101 translation: competed with specialized supervised translation models
- Translated Galician despite never seeing it in training (transfer from Spanish/Portuguese)
- Weakness: low-resource languages (Swahili, Yoruba) still struggle - data quantity matters

## Slide 10: BLOOMZ and Environmental Impact
Content to include:
- BLOOMZ: multitask prompted fine-tuning on xP3 multilingual dataset
- Dramatic zero-shot improvement on unseen tasks vs base BLOOM
- From "knowledge" to "action" - learning to follow instructions
- Environmental transparency: ~25 tons CO2 equivalent (vs 500+ for GPT-3)
- 20x reduction due to Jean-Zay supercomputer in France (nuclear power)
- Strategic data center choice matters for AI's ecological cost

## Slide 11: Question for You
Does relentlessly scaling models toward ever more parameters always make them smarter in every way? Or in the chase for bigger models, are we losing subtle, more fundamental linguistic capabilities along the way - and what does this mean for the future of AI that should truly understand language, not just generate fluent text?
