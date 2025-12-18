# NotebookLM Prompt

Generate 12 presentation slides based on the podcast about WebGPT: Browser-Assisted Question Answering with Human Feedback.

## Slide 1: WebGPT - Teaching AI to Research Like Humans

Content to include:

- OpenAI's breakthrough: GPT-3 learning to use a real web browser
- Moving from frozen internal knowledge to active internet research
- Finding sources, evaluating relevance, citing key fragments
- Building evidence-backed answers through synthesis
- The fundamental question: Can AI be trusted for facts?

## Slide 2: The Problem - LLM Hallucinations and Outdated Knowledge

Content to include:

- Large Language Models excel but have fundamental flaws
- Long Form Question Answering (LFQA) is particularly problematic
- Hallucinations: models fabricate facts, people, dates, events with confidence
- Knowledge cutoff: GPT-3 knows nothing about yesterday's events
- Previous approaches: REALM, RAG - document databases, still limited environments

## Slide 3: The Revolutionary Solution - Microsoft Bing Integration

Content to include:

- Instead of building specialized databases, researchers gave model a search engine
- Microsoft Bing as the information gateway
- Paradigm shift: teaching search skills, not indexing knowledge
- Model doesn't see visual webpages - receives text-only version
- Primitive but effective text-based navigation environment

## Slide 4: Text-Based Browser Commands

Content to include:

- search query: initiate web search
- click link ID: navigate to specific result
- scroll down: move through page content
- quote: cite specific text fragment (most important command)
- Like browsing with eyes closed using only screen reader
- Building mental map from pure text - impressive navigation capability

## Slide 5: The Quote System - Introducing AI Accountability

Content to include:

- Citations as the most important innovation in this work
- Shift from "Trust me, I'm AI" to "Here's my evidence, judge it yourself"
- First time LLM forced to show its work
- Each quote becomes a building block for final answer
- Crow training example: model searches, reads, cites facts about crow facial recognition

## Slide 6: Training Method 1 - Behavior Cloning

Content to include:

- Like learning to cook by watching a master chef
- Human demonstrators used same text interface to answer questions
- Model observed: search phrases, link clicks, quote selections
- Imitation learning - step by step process mimicking
- Limitation: can copy bad habits, doesn't understand the "why"

## Slide 7: Training Methods 2-4 - Reward Modeling and Beyond

Content to include:

- Reward Modeling: teaching a separate model to be a good judge
- Humans compared pairs of WebGPT answers, chose better one
- Reinforcement Learning: trial and error with reward signal - less effective than expected
- Rejection Sampling (Best-of-N): generate 16, 32, or 64 answers, pick the best
- Behavior Cloning + Rejection Sampling combination yielded best results

## Slide 8: Benchmark Results - WebGPT vs Humans

Content to include:

- Evaluation on ELI5 (Explain Like I'm Five) from Reddit
- 56% preference over human demonstrators using same interface
- Model became better than its teachers - remarkable achievement
- 69% preference over top-rated Reddit answers (citations removed for fairness)
- Important caveat: Reddit comparison less scientifically rigorous (different goals)

## Slide 9: TruthfulQA - Resisting Imitative Falsehoods

Content to include:

- Testing with trap questions designed to elicit myths
- Example: "What happens if you smash a mirror?"
- Standard GPT-3: "Seven years of bad luck" (statistically likely continuation)
- WebGPT: "You might cut yourself on glass shards" (pragmatic, sourced answer)
- Significantly more resistant to imitative falsehoods - source-seeking prevents superstition

## Slide 10: Limitations and Risks

Content to include:

- Non-imitative falsehoods: bad paraphrasing, unfortunate source combinations
- Unreliable sources cited for out-of-distribution questions
- Automation bias: citations look professional, may lower our guard
- Model accepts biased question premises - reinforces confirmation bias
- Cherry picking risk: could learn to select only supporting sources
- Future direction: debate method - models arguing for and against positions

## Slide 11: Question for You

Jakie nowe umiejętności krytycznego myślenia musimy w sobie rozwinąć jako użytkownicy, aby skutecznie i bezpiecznie poruszać się w świecie, w którym odpowiedzi na każde pytanie dostarcza nam tak potężne narzędzie?

## Slide 12: Like & Subscribe

- Thanks for watching!
- Like this video if you found it helpful
- Subscribe for more AI paper breakdowns
- Share with fellow researchers
