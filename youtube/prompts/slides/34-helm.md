# NotebookLM Prompt

Generate 11 presentation slides based on the podcast about **HELM: Holistic Evaluation of Language Models** (Stanford, 2022).

---

## Slide 1: The Evaluation Problem

Content to include:

- Before HELM: comparing LLMs was like comparing athletes from different sports (tennis vs swimming)
- Original papers for leading models (e.g., T5 vs Anthropic) had zero overlapping benchmarks
- Different labs measured different things (like car manufacturers comparing acceleration vs fuel efficiency)
- Result: meaningful comparison between models was impossible
- HELM from Stanford aimed to create the first "AI Olympics" with standardized evaluation

## Slide 2: HELM's Three Pillars

Content to include:

- **Pillar 1: Broad Coverage** - map wide capability space while acknowledging gaps (e.g., missing dialects, non-English languages)
- **Pillar 2: Multi-Metric Approach** - replace single Accuracy metric with comprehensive evaluation
- **Pillar 3: Standardization** - same conditions for all 30 models from 12 companies (AI21 Labs, Google, Meta, OpenAI, Microsoft, Anthropic)
- All models evaluated using identical few-shot prompting methodology
- Coverage jumped from 17.9% to 96% of key scenarios

## Slide 3: Seven Evaluation Metrics

Content to include:

- **Accuracy** - correctness of responses
- **Calibration** - does the model know when it doesn't know? (critical for medical/legal applications)
- **Robustness** - stability under input perturbations (typos, rephrasing)
- **Fairness** - equitable performance across demographic groups
- **Bias** - systematic skews in outputs
- **Efficiency** - computational requirements
- Each metric measured across 16 main scenarios

## Slide 4: Open Source vs Closed Access Gap

Content to include:

- Consistent performance gap between open-source and limited-access models
- Top performers: Text-Davinci-002 (OpenAI), TNLG v2 (Microsoft) - both closed
- Accessibility comes with performance cost
- This finding has implications for democratization of AI capabilities
- Proprietary training data and methods remain significant advantages

## Slide 5: Complex Metric Relationships

Content to include:

- Accuracy and Calibration showed unexpected, context-dependent relationships
- **HellaSwag scenario**: higher accuracy = worse calibration (digital Dunning-Kruger effect)
- **OpenBookQA scenario**: opposite pattern - accuracy improvements correlated with better calibration
- No universal rule: behavior depends on task context
- Cannot say "model has good calibration" - must ask "good calibration for which task?"

## Slide 6: Code Training Transfers to Reasoning

Content to include:

- Code-trained models unexpectedly excel at natural language reasoning
- **GSM8K math test results**:
  - Code-Davinci-002: 52.1% accuracy
  - Text-Davinci-002: 35% accuracy (same model family, text-only)
- 17+ percentage point gap - not statistical noise
- Hypothesis: strict logical structure of code teaches abstract reasoning
- Analogy: learning Latin improves logical puzzle-solving ability

## Slide 7: Catastrophic Prompt Sensitivity

Content to include:

- Most shocking finding: format changes cause performance collapse
- **OPT-175B on HellaSwag benchmark**:
  - Separate answer evaluation format: 79.1% accuracy
  - Combined ABCD multiple choice format: 30.2% accuracy
- Same model, same knowledge, same task - only format changed
- 30.2% is below random chance (25% for 4 options)
- Raises fundamental question: are we measuring knowledge or template-matching?

## Slide 8: Beyond Model Size

Content to include:

- Size matters within model families (larger GPT-3 variants outperform smaller ones)
- Size doesn't predict performance across different families
- Top performers had 50B+ parameters, but Anthropic's LM v4 S3 (52B) beat much larger models
- **Key factors beyond size**:
  - Training data quality and composition
  - Post-training methods: Instruction Tuning, RLHF (Reinforcement Learning from Human Feedback)
- Quality of "upbringing" may matter more than raw "brain size"

## Slide 9: Implications for AI Users

Content to include:

- Best model on leaderboard may not be best for your specific use case
- Real-world usefulness depends on how well model interprets human intentions
- Future model selection may prioritize "character" over raw benchmark scores
- **Prompt Engineering** emerges as critical skill - "art of communication with non-human intelligence"
- Model-prompt compatibility may matter more than absolute capability

## Slide 10: HELM's Limitations & Future

Content to include:

- **English dominance** - limited multilingual evaluation
- **Data Contamination** - critical unresolved problem
  - Models may have trained on test data ("seeing exam questions before the test")
  - Training data secrecy prevents verification
  - Evaluation may be based on faith, not facts
- HELM designed as "living benchmark" - continuous evolution planned
- Call for greater transparency from model creators

## Slide 11: Question for You

If a powerful model's performance completely collapses due to a minor formatting change in the question - are we measuring genuine reasoning and world knowledge, or just an incredibly advanced but ultimately blind pattern-matching ability?
