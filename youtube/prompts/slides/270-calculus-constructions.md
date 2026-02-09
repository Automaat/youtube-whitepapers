Generate 11 presentation slides based on the podcast about "The Calculus of Constructions" by Huet and Kok.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to The Calculus of Constructions
- The Calculus of Constructions unifies logic and programming languages
- Combines functional programming with type theory and formal proofs
- Developed by Gérard Huet and Thierry Coquand (Kok refers to Coquand)
- Creates a single language where writing code is proving theorems
- Foundation for modern proof assistants like Coq and LEGO

## Slide 2: The Perfect Analogy - Building with Types
- Types in programming are like blueprints in construction
- Just as buildings need solid foundations, programs need sound type systems
- The Calculus of Constructions provides mathematical rigor to ensure correctness
- Every construction step is verified to maintain structural integrity
- Prevents errors at compile-time rather than discovering them at runtime

## Slide 3: One Language for Code and Proofs
- Traditional separation: programming languages vs. proof systems
- The Calculus of Constructions merges these into unified framework
- Writing a function definition simultaneously creates a mathematical proof
- Type checking becomes automated theorem verification
- Eliminates need for separate specification and implementation

## Slide 4: Constructive Approach - Building Instead of Defining
- Rather than abstract definitions, construct actual objects
- Every proof must provide explicit construction or algorithm
- No reliance on non-constructive existence proofs
- If something exists, you must show how to build it
- Aligns with computational interpretation of logic

## Slide 5: Key Abstraction - Dependent Types
- Types can depend on values, not just other types
- Enables expressing precise specifications in type system
- Example: vector type parameterized by exact length
- Most important abstraction enabling proof-carrying code
- Allows encoding complex mathematical properties as types

## Slide 6: The LEGO System - Practical Implementation
- LEGO is a proof assistant based on Calculus of Constructions
- Demonstrates practical applicability of theoretical framework
- Provides interactive environment for theorem proving
- Users can construct proofs step-by-step with system verification
- Shows the concepts work in real-world formal verification

## Slide 7: Foundation for Modern Computing
- Precursor to modern dependently-typed languages like Coq, Agda, Idris
- Influenced certified software development practices
- Enables writing programs that are correct by construction
- Computational interpretation connects logic and programming
- Bridges theoretical computer science and practical software engineering

## Slide 8: Strong Normalization from Logic Perspective
- Strong normalization guarantees all computations terminate
- Every well-typed term reduces to normal form in finite steps
- Critical property ensuring consistency of underlying logic
- Prevents paradoxes and infinite loops in proof systems
- Provides computational soundness for the type system

## Slide 9: Direct Predecessor to Coq
- This paper directly led to development of Coq proof assistant
- Coq extends and implements ideas from Calculus of Constructions
- One of most widely used systems for formal verification today
- Used to verify critical software like CompCert C compiler
- Demonstrates lasting impact on formal methods and software verification

## Slide 10: Broader Impact on Software Engineering
- Influenced type systems in mainstream programming languages
- Inspired development of dependent type features in modern languages
- Changed how we think about program correctness and verification
- Established foundations for certified programming movement
- Shows connection between theoretical advances and practical tools

## Slide 11: Question for You
What other connections are still waiting to discover their own calculus of constructions that will transform them into powerful tools of the future?
