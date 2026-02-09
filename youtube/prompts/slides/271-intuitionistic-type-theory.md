Generate 11 presentation slides based on the podcast about **Intuitionistic Type Theory** by Per Martin-Löf.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Intuitionistic Type Theory
- Martin-Löf's foundational framework connecting proofs and programs
- Revolutionary approach treating propositions as types and proofs as programs
- Constructive mathematics based on intuitionistic logic principles
- Foundation for modern proof assistants and dependent type systems

## Slide 2: Core Philosophy - Propositions as Types
- Every proposition is interpreted as a type in the type system
- Truth of a proposition means inhabiting that type with a concrete term
- Constructive proofs require explicit construction of witnesses
- Fundamental shift from classical logic's existence claims to computational evidence

## Slide 3: Basic Types and Set Formation
- Type hierarchy starting with Set (universe of types)
- Primitive types: natural numbers, booleans, finite types
- Type formation rules define how to construct new types
- Judgments form: "A is a type" and "a is an element of type A"

## Slide 4: Products and Conjunctions (Sigma Types)
- Conjunction A ∧ B represented as product type A × B
- Proof of conjunction is a pair (a, b) where a proves A and b proves B
- Dependent products (Σ-types) generalize pairs with type dependency
- Elimination via pattern matching and projections

## Slide 5: Implication as Function Types (Pi Types)
- Implication A → B interpreted as function type from A to B
- Proof is a function transforming proofs of A into proofs of B
- Dependent function types (Π-types) allow result type to depend on input
- Lambda abstraction constructs proofs of implications

## Slide 6: Universal Quantification
- "For all x in A, property P(x) holds" becomes Π-type: (x: A) → P(x)
- Constructing such function requires providing proof for every possible input
- Type-checking ensures logical correctness through computation
- Connects mathematical quantification with computational abstraction

## Slide 7: Combinators and Proof Construction
- K combinator and S combinator mentioned as foundational proof builders
- Lambda calculus forms computational substrate of proof theory
- Normalization ensures every proof reduces to canonical form
- Combinatory logic provides alternative foundation for computation

## Slide 8: Axiom of Choice as Constructive Principle
- In constructive setting, choice becomes a provable theorem
- For collection of non-empty sets, choice function can be constructed
- No contradiction with constructive principles unlike classical mathematics
- Demonstrates power of computational interpretation of logic

## Slide 9: Natural Numbers and Induction
- Natural numbers defined inductively with zero and successor
- Peano axioms naturally expressed in type theory
- Examples: defining addition constructively, proving properties by induction
- Induction principle becomes recursion principle for functions

## Slide 10: Russell's Paradox and Universe Hierarchy
- Cannot have "set of all sets" without contradiction
- Universe hierarchy: Set₀, Set₁, Set₂, ... prevents paradoxes
- Each universe level contains types from lower levels
- Stratification resolves classical foundational problems constructively

## Slide 11: Question for You
What advantages does treating propositions as types provide for mechanical proof verification compared to classical logical approaches?
