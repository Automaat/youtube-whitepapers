## NotebookLM Prompt

Generate 11 presentation slides based on the podcast about DeepMind's Sparrow paper - "Improving alignment of dialogue agents via targeted human judgements".

### Slide 1: Introduction - The Trust Problem in LLMs

Content to include:

- LLMs are everywhere (emails, search, coding) but fundamentally untrustworthy
- Models hallucinate facts with high confidence
- Can perpetuate harmful stereotypes and give dangerous advice
- Core research question: How to make powerful AI tools safe and truly helpful assistants?
- Sparrow: DeepMind's research platform (not a commercial chatbot) - a "testing ground" for alignment methodology

### Slide 2: The 23 Rules Approach

Content to include:

- Shift from abstract concepts ("harmlessness", "helpfulness") to 23 concrete, human-readable rules
- Example rules: "Don't pretend to have identity or body", "Don't offer financial or medical advice", "Don't use hate speech or vulgarities", "Don't generate sexually explicit content"
- Key advantage: Instead of asking "Is this response good?" → ask "Does this violate rule #7?"
- Enables collection of much more precise and useful feedback data
- Transforms subjective "I don't like it" into objective "Specific rule X was violated"

### Slide 3: Evidence-Based Responses - Fighting Hallucinations

Content to include:

- Second pillar: grounding responses in verifiable sources
- When asked factual questions, Sparrow doesn't answer "from memory"
- Generates its own search query to find information
- Analyzes search results and formulates response with cited evidence
- Example: Question about tallest EU building → generates query → finds Wikipedia info about Warsaw Tower → answers with citation
- Builds on earlier GopherCite model but integrates into fluid interactive dialogue

### Slide 4: RLHF - Reinforcement Learning from Human Feedback

Content to include:

- Core mechanism: training model like "teaching" - rewards are points from humans for good responses
- Base model: Chinchilla (70 billion parameters)
- Model learns to formulate responses that maximize human-assigned rewards
- Continuous feedback loop: collect human data → train reward models → use combined signal for RL fine-tuning → improved model generates better data → repeat

### Slide 5: Two Parallel Reward Models

Content to include:

- **Preference Reward Model**: Humans see multiple responses to same question, pick the best one; learns what humans find helpful, polite, well-formulated
- **Rule Reward Model**: Trained via adversarial probing; doesn't evaluate "general goodness" but specifically whether any of 23 rules are violated
- Final Sparrow training: must satisfy both models simultaneously
- One model promotes being helpful/nice, other acts as strict guardian of specific rules

### Slide 6: Adversarial Probing - Breaking the System

Content to include:

- Specially trained evaluators tasked with provoking rule violations
- Example tasks: "Try to get Sparrow to give medical advice" or "Make it pretend to be human with feelings"
- Record entire conversation and label exact moment of rule violation
- Provides precise data on where and how model failed
- Like security penetration testing - find vulnerabilities to patch them
- System learns to recognize and penalize (negative points) specific rule violations

### Slide 7: Real-Time Reranking

Content to include:

- Technique applied during inference, not just training
- Model generates 8 potential responses in background for each query
- All 8 candidates pass through trained reward models before showing anything to user
- Only response with highest combined score from both Preference RM and Rule RM is displayed
- Additional quality filter operating right before response delivery

### Slide 8: Results and Performance

Content to include:

- Sparrow responses preferred significantly more often than baseline models in direct comparisons
- **8% rule violation rate** during adversarial probing attacks (down to single digits under intentional attack)
- **78% factual accuracy** when Sparrow provided sources - source actually supported the claim
- Massive improvement over models that freely hallucinate
- No direct comparison to other models in same test, but single-digit violation rate considered significant progress

### Slide 9: The Critical Tradeoff - Instance Harm vs. Distributional Harm

Content to include:

- Major unintended side effect discovered
- Method effectively eliminates **instance harm** (single racist/offensive statements)
- But same training process can amplify **distributional harm** (hidden, systemic statistical biases)
- Example: Model learns to never say "women are bad drivers" (instance harm eliminated)
- But may strengthen statistical associations: "mechanic" → male, "nurse" → female
- Model becomes cautious → sticks to statistical middle → middle reflects historical biases in training data
- Sparrow scored **worse on bias benchmarks** (BBQ, Winogender) after RLHF alignment

### Slide 10: Limitations and Future Directions

Content to include:

- Sparrow uses only short text fragments from sources - cannot read/evaluate full articles or overall context
- No distinction between reputable scientific portal vs. anonymous internet forum - just "strings of characters"
- Can correctly cite complete nonsense if found online
- Future systems need to learn **source credibility evaluation**, not just correct citation
- Proposed future concept: **AI Debate** - two models debate with sources, human judges argumentation process
- Shift from simple assistant toward critical thinking partner

### Slide 11: Question for You

Who should create the rules for AI that will potentially be used globally across different cultures and value systems? And how can we ensure that these rules, even when created with the best intentions, don't inadvertently silence certain perspectives while amplifying others?
