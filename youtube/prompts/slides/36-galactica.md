## NotebookLM Prompt

Generate 11 presentation slides based on the podcast about **Galactica: A Large Language Model for Science** (Meta AI, 2022).

### Slide 1: The Scientific Information Crisis

Content to include:

- Vannever Bush's 1945 essay "As We May Think" warned about information overload
- By May 2022: 516 papers submitted daily to arXiv alone
- Current search tools follow "store and point" paradigm - show 1000 doors but don't explain connections
- Galactica's thesis: LLM can become single neural network interface to scientific knowledge
- Paradigm shift: instead of searching external library, ask a librarian who read everything

### Slide 2: Curated Corpus - Quality Over Quantity

Content to include:

- 106 billion tokens of carefully selected scientific data
- 48+ million scientific papers, textbooks, lecture notes
- Specialized databases: PubChem (chemical compounds), UniProt (protein sequences)
- Contrast with PaLM: 50% of its corpus is social media conversations
- "Normative approach" - conscious decision about what constitutes valuable knowledge
- Philosophy: curate like archivists, not vacuum like web crawlers

### Slide 3: Learning the Languages of Science - Special Tokens

Content to include:

- Citations wrapped in `[startref]` and `[endref]` tokens - model learns citation graph structure
- Chemistry: `[start_smiles]` token enables learning molecular grammar (e.g., C1=CC=CC=C1 as benzene)
- Character-level tokenization for molecular structures
- Amino acid sequences marked with `[start_amino]` token
- Model learns to understand these as structured objects, not random character strings
- Enables cross-domain reasoning between text, chemistry, and biology

### Slide 4: The <work> Token - Thinking Out Loud

Content to include:

- `<work>` token acts as "digital scratch paper" for step-by-step reasoning
- Inspired by human problem-solving: we don't give instant answers to complex math
- When encountering reasoning tasks, model generates intermediate steps before final answer
- Critical innovation for mathematical and logical reasoning capabilities
- Enables chain-of-thought style reasoning during inference

### Slide 5: Mathematical Reasoning Benchmarks

Content to include:

- MMLU benchmark (university-level exam across domains): Galactica 120B achieves 41.0%
- Chinchilla (compute-optimal model) comparison: 35.7%
- MATH benchmark (advanced mathematics): Galactica 120B scores 24.0%
- PaLM 540B (4x larger model) scores only 8.8% on MATH
- Even Galactica 30B (18x smaller than PaLM) outperforms PaLM on MATH
- Key insight: parameter count alone doesn't determine reasoning ability

### Slide 6: Knowledge Probes and Domain Tasks

Content to include:

- LaTeX equation generation from name (e.g., "Schrödinger equation" → LaTeX code)
- Galactica 120B: 68.2% accuracy vs GPT-3 text-davinci-002: 49.0%
- Chemical reaction product prediction: 43.1% accuracy
- IUPAC naming (systematic chemical nomenclature): 39.2% accuracy in self-supervised setting
- Attention mechanism is interpretable: when generating "amino", model focuses on -NH2 group
- When generating "thiazole", attention focuses on sulfur atom in ring

### Slide 7: Citation Prediction - New Interface to Literature

Content to include:

- Task: predict which papers should be cited given a text paragraph
- Galactica 120B achieves 36.6% accuracy
- Specialized Dense Retriever (state-of-the-art search tool): only 8.2%
- LLM is 4x better than dedicated citation tool
- As model scales, hallucination decreases - suggests more niche but relevant papers
- Step toward discovering hidden connections in scientific literature

### Slide 8: Counter-Intuitive Finding - Epoch Repetition Works

Content to include:

- Chinchilla scaling laws (DeepMind) established dogma: never repeat data, always use unique tokens
- Repetition supposedly leads to overfitting - memorization without generalization
- Galactica trained for 4+ epochs - each text seen multiple times
- Result: continued improvement on both in-domain AND out-of-domain tasks
- Hypothesis: scaling laws apply to noisy internet data, not dense scientific corpora
- High-quality data benefits from deeper processing through repetition

### Slide 9: Counter-Intuitive Finding - Narrow Training, General Improvement

Content to include:

- Narrow scientific training improves performance on general (non-scientific) tasks
- Big Bench benchmark (mostly non-scientific tasks): Galactica 120B scores 48.7%
- OPT 175B (general model): 43.4%
- BLOOM 176B (general model): 42.6%
- Scientific knowledge builds stronger reasoning foundations than random internet text
- Analogy: learning Latin and Greek improves understanding of modern languages
- Challenges "vacuum the entire internet" philosophy of model training

### Slide 10: Real-World Applications - Chemistry and Biology

Content to include:

- IUPAC naming: self-supervised 39.2% accuracy on complex systematic nomenclature
- Attention visualization shows structural understanding (not black box)
- Protein annotation: automatically describe protein function from amino acid sequence
- Case study: African elephant transmembrane regulator protein (not in training data)
- Model correctly generated keywords: "ATP binding", "chloride channel", "transmembrane"
- Transferred knowledge from horse protein (91.8% sequence similarity)
- Automating work currently done by thousands of biologist curators

### Slide 11: Question for You

Since Galactica can already read genetic code and chemical formulas, what will happen when we teach it to see? When we give it access to images from the Hubble telescope, electron microscopes, and MRI scans - and allow it to connect this visual data with all the textual knowledge it already possesses - how will that fundamentally change the way we make scientific discoveries?
