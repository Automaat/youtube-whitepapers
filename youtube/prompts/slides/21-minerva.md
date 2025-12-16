## NotebookLM Prompt

Generate 11 presentation slides based on the podcast about the Minerva paper "Solving Quantitative Reasoning Problems with Language Models" by Google Research.

### Slide 1: Minerva - LLM for Quantitative Reasoning
Content to include:
- Fundamental difference: computers excel at arithmetic but struggle with quantitative reasoning
- Quantitative reasoning = translating natural language into mathematical language
- Minerva reads math/physics/chemistry problems and generates full logical solutions
- Combines natural language with precise LaTeX mathematical notation
- Achieved average score on Polish Matura math exam - no longer just a lab curiosity

### Slide 2: Why Quantitative Reasoning is Hard for LLMs
Content to include:
- Multi-step task requiring several competencies simultaneously
- Step 1: Correctly interpret question in natural language with all nuances
- Step 2: Retrieve appropriate formulas and facts from knowledge (e.g., moment of inertia formula)
- Step 3: Execute series of symbolic and numerical calculations
- Step 4: Generate coherent, logical step-by-step explanation like a human would write
- Unlike Wolfram Alpha - Minerva must deduce formulas from context, not receive them explicitly

### Slide 3: Main Hypothesis - Data Quality Over Architecture
Content to include:
- Revolutionary idea: no new algorithm or architecture needed
- Thesis: sufficiently large LLM + high-quality technical dataset = emergent reasoning
- Model learns to reason "organically" when trained on data combining natural language with formal mathematics
- Key is quality and scale of specific technical data, not fundamental architecture changes
- "All the magic is in the data" - better training diet for the model

### Slide 4: Training Data Composition - 38.5 Billion Tokens
Content to include:
- ~50% raw scientific papers from arXiv server (physicists, mathematicians communicate)
- ~45% web pages filtered for mathematical content (MathJax format for equations)
- Only 5% general text data for maintaining linguistic fluency
- Critical detail: preserved original raw mathematical notation including LaTeX commands
- Model learned grammar of natural language parallel with grammar of mathematics

### Slide 5: Model Architecture - Fine-tuning PaLM
Content to include:
- Not built from scratch - Minerva is fine-tuned on pre-trained PaLM models
- Three sizes: 8B, 62B, and 540B parameters
- Fine-tuning = adjusting powerful general model for highly specialized task
- Model saw natural language and mathematics as inseparable whole
- Process designed to maintain ability to write full reasoning chains

### Slide 6: Majority Voting - Wisdom of the Crowd
Content to include:
- Inference technique, not training modification
- Generate 100-200 different solution attempts for same problem
- Instead of evaluating which reasoning path is most logical, check final answers
- Select answer that appears most frequently as final result
- "Ways to make mistakes are infinite, but correct answers are usually just one"
- Like brainstorming session model conducts with itself

### Slide 7: Benchmark Results - Massive Improvement
Content to include:
- MATH benchmark (high school competition level): previous SOTA 6.9% → Minerva 540B 53%
- Not incremental improvement - completely different league (like Sunday player to Champions League)
- Polish Matura exam: achieved national average level
- Improvement enabled by combination of scale + technical data + Majority Voting
- Demonstrates quantitative reasoning is learnable from data alone

### Slide 8: Physics Example - Rolling Disk Problem
Content to include:
- Task: What fraction of total kinetic energy of rolling disk is rotational kinetic energy?
- Step 1: Introduces own notation (V for velocity, I for moment of inertia)
- Step 2: Writes correct general physics formulas for translational and rotational kinetic energy
- Key moment: Correctly recalls specific formula I = ½mr² for uniform solid disk (not in problem!)
- Step 3: Executes algebraic calculations, simplifies, arrives at correct answer: 1/3
- Demonstrates application of physics knowledge, not just pattern matching

### Slide 9: Verification - Thinker or Plagiarist?
Content to include:
- Test 1: Searched training data for test questions - not found (no memorization)
- Test 2: Modified existing problems (changed numbers, rephrased) - model still solved them correctly
- Test 3: Compared solution paths using BLEU Score - low similarity to official answers
- Proves Minerva creates unique reasoning paths, not copying seen solutions
- Modified problem test most convincing - can't memorize answer to never-asked question

### Slide 10: Three Main Limitations
Content to include:
- Limitation 1: No formal verification of reasoning - can get right answer via wrong reasoning (false positives)
- Example: Getting 4 by calculating 2+3-2 instead of correct method - dangerous for science/engineering
- Limitation 2: No external tools access - can't use calculator or Python interpreter
- Like theoretical mathematician forbidden to use calculator - can prove theorem but err in simple multiplication
- Limitation 3: Black box - no direct control over what abilities emerge from training

### Slide 11: Question for You
Display only this question from the podcast:

"Kiedy sztuczna inteligencja staje się nauczycielem, pojawia się problem. Kto ocenia nauczyciela?"

("When artificial intelligence becomes a teacher, a problem arises. Who evaluates the teacher?")
