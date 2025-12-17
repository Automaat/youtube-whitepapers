## NotebookLM Prompt

Generate 11 presentation slides based on the podcast about the LLaMA 3 paper "The Llama 3 Herd of Models" from Meta.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

### Slide 1: LLaMA 3 Overview
Content to include:
- Flagship model: 405 billion parameters (Dense Transformer architecture)
- Training corpus: 15 trillion tokens (vs 1.8T in LLaMA 2)
- Context window: 128,000 tokens
- Dense architecture (not Mixture of Experts) - proven approach perfected
- Designed from scratch for coding, reasoning, and multilingual capabilities

### Slide 2: Three Pillars of Success
Content to include:
- Pillar 1: Data quality - obsessive curation and filtering
- Pillar 2: Scale - 50x more compute than largest LLaMA 2
- Pillar 3: Complexity management - engineering and organizational excellence
- Key thesis: Evolution and refinement of existing methods beats chasing novelty
- No architectural revolution needed - standard Transformer perfected

### Slide 3: Pre-training Data Pipeline
Content to include:
- Multi-stage rigorous filtering process
- Removed entire domains with PII or unsafe content
- Custom HTML parser for clean text extraction
- Aggressive deduplication at multiple levels: URL, document (minHash), line-level
- Goal: Maximum uniqueness of every piece of information

### Slide 4: LLaMA 2 as Quality Judge
Content to include:
- Used previous LLaMA 2 models to classify data quality
- Trained LLaMA 2 to recognize high-quality text
- Automated classification of massive datasets
- "Curator" preparing library for smarter successor
- Self-bootstrapping approach - model helps create its successor

### Slide 5: Data Mix and Scaling Laws
Content to include:
- Carefully composed training diet: ~50% general knowledge, 25% math/reasoning, 17% code, 8% multilingual
- Proportions calculated using scaling laws experiments
- Predict impact of diet changes on final model capabilities before spending millions
- Data engineering becoming more important than model architecture engineering
- Future: perfecting training diet composition for specific goals

### Slide 6: Architecture Improvements
Content to include:
- Grouped Query Attention (GQA) - significantly speeds up response generation
- Special attention mask for document separation in long contexts
- Prevents information mixing between multiple documents in single query
- Maintains coherence in long context processing
- Quiet but important optimizations to standard Transformer

### Slide 7: Training at Scale - Engineering Challenges
Content to include:
- Training on clusters with up to 16,000 H100 GPUs
- 54 days of training with 419 unexpected interruptions
- Effective training time exceeded 90% despite failures
- Daily 1-2% performance fluctuation caused by ambient temperature in data center
- Shows extreme sensitivity of these systems to environmental factors

### Slide 8: Post-Training Techniques
Content to include:
- Supervised Fine-Tuning (SFT) and Direct Preference Optimization (DPO)
- Rejection sampling: model generates ~10 responses, Reward Model selects best one
- Code training: synthetic data with execution feedback - learning from practical errors
- Math training: step-by-step solutions with self-verification mechanisms
- 128K context: only 0.1% synthetic long-context examples needed (microscopic intervention, huge results)

### Slide 9: Benchmark Results - Two Faces
Content to include:
- Leader in specialized benchmarks: GSM-8K (mathematical reasoning), HumanEval Plus (coding)
- Surpasses GPT-4 in several domains
- Human evaluations show more nuanced picture - on par with GPT-4
- Mixed results vs GPT-4O and Claude 3.5 Sonnet in general helpfulness
- Era of one universally best model may be over - choice depends on specific use case

### Slide 10: Multimodality and Safety
Content to include:
- Compositional approach: attached image/speech modules via lightweight adapters
- Preserves text model performance while adding new capabilities
- LLaMA 3V outperforms GPT-4V on all tested visual benchmarks
- Safety: pre-training data filtering + safety fine-tuning + LLaMA Guard 3 classifier
- Balance: block harmful content without absurd refusals on harmless questions

### Slide 11: Question for You
How do we design companies, processes, and teams capable of building objective, trustworthy, and truly intelligent machines? Perhaps this is the real challenge for the next decade.
