Generate 11 presentation slides based on the podcast about "Precise Interprocedural Dataflow Analysis via Graph Reachability" by Thomas Reps, Susan Horwitz, and Mooly Sagiv (1995).

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Challenge of Interprocedural Analysis
- Traditional dataflow analysis worked only within single procedures
- Real programs require tracking data flow across function calls and returns
- Previous tools either ignored interprocedural effects or were impractically slow
- This paper introduces IFDS framework: precise and efficient interprocedural analysis

## Slide 2: What Makes Interprocedural Analysis Hard
- Need to track variables not just in one function but across entire call chains
- Must handle procedure calls, parameter passing, and return values correctly
- Context-sensitivity is crucial: different call sites need different analysis results
- Naïve approaches explode in complexity or lose precision

## Slide 3: The Distributive Framework Property
- Analysis must satisfy the distributive property: f(x ∪ y) = f(x) ∪ f(y)
- This mathematical property enables efficient graph-based algorithms
- Examples: reaching definitions, live variables, truly live variables
- Separability property: effects on different variables can be analyzed independently

## Slide 4: IFDS Framework Fundamentals
- IFDS: Interprocedural Finite Distributive Subset problems
- Key insight: model dataflow facts as reachability in an exploded supergraph
- Each program point gets multiple nodes (one per dataflow fact)
- Flow functions connect nodes to represent how facts propagate

## Slide 5: The Exploded Supergraph Construction
- Create supergraph with nodes for each (program point, dataflow fact) pair
- Add special node Λ representing "no fact" or empty set
- Edges represent flow functions showing how facts propagate
- Call and return edges connect procedures while maintaining context

## Slide 6: Summary Edges for Efficiency
- Summary edge: precomputed effect of an entire procedure call
- Stores what happens from call site to return site for specific dataflow facts
- Enables reuse: once computed, summary applies to all call sites
- Critical optimization that makes the algorithm practical

## Slide 7: The Tabulation Algorithm
- Two phases: forward pass builds summary edges, backward pass uses them
- Worklist algorithm explores graph systematically
- Path edges track reachability in the exploded supergraph
- Algorithm is demand-driven: computes only what's needed

## Slide 8: Implementation and Real-World Results
- Implemented in C using EEP (Efficient Execution Platform)
- Used partial redundancy elimination as test case
- Analyzed programs up to 12,000 lines of code
- Performance was practical: analysis completed in reasonable time

## Slide 9: Theoretical Complexity Analysis
- Time complexity: O(ED³) where E is edges, D is dataflow facts
- Space complexity: O(ED²) for storing path and summary edges
- Worst-case cubic, but often much better in practice
- Polynomial complexity makes it feasible for real programs

## Slide 10: Impact on Program Analysis
- First practical algorithm for precise interprocedural dataflow analysis
- Graph reachability formulation enabled decades of follow-up research
- IFDS became foundation for modern static analysis tools
- Demonstrates how theoretical computer science enables practical tools

## Slide 11: Question for You
What other program analysis problems could benefit from being reformulated as graph reachability queries?
