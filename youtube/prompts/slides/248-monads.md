Generate 11 presentation slides based on the podcast about "Notions of Computation and Monads" by Eugenio Moggi.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Problem with Lambda Calculus
- Lambda calculus with βη-conversion assumes all programs are total functions from values to values
- This oversimplification erases critical real-world computational behaviors
- Non-termination (diverging computations) cannot be properly represented
- Side effects like state mutation and I/O are ignored in the theoretical model
- Traditional program equivalence proofs fail because they don't account for these computational effects
- Need: a mathematical framework that preserves both functional purity and computational reality

## Slide 2: Moggi's Solution - The Kleisli Triple
- Core innovation: triple (T, η, *) where T is a unary type constructor encoding "notions of computation"
- η (eta): injection operation that wraps values into computations (the "return" operation)
- (*) extension operator: evaluates a computation then applies function to result (Kleisli composition)
- Intuition: c: TA --f*--> (let x⇐c in f(x)): TB represents sequential evaluation
- Three axioms capture sequential program execution perfectly
- Separates concerns: values (category C) vs computations (monad T) vs programs (Kleisli category)

## Slide 3: Type Constructor T - Encoding Effects
- Partiality: TA = A⊥ (add bottom element for divergence/non-termination)
- Nondeterminism: TA = Pfin(A) (finite powersets of possible results)
- Side effects: TA = (A×S)^S (state-dependent computations mapping input state to output state and result)
- Exceptions: TA = A+E (coproduct with error type E for exception handling)
- Continuations: TA = R^(R^A) (continuation-passing style)
- All share identical categorical structure despite different operational meanings

## Slide 4: The Extension Operator and Let-Binding
- Extension operator f*: TA → TB encodes sequential composition of effectful computations
- Let-binding syntax: let x⇐c in f(x) explicitly sequences computation c before applying f
- First Kleisli axiom: ηA; f* = f (returning value then using it equals direct application)
- Second axiom: f*; ηB = f (sequencing then returning is identity)
- Third axiom: f*; (g; h*)* = (f; (g; h*)*)* (associativity of sequential evaluation)
- This algebraic structure provides correct semantics for any computational effect

## Slide 5: Kleisli Category - Programs as Morphisms
- Kleisli category CT has same objects as base category C but different morphisms
- Morphisms A→B in CT are actually morphisms A→TB in C (computations producing B from A)
- Composition in CT represents sequential evaluation of programs with effects
- Identity morphism is ηA (wrapping pure value as trivial computation)
- Category theory provides general theory of functions replacing direct λ-calculus manipulation
- Mono requirement: ηA must be injective so values embed distinctly into computations

## Slide 6: Strong Monads for Complex Languages
- Simple monads insufficient for languages with multiple parameters and function types
- Strong monad adds tensorial strength: natural transformation t: A×TB → T(A×B)
- Converts "value paired with computation" to "computation producing pair"
- Enables modeling functional types with different calling conventions
- Call-by-value semantics: (TB)^A for functions from A to computations of B
- Call-by-name semantics: (TB)^(TA) for functions from computations of A to computations of B

## Slide 7: Formal Systems - Metalanguage and Programming Language
- Simple Metalanguage: equational logic with type constructor T, return operation [·], and let-binding
- Terms explicitly distinguish values from computations using syntactic markers
- Simple Programming Language: extends with explicit sequencing via let construct
- Extended Metalanguage: algebraic terms with multiple variables and function spaces
- λc-model: category with products, strong monad, and T-exponentials for complete semantics
- Conservative extension results guarantee intuitionistic higher-order logic reasoning about computations

## Slide 8: Practical Applications in Language Design
- Program verification: prove equivalence correctly respecting computational effects
- Hoare-style specifications for imperative features using modal operators γ: TΩ→Ω
- Language implementation primitives: lookup/update for mutable state, if/while for control flow
- Interactive I/O modeled as tree structures with read/write operations
- Denotational semantics replacing domain theory with modular monad-based approach
- Location allocation and memory management primitives with formal semantics

## Slide 9: Conservative Extensions and Toposes
- HMLT (higher-order metalanguage over toposes) conservatively extends MLT
- Monads can be lifted to toposes preserving all categorical structure
- Yoneda embedding C → Ĉ (topos of presheaves) provides complete higher-order logic
- Theoretical guarantees: adding computational effects doesn't break logical soundness
- Any proof in extended system has corresponding proof in base system
- Separation between computational and logical layers remains formally verified

## Slide 10: Impact on Modern Programming
- Haskell's do-notation is direct syntactic realization of Moggi's let construct
- Async/Promise libraries implement monadic composition of asynchronous computations
- Either/Result monads formalize exception semantics in type-safe manner
- State monad encapsulates mutable state safely in purely functional languages
- Effect systems in modern languages (Scala, Rust, TypeScript) use monad-like abstractions
- Provides theoretical foundation for all modern effect-handling in typed functional programming

## Slide 11: Question for You
As opposed to pure logical deduction?
