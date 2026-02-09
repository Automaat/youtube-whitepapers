Generate 11 presentation slides based on the podcast about "Predicate Abstraction for Reachability Analysis".

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Predicate Abstraction
- Formal verification technique for infinite-state systems
- Maps infinite state space to finite Boolean abstraction
- Enables automated verification of hardware and software
- Foundation for modern model checking tools like SLAM and BEBOP
- Combines theorem proving with model checking approaches

## Slide 2: The State Space Explosion Problem
- Every variable value creates possible system states
- Traditional model checking limited to finite state systems
- Real programs have unbounded variables (integers, pointers, arrays)
- Need to verify properties over infinite state spaces
- Predicate abstraction provides systematic solution

## Slide 3: Core Concept - Boolean Abstraction
- Select predicates (Boolean expressions) about program state
- Each predicate represents property of interest (e.g., x > 10)
- Map concrete states to Boolean vectors of predicate values
- Reduces infinite states to 2^n abstract states (n predicates)
- Preserves relevant properties while enabling finite verification

## Slide 4: Computing Successor States
- For each abstract state, compute all possible successors
- Use theorem prover to determine reachable predicate combinations
- Newton method: systematic enumeration of Boolean possibilities
- Generates conservative over-approximation of behaviors
- Ensures soundness: all real behaviors captured in abstraction

## Slide 5: Abstraction Refinement Loop
- Start with coarse abstraction (few predicates)
- Check safety properties on abstract model
- If counterexample found, check if it's real or spurious
- Spurious counterexample: add predicates to eliminate it
- Iterative refinement until verification succeeds or real bug found

## Slide 6: Weakest Precondition Calculation
- For path segment, compute condition that must hold before
- If weakest precondition is false, path is infeasible
- Uses theorem prover to validate preconditions symbolically
- Key technique for distinguishing real vs spurious errors
- Enables targeted refinement of abstraction

## Slide 7: SLAM Tool Architecture
- Microsoft's driver verification tool using predicate abstraction
- Boolean program as intermediate verification language
- C2BP: translates C code to Boolean programs
- BEBOP: model checker for Boolean programs
- Newton: computes predicate abstraction refinements

## Slide 8: Counterexample-Guided Refinement
- Abstract model checker produces error trace
- Symbolic execution validates trace feasibility
- Infeasible trace indicates abstraction too coarse
- Extract new predicates from infeasible path constraints
- Add predicates and regenerate abstraction automatically

## Slide 9: Real-World Success - Windows Driver Verification
- SLAM found real bugs in Windows device drivers
- Verified correctness of API usage patterns
- Handled real C code with pointers and function calls
- Demonstrated scalability to industrial software
- Influenced development of Static Driver Verifier (SDV)

## Slide 10: Impact and Applications
- Foundation for software model checking tools
- Enables verification of infinite-state systems automatically
- Combines strengths of theorem proving and model checking
- Applicable to concurrent systems and protocol verification
- Key technique in modern formal methods toolchain

## Slide 11: Question for You
Or network protocols on which internet security depends?
