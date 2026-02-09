Generate 11 presentation slides based on the podcast about Principal Type-Schemes for Functional Programs by Damas and Milner.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to ML Type System
- ML (Meta Language) introduced automated type inference for functional programming
- Programmers no longer need to explicitly declare types in their code
- Compiler automatically deduces the most general type for each expression
- Combines type safety with flexibility previously only found in dynamic languages

## Slide 2: The Problem: Manual Type Declarations
- Traditional statically-typed languages required explicit type annotations everywhere
- Writing type declarations was tedious and error-prone
- Programmers had to choose between type safety and coding convenience
- Question: Could we have both safety and convenience?

## Slide 3: Polymorphism - The Core Innovation
- Polymorphic functions work with multiple types using type variables
- Example: identity function can accept any type and return the same type
- Type variables (like 'a, 'b) represent "any type"
- Enables maximum flexibility while maintaining type safety

## Slide 4: Hindley-Milner Type System
- Damas and Milner formalized the theoretical foundation
- Algorithm W performs type inference through constraint solving
- Unification process matches type variables with concrete types
- Guarantees finding the most general (principal) type when it exists

## Slide 5: The Unification Algorithm
- Analyzes function definitions to infer parameter and return types
- Collects type constraints from how values are used in the function body
- Unification solves these constraints to find compatible types
- Example: if function adds 1 to parameter, it must be numeric type

## Slide 6: Type Inference in Action
- Compiler analyzes function body without any type annotations
- Determines that operations like addition constrain types to numbers
- Infers most general type that satisfies all constraints
- Reports type errors when constraints cannot be satisfied

## Slide 7: Generalization and Instantiation
- Let-polymorphism allows variables to have polymorphic types
- Type variables are generalized when binding values
- Instantiated with specific types at each use site
- Enables code reuse without sacrificing type safety

## Slide 8: Soundness and Completeness Proofs
- Damas and Milner proved soundness: inferred types are always correct
- Cannot release a compiler with "usually works" type checking
- Proved completeness: algorithm finds principal type when it exists
- Mathematical rigor ensures reliability for production systems

## Slide 9: Impact on Language Design
- Both soundness and completeness in one system was revolutionary
- Influenced design of OCaml, Haskell, F#, Rust, and many modern languages
- Type inference became standard feature in functional programming languages
- Demonstrated that powerful type systems don't require verbose code

## Slide 10: The Balance: Help vs. Complexity
- Simple code benefits greatly from automatic type inference
- const user = fetchUser() - compiler infers complete type
- Complex scenarios might need explicit type annotations for clarity
- Modern languages allow optional annotations where they improve readability

## Slide 11: Question for You
Where is the boundary between help and complication when it comes to type inference?
