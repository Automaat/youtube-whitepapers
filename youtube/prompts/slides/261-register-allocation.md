Generate 11 presentation slides based on the podcast about Register Allocation.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Register Allocation Problem
- Compiler must assign unlimited virtual registers to limited physical CPU registers
- CPU registers are fastest memory access (faster than RAM by orders of magnitude)
- Poor allocation forces expensive memory spills (storing values in RAM)
- Balance: minimize memory access while maximizing register utilization
- Critical optimization impacting program performance

## Slide 2: Early Approaches and Their Limitations
- Initial compilers used simple heuristics for register assignment
- Naive allocation generated unnecessary copy instructions
- Performance penalty from both extra instructions and memory spills
- IBM research showed existing techniques were inadequate for production compilers
- Need for systematic, graph-based approach became apparent

## Slide 3: Liveness Analysis Fundamentals
- Value is "live" when it holds data needed by future instructions
- Liveness intervals determine when registers must be preserved
- Two values with overlapping liveness cannot share same register
- Precise liveness analysis reduces unnecessary register pressure
- Forms foundation for interference graph construction

## Slide 4: Graph Coloring Formulation
- Each virtual register becomes a node in interference graph
- Edge connects nodes if their liveness intervals overlap
- Graph coloring assigns colors (physical registers) to nodes
- Adjacent nodes must receive different colors
- k-colorability determines if allocation succeeds with k registers

## Slide 5: NP-Completeness Challenge
- General graph k-coloring is NP-complete problem
- Exact solutions infeasible for large programs
- Early attempts used expensive optimization algorithms
- Compilation time exploded for real-world code
- Heuristics necessary for practical implementation

## Slide 6: Chaitin's Revolutionary Insight
- Observation: don't need optimal coloring, just good enough
- Greedy algorithm with smart node ordering
- Simplify graph by removing nodes with degree < k
- Recurse until graph empty or stuck
- Rebuild graph in reverse, assigning colors opportunistically

## Slide 7: Spilling Strategy
- When coloring fails, some values must spill to memory
- Cost function estimates impact of spilling each candidate
- Priority based on: loop nesting depth, usage frequency, lifetime length
- Generate store/load instructions around spilled value uses
- Rebuild interference graph and retry allocation

## Slide 8: Coalescing Optimization
- Eliminate unnecessary copy instructions (mov operations)
- Merge copy-related nodes if they don't interfere
- Reduces both instruction count and register pressure
- Conservative coalescing prevents creating uncolorable graphs
- Significant performance improvement in practice

## Slide 9: Iterative Refinement Process
- Build initial interference graph from liveness analysis
- Attempt greedy coloring with simplification
- On failure: select spill candidates using cost function
- Insert spill code and regenerate graph
- Repeat until successful coloring achieved

## Slide 10: Impact and Modern Extensions
- Became standard technique in production compilers
- Enabled efficient code generation for RISC architectures
- Modern variants: linear scan, SSA-based allocation, trace-based methods
- Trade-offs between compilation time and code quality
- Still active research area with incremental improvements

## Slide 11: Question for You
Could we radically simplify compiler optimization if we found the right interference graph representation and cost function?
