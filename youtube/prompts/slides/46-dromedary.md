# NotebookLM Prompt

Generate 11 presentation slides based on the podcast about "Principle-Driven Self-Alignment of Language Models from Scratch with Minimal Human Supervision" (Dromedary).

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

### Slide 1: The Holy Grail of AI Alignment
Content to include:
- Current alignment dominance: Supervised Fine-Tuning (SFT) and RLHF (Reinforcement Learning from Human Feedback)
- Critical problem: both methods require massive human-annotated datasets (tens to hundreds of thousands of examples)
- Cost and inconsistency: expensive process, human annotators introduce biases and inconsistencies
- Dromedary's claim: achieved results with fewer than 300 lines of human annotation
- Paradigm shift: teaching principles instead of showing thousands of examples

---

### Slide 2: The Self-Align Method Overview
Content to include:
- Four-stage pipeline for self-alignment from scratch
- Stage 1: Topic-Guided Red-Teaming Self-Instruct
- Stage 2: Principle-Driven Self-Alignment
- Stage 3: Principle Engraving
- Stage 4: Verbose Cloning
- Key innovation: model teaches itself using only 16 human-written principles

---

### Slide 3: Stage 1 - Topic-Guided Red-Teaming Self-Instruct
Content to include:
- Model generates its own training tasks/instructions
- Starts with only 195 seed prompts
- Red teaming concept: intentionally attacking system to find weaknesses
- 20 adversarial categories: future events, scientific knowledge, cultural understanding, harmful content provocation
- Output: 360,000 synthetic, highly diverse queries
- Model becomes its own most demanding critic

---

### Slide 4: Stage 2 - Principle-Driven Self-Alignment
Content to include:
- Only 16 human-written high-level principles (e.g., "be helpful and harmless", "act ethically", "admit ignorance")
- 5 concrete in-context learning examples
- Key innovation: Internal Thoughts mechanism
- Model reasons about which principles apply BEFORE generating response
- Example: "Who will be US president in 2025?" → model thinks about knowledge cutoff, honesty principle, then responds appropriately
- Preventive approach vs post-hoc correction

---

### Slide 5: Stages 3 & 4 - Principle Engraving and Verbose Cloning
Content to include:
- Principle Engraving: fine-tuning on self-generated high-quality responses
- Principles and examples removed from context during inference
- Goal: engrave principles directly into model parameters (becomes "second nature")
- Verbose Cloning: addresses overly concise responses after engraving
- Context distillation technique: model learns from its more verbose self
- Result: more eloquent and detailed responses while maintaining safety

---

### Slide 6: Self-Align vs Constitutional AI (Anthropic)
Content to include:
- Self-Align: works from scratch; Constitutional AI (CAI) requires initial RLHF training
- Self-Align: preventive ("think before you speak") - principles considered before response
- CAI: post-factum ("speak then think") - self-critique and revision after generation
- Technical difference: Self-Align limited by context window for 16 principles
- CAI has no such limit - constitution can be much longer and more detailed
- Different philosophies: proactive vs reactive alignment

---

### Slide 7: Benchmark Results - TruthfulQA and Safety
Content to include:
- TruthfulQA MC-1 (multiple choice): 69% accuracy - surpasses GPT-4
- TruthfulQA generation task: better than Alpaca and LLaMA, behind Vicuna (trained on ChatGPT data)
- Big Bench HH Eval - Harmlessness score: 0.91
- Comparison: LLaMA 0.71, Alpaca 0.76, ChatGPT 0.95
- Extremely close to ChatGPT on safety metrics
- Conversation quality: ~89% of ChatGPT quality
- Better than text-davinci-003 and Alpaca, behind Vicuna and ChatGPT

---

### Slide 8: The Verbose Tax - A Counter-Intuitive Discovery
Content to include:
- Verbose Cloning improves helpfulness but degrades truthfulness scores
- Trade-off discovered: more eloquent responses = lower precision on factual tasks
- Fundamental conflict between being good conversationalist and reliable fact source
- Process making responses more natural may introduce speculation/noise
- Key insight: Alignment is not one-dimensional
- Optimizing for one metric comes at cost of another

---

### Slide 9: Limitations and Failure Cases
Content to include:
- Knowledge limited to LLaMA's training data (cutoff 2021)
- Weather question failure: recited Wikipedia climate data instead of admitting no real-time access
- Author biography hallucination: created completely false biography for Zhiqing Sun
- Violated Candor Rule despite principles being "engraved"
- Defining 16 ethical principles is philosophically challenging ("who decides what's ethical?")
- Model can still replicate hidden biases from original training data

---

### Slide 10: Implications and Future of AI Alignment
Content to include:
- New paradigm: "First Align, Then Follow" vs traditional "First Follow, Then Align"
- Values first, then specific skills (like child education)
- Democratization: minimal human/financial input opens doors for startups, universities, smaller teams
- More transparent control than RLHF "black box"
- Authors released code, LoRA weights, and data publicly
- Open question: Can universal ethical AI principles exist across cultures and legal systems?
- Future possibility: mosaic of models aligned to different local value systems (European, Chinese, American)

---

### Slide 11: Question for You
Display the question:

"Can a universal set of ethical principles for AI be created that will be globally accepted - across different cultures, legal systems, and social contexts? Or will AI's future be a mosaic of models aligned to different local value systems?"
