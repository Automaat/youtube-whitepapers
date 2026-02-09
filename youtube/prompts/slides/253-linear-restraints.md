Generate 11 presentation slides based on the podcast about "Automatic Discovery of Linear Restraints Among Variables of a Program" by Patrick Cousot and Nicolas Halbwachs.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Hidden Engine of Modern Software
- 1978 paper that underpins much of today's program verification technology
- Patrick Cousot and Nicolas Halbwachs introduce automatic discovery of linear invariants
- Computers automatically verify program safety without human-written assertions
- Foundational work in Abstract Interpretation methodology
- Transforms program analysis from manual verification to automated geometric reasoning

## Slide 2: The Problem - Finding Program Invariants
- Traditional verification requires manually written loop invariants
- Example: verifying array bounds without subscript assertions
- Linear equality relations among variables often unstated but critical
- Challenge: discover relationships that hold throughout program execution
- Goal: computer discovers invariants automatically instead of relying on programmer

## Slide 3: Geometric Perspective - Program State as Polyhedra
- Revolutionary shift: program state as geometric shapes, not just numbers
- Each variable represents a dimension in n-dimensional space
- Linear constraints define convex polyhedra (geometric regions)
- Every point inside polyhedron represents valid program state
- Program analysis becomes observing polyhedron transformations through code

## Slide 4: Abstract Interpretation Framework
- Part of broader methodology called Abstract Interpretation by Cousot
- Track billions of possible states using single geometric abstraction
- Assignments transform polyhedra through linear operations
- Conditional statements (if) perform geometric cuts on polyhedra
- Precise mathematical foundation replaces imprecise symbolic reasoning

## Slide 5: The Widening Problem - Handling Loops
- Loops create infinite sequences of expanding polyhedra
- Without intervention, analysis would never terminate
- Widening operator performs controlled extrapolation
- Jumps to shape greater-than-or-equal to infinite iteration result
- Conscious trade-off: lose precision but guarantee termination

## Slide 6: Dual Representations - Frame and Constraints
- Two equivalent ways to represent polyhedra
- Constraint representation: system of linear inequalities
- Frame representation: vertices, extreme rays, and lines
- Conversions enable different operations (convex-hull uses frame, intersection uses constraints)
- Choosing right representation critical for computational efficiency

## Slide 7: Lanery's Method - Finding Polyhedron Frames
- Linear programming pivot method to extract frame from constraints
- Adjacency graph traversal technique finds all vertices and extreme rays
- Handles polyhedra with no lines (bounded polytopes)
- Identifies feasible bases and adjacent vertices systematically
- Foundation for conversion between dual representations

## Slide 8: Modern Impact - Where This Work Lives Today
- Modern compilers use simplified versions for code optimization
- Static analyzers (ASTREE) verify safety-critical software (avionics, automotive)
- Automated theorem provers leverage polyhedral analysis
- Prevents buffer overflows, null pointer dereferences at compile time
- Invisible but essential infrastructure in software toolchains

## Slide 9: Computational Complexity Challenges
- Representing polyhedra in high-dimensional spaces extremely expensive
- Real programs have dozens to hundreds of variables
- Computational cost grows exponentially with dimensions
- Precision vs performance trade-off defines subsequent research
- Authors openly acknowledged scalability as major limitation

## Slide 10: Evolution - Simpler Geometric Abstractions
- Research shifted to cheaper shapes than full polyhedra
- Octagons: constraints like x±y ≤ c (eight-sided in 2D)
- Intervals: simple ranges for each variable independently
- Zones and difference-bound matrices for timing analysis
- Each abstraction trades precision for scalability to larger programs

## Slide 11: Question for You
What other abstractions are waiting to be discovered that could balance precision, performance, and scalability for program analysis?
