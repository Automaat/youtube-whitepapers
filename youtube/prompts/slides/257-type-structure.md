Generate 11 presentation slides based on the podcast about John C. Reynolds' 1974 paper "Towards a Theory of Type Structure".

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Fundamental Dilemma (1974)
- Reynolds tackled the core tension: flexible code vs. type safety
- Early type systems were rigid—required separate implementations for each type
- Example: `sort_integers()`, `sort_floats()`, `sort_strings()` as distinct functions
- Code reuse was impossible without sacrificing type checking
- Dynamic typing offered flexibility but lost compile-time safety guarantees
- The question: Can we have both polymorphism and type safety?

## Slide 2: The Problem with Early Type Systems
- Strongly-typed languages enforced safety but prevented code reuse
- Programmers wrote nearly identical code repeatedly for different types
- Weakly-typed systems allowed flexibility but shifted correctness burden to programmers
- No middle ground existed between these two extremes
- Reynolds saw this as a solvable theoretical challenge
- Mathematical formalism could bridge the gap

## Slide 3: Type Homomorphisms—The Core Innovation
- Reynolds introduced type-level abstraction through homomorphisms
- Functions can operate uniformly across types while preserving structure
- Key insight: separate the algorithm from the data representation
- Type parameters allow single implementation for multiple concrete types
- Compiler verifies correctness for all possible instantiations
- Polymorphic functions maintain safety without sacrificing generality

## Slide 4: Lambda Calculus Extension—System F
- Reynolds formalized polymorphism by extending lambda calculus
- Introduced type abstraction: `Λt.e` (capital lambda for type-level functions)
- Type application: instantiate abstract types with concrete ones
- Example: `λx ∈ t.x` represents the identity function for any type t
- This became known as polymorphic lambda calculus or System F
- Foundation for modern generic programming and type inference

## Slide 5: Representation Independence
- Core principle: internal representation should be hidden from clients
- Abstraction boundaries prevent code from depending on implementation details
- Theoretical foundation for modules, interfaces, and API design
- Guarantees that changing internal structure won't break external code
- Enables safe refactoring and system evolution
- Formalized what was previously just good practice

## Slide 6: Parametric Polymorphism vs. Ad-Hoc Polymorphism
- Parametric: uniform behavior across all types (Reynolds' focus)
- Ad-hoc: different implementations per type (operator overloading)
- Parametric polymorphism enables stronger reasoning about correctness
- Type variables act as placeholders without knowledge of concrete types
- Functions must work identically regardless of type instantiation
- This constraint is a feature, not a limitation

## Slide 7: The Soundness Challenge
- Critical question: Does adding polymorphism introduce logical contradictions?
- Type systems must be proven sound to be trustworthy
- Risk: abstraction might create paradoxes or inconsistencies
- Reynolds provided formal proofs that System F is sound
- No internal contradictions—safe to use in practice
- Established mathematical rigor for type theory

## Slide 8: Influence on ML and Functional Languages
- ML (1973-1978) adopted and popularized Reynolds' ideas
- Hindley-Milner type inference automated type checking
- Programmers could write polymorphic code without explicit type annotations
- OCaml, Haskell, F# built on these foundations
- Parametric polymorphism became standard in functional programming
- Generics in imperative languages followed similar principles

## Slide 9: Impact on Rust and Modern Systems Languages
- Rust's type system directly descends from Reynolds' work
- Zero-cost abstractions rely on parametric polymorphism
- Traits and generics provide type-safe code reuse
- Compiler verifies memory safety through type-level reasoning
- No runtime overhead for polymorphic functions (monomorphization)
- Reynolds' theory enables modern systems programming guarantees

## Slide 10: Legacy and Ongoing Relevance
- 1974 work remains foundational 50 years later
- Ideas migrated from theory to everyday engineering practice
- Type systems continue evolving based on Reynolds' principles
- Generic programming, dependency injection, abstract data types all trace back
- Boundary between academic theory and practical engineering is fluid
- Crossing that boundary produces the most valuable innovations

## Slide 11: Question for You
Which modern programming language feature that you use daily do you think would most surprise Reynolds if he could see how his theoretical work evolved in practice?
