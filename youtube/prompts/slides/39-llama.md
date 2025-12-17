# NotebookLM Prompt

Generate 11 presentation slides based on the podcast about **LLaMA: Open and Efficient Foundation Language Models** (Meta AI, February 2023).

## Slide 1: LLaMA - Revolutionary Thesis
Content to include:
- Meta AI's heretical claim: smaller models trained longer can beat larger ones
- LLaMA 13B outperforms GPT-3 175B (10x smaller) on most benchmarks
- Trained exclusively on publicly available data (100% transparency)
- Paradigm shift from training cost optimization to inference cost optimization
- One of the most influential papers in open-source AI history

## Slide 2: Training Budget vs Inference Budget
Content to include:
- Traditional approach: optimize for training compute budget (one-time massive investment)
- LLaMA hypothesis: inference budget is the real bottleneck (millions of daily queries)
- Smaller model trained on more data = cheaper and faster at inference time
- 7B model performance continued improving even after 1 trillion tokens
- Fundamental change in AI economics: "What model at level X is cheapest to run at scale?"

## Slide 3: Training Data Composition (1.4T Tokens)
Content to include:
- 100% publicly available data (contrast with GPT-3's mysterious "Books2" dataset)
- Common Crawl: 67% (filtered for quality)
- C4: 15% (another cleaned Common Crawl version)
- GitHub code: 4.5%
- Wikipedia (20 languages): 4.5%
- Books (Gutenberg + Books3): 4.5%
- ArXiv scientific papers: 2.5%
- Stack Exchange Q&A: 2%

## Slide 4: Architecture - Intelligent Evolution
Content to include:
- Not a revolution but smart optimization of existing Transformer architecture
- Three proven improvements combined ("engine tuning, not new engine design")
- Pre-normalization with RMSNorm for training stability
- SwiGLU activation function (borrowed from PaLM)
- Rotary Position Embeddings (RoPE)
- Each improvement individually documented, but powerful when combined

## Slide 5: Key Architectural Improvements
Content to include:
- Pre-normalization with RMSNorm: prevents gradient explosion/vanishing during multi-week training
- SwiGLU activation: replaces ReLU, provides measurable efficiency gains
- RoPE (Rotary Position Embeddings): relative positioning instead of absolute
- RoPE enables better understanding of word relationships in long sequences
- "Small changes, big effects" philosophy throughout

## Slide 6: Engineering Optimizations
Content to include:
- xFormers library for efficient attention implementation
- Avoids storing massive attention matrices in memory
- Activation checkpointing: saves only key intermediate results
- Recomputes activations on-the-fly during backward pass
- Enabled training 65B model in just 21 days
- Massive memory savings made project feasible at this scale

## Slide 7: Benchmark Results - The David vs Goliath Moment
Content to include:
- LLaMA 13B beats GPT-3 175B on most benchmarks (10x smaller model!)
- Common sense reasoning: HellaSwag, WinoGrande superiority
- Closed-book QA: TriviaQA - proves denser, better-organized knowledge
- Smaller model trained longer = more knowledge per parameter
- Runs on single powerful consumer GPU (with effort)

## Slide 8: LLaMA 65B vs Industry Giants
Content to include:
- Fully competitive with Chinchilla 70B across most tasks
- Outperforms Chinchilla on most common sense reasoning benchmarks
- GSM8K math benchmark: beats specialized Minerva 62B (fine-tuned on math!)
- Generalist defeats specialist in its own domain
- MMLU weakness: lower scores due to less book/scientific data (177GB vs 2TB)

## Slide 9: Limitations - Toxicity & Bias
Content to include:
- Real Toxicity Prompts benchmark: toxicity increases with model size
- LLaMA 65B generates more toxic content than LLaMA 7B
- CrowS-Pairs: stereotypes measured in 9 categories, high bias in religion
- WinoGender: gender bias in occupation associations
- More errors when gender contradicts stereotypes (male nurse, female engineer)
- Models mirror both knowledge and societal biases from training data

## Slide 10: Impact & Instruction Fine-Tuning Preview
Content to include:
- Democratization of LLM research: open weights released to scientific community
- Universities, startups, small teams can now conduct frontier research
- Explosion of open-source AI innovation (foundation for many subsequent models)
- LLaMA-I preview: instruction fine-tuning boosts MMLU from 63.4% to ~69%
- Signal that base models need alignment for real-world utility
- Changed AI economics permanently: inference efficiency matters most

## Slide 11: Question for You
Content to include:
- By building ever more powerful models on data from the entire internet, are we creating better tools for understanding the world, or rather increasingly perfect mirrors that uncritically reflect all its imperfections? And how do we wisely scale capabilities without proportionally scaling potential harms?
