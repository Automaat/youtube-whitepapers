# NotebookLM Prompt - Scaling Laws for Neural Language Models

Generate 10 presentation slides based on the podcast about "Scaling Laws for Neural Language Models" by Jared Kaplan et al. (OpenAI).

## Slide 1: Introduction - The Rosetta Stone of AI

Content to include:

- Paper "Scaling Laws for Neural Language Models" revolutionized AI development strategy
- Analogy: Building a huge V12 engine and running it at fraction vs. small optimized engine
- OpenAI research that "shook the foundations" of AI world
- Gave engineers a set of "physics laws" governing their universe
- Transformed AI development from alchemy to chemistry (predictable engineering)
- Green light for the race toward gigantic models we witness today

## Slide 2: Scale Over Architecture - The Fundamental Discovery

Content to include:

- Architecture shape proved secondary; parameter count is king
- Deep vs. wide models with same parameter count perform nearly identically
- Differences were at statistical error level when comparing different architectures
- Years of fine-tuning architectures were "chasing ghosts"
- Key distinction: non-embedding parameters matter, not total parameters
- Debunked traditional focus on innovative architectural designs

## Slide 3: Non-Embedding Parameters - The Brain vs. Dictionary

Content to include:

- Model has two parts: embedding layer (dictionary) and non-embedding (brain)
- Embedding parameters: translate words like "cat" or "runs" into number vectors
- Non-embedding parameters: build logical sentences and understand context
- Size of the "brain" is decisive, not the size of the "dictionary"
- Analogy: judging a writer by understanding of character relationships, not vocabulary size
- Filtering out embedding parameters revealed the clean scaling trend

## Slide 4: Power Laws - Predictable Mathematical Progress

Content to include:

- Performance follows power law (prawo potęgowe) like natural phenomena
- Same mathematical pattern as earthquake frequency vs. magnitude
- Cross-entropy loss: measures how "surprised" model is by next word (lower = better)
- Ideal model would have loss = 0 (predicts everything perfectly)
- Loss decreases predictably when scaling any of three resources: N, D, or C
- Turned AI development from guesswork into strategic engineering

## Slide 5: The Three Scaling Variables

Content to include:

- N: Number of non-embedding parameters (model size)
- D: Amount of training data (tokens)
- C: Compute budget (measured in PF-Days)
- PF-Day = petaflop (10^15 operations/second) running for 24 hours
- Smooth scaling curves span 7 orders of magnitude
- Same physical law applies from "ant to whale" - cannot be coincidence

## Slide 6: Compute-Efficient Training - The Counter-Intuitive Revolution

Content to include:

- Traditional approach: train until convergence (learning curve flattens)
- Paper proved this is "waste of resources"
- Optimal strategy: build largest possible model, stop training early
- Under-trained giant beats fully-trained small model at same compute budget
- Concept of "compute efficient training" introduced
- Completely reversed traditional engineering intuition by 180 degrees

## Slide 7: Sample Efficiency - Why Bigger Models Learn Faster

Content to include:

- Large models are like genius students - learn faster from each example
- Small models like average students - need many repetitions
- Same compute budget: large model makes much bigger progress
- Learning curve of large model descends much more steeply
- Racing car analogy: V12 reaches 500 HP faster and cheaper than perfecting small engine to 300 HP
- Even if theoretically V12 could reach 1000 HP, stopping at 500 is optimal

## Slide 8: Optimal Budget Allocation

Content to include:

- When scaling compute 1 billion times: where to invest?
- Lion's share → increasing model size
- Smaller portion → increasing batch size (examples processed at once)
- Tiny fraction → extending training time
- Research teams should build biggest affordable model and train shorter
- Foundation strategy for OpenAI, Anthropic, Google - mathematical proof for building bigger

## Slide 9: Model Size vs. Data Requirements

Content to include:

- "Big models more important than big data" - challenges "data is new oil" narrative
- 8x model size increase requires only 5x more data (not 8x)
- Compute and model size needs grow faster than data needs
- Good news: we're hitting walls on quality text data availability
- Research focus shifted to training methods (model parallelism) and specialized hardware
- Model size is the main engine of progress

## Slide 10: Limits and Open Questions

Content to include:

- Theoretical breaking point predicted at trillions of parameters
- Natural language has irreducible entropy - cannot predict everything
- Paper is empirical - describes "what" works, not "why"
- Compared to thermodynamics (macroscopic properties) vs. statistical mechanics
- Waiting for deeper theory explaining specific power law exponents
- Question: When scaling hits the wall, will we need entirely new paradigm for AGI?
