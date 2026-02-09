Generate 11 presentation slides based on the podcast about "Theorems for Free!" by Philip Wadler.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Type-Driven Reasoning
- Understanding function behavior without reading implementation
- Predicting what a function cannot do based on its type signature
- The promise: guarantees from types alone, not from code inspection
- Third way beyond reading code line-by-line or writing tests

## Slide 2: Parametricity - The Core Concept
- Parametric polymorphism: functions that work on data of any type
- Generic functions have paradoxically limited capabilities
- Type genericity constrains what implementations can do
- Pure functions with no side effects (no I/O, no database, no state)

## Slide 3: The Machine Analogy
- Function as a black box with triangular input and output ports
- No external parts or knowledge inside the machine
- Can only manipulate data structure, not create or modify values
- Operations: rearrange, copy, filter - but never fabricate from nothing

## Slide 4: What Generic Functions Cannot Do
- Cannot create new values without input
- Cannot modify data in type-specific ways
- Can only move, copy, or reorder existing data
- Mathematical proofs guarantee these impossibilities

## Slide 5: Mathematical Rigor Through Formal Notation
- Symbols like `∀r. ∃τ₃. ∀k,b,r,x₃,x` prove impossibility
- Not executable code - mathematical proofs
- Properties derived directly from function types, independent of implementation
- `∃functorV` pattern: repeated structures in formal proofs

## Slide 6: Example - List Function `[A] → [A]`
- Limited operations: return unchanged, reverse order, filter elements, duplicate
- Cannot create new elements of type A from nothing
- Cannot add number 42 (doesn't know if A is a number)
- Cannot uppercase text (doesn't know if A is text)

## Slide 7: Example - Function Iteration `(A → A) → Int → (A → A)`
- Given: operation `(A → A)`, count `Int`, returns iterated operation
- Can only apply the operation N times (0, 1, 5, etc.)
- Cannot suddenly multiply if given addition
- Behavior strictly dictated by structural constraints

## Slide 8: Practical Implications
- Better API design: generic types provide automatic guarantees
- Users know functions won't do unexpected things with their data
- Deliberate trade-off: more general types = more constraints = more safety
- Parametricity is a design tool, not a restriction

## Slide 9: Program Correctness Through Types
- Proving correctness for all possible data, not just test cases
- Fundamental difference in certainty level vs. testing
- Type-based reasoning provides stronger guarantees
- When functions become impure, they lose this "blindness" property

## Slide 10: Beyond Pure Functions
- Research extended to functions with side effects
- Weaker theorems possible for non-pure code
- Decades of further research built on this foundation
- Types as formal specifications, not just labels

## Slide 11: Question for You
Is our freedom in implementation more limited by type structure than we realize?
