# NotebookLM Prompt

Generate 11 presentation slides based on the podcast about **"Training language models to follow instructions with human feedback" (InstructGPT, OpenAI 2022)**.

---

## Slide 1: The Alignment Problem

Content to include:

- Large language models (LLMs) don't understand user intentions despite being powerful
- Misalignment: models fulfill requests literally, ignoring actual intent
- Models generate outputs that are untruthful, toxic, or simply unhelpful
- The goal: create models that are Helpful, Honest, and Harmless (3H safety framework)
- Revolutionary approach: don't build bigger models, train smarter with RLHF

---

## Slide 2: The Shocking Result - Size Doesn't Matter

Content to include:

- InstructGPT with only 1.3B parameters outperformed original GPT-3 with 175B parameters
- Over 100x smaller model preferred by human evaluators
- Completely contradicts "bigger is better" philosophy dominant at the time
- Quality of training and alignment to user intent can outweigh raw model capacity
- Training methodology matters more than parameter count

---

## Slide 3: The RLHF Pipeline - Three Steps

Content to include:

- Reinforcement Learning from Human Feedback (RLHF) as the core method
- Step 1: Supervised Fine-Tuning (SFT) - teaching the format
- Step 2: Reward Model training - building a digital judge
- Step 3: Reinforcement Learning with PPO - optimization loop
- Entire process based on feedback from 40 trained human labelers

---

## Slide 4: Step 1 - Supervised Fine-Tuning (SFT)

Content to include:

- Labelers write ideal responses from scratch for real API prompts
- High-quality dataset created: prompt-response pairs
- GPT-3 fine-tuned on these exemplary answers
- Like showing a student perfectly solved problems
- Teaches format and style, but not evaluation or judgment
- Foundation layer - necessary but insufficient alone

---

## Slide 5: Step 2 - Reward Model Training

Content to include:

- Model generates 4-9 different responses per prompt
- Labelers rank responses from best to worst (not writing ideal answers)
- Separate reward model trained on millions of these rankings
- Reward model learns to predict which response humans prefer
- Outputs a score representing human preference
- Becomes an automated reflection of human preferences

---

## Slide 6: Step 3 - PPO Reinforcement Learning

Content to include:

- Proximal Policy Optimization (PPO) algorithm optimizes the SFT model
- Cycle: model receives prompt → generates response → reward model scores it
- PPO adjusts parameters to maximize reward scores
- Trial and error at massive scale
- Model actively explores what makes responses better
- Dynamic learning vs. static imitation

---

## Slide 7: Quantitative Results

Content to include:

- 175B InstructGPT wins against 175B GPT-3 in 85% of comparisons
- Hallucination rate dropped by 50%: from 41% (GPT-3) to 21% (InstructGPT) in closed-domain tasks
- 25% reduction in toxic outputs - but only when explicitly prompted to be respectful
- No improvement in bias on standard benchmarks
- Alignment is not monolithic - improvement in one dimension doesn't guarantee improvement in others

---

## Slide 8: The Alignment Tax Problem

Content to include:

- Initial RLHF caused performance degradation on NLP benchmarks (SQuAD, DROP)
- Model became better at conversation but worse at formal tasks
- Solution: PPO-PTX variant - mix original GPT-3 pretraining data during RL phase
- Acts as an anchor preventing model from forgetting fundamental capabilities
- Simple technique that eliminated most performance losses
- You can have both: alignment AND capability

---

## Slide 9: Generalization Beyond Training Data

Content to include:

- InstructGPT followed instructions in tasks it wasn't directly trained for
- Performed well on programming code prompts despite minimal code examples in training data
- Suggests understanding of abstract concept "following intent" - not memorization
- Public datasets (FLAN, T0) didn't reflect real-world usage patterns
- Real users primarily want: creative generation, brainstorming, open-ended conversation
- Academic benchmarks were disconnected from reality

---

## Slide 10: Fundamental Limitations

Content to include:

- Model fooled by false premises (e.g., "Why is eating socks important after meditation?")
- Tries to justify absurd requests instead of identifying the absurdity
- Overly cautious, verbose responses
- The 40 labelers problem: whose values define "good"?
- Small, demographically homogeneous group (Global North) with specific instructions
- InstructGPT behavior reflects preferences of a tiny elite, not universal human values

---

## Slide 11: Question for You

Display only this question:

**"Czy spersonalizowane AI, dopasowane do preferencji każdego użytkownika, prowadziłoby do bardziej pluralistycznej przyszłości - czy zamknęłoby nas w ostatecznych bańkach informacyjnych i echo chambers, z których nie byłoby ucieczki?"**

*(Would personalized AI, aligned to each user's preferences, lead to a more pluralistic future - or would it lock us in ultimate information bubbles and echo chambers from which there would be no escape?)*
