Generate 11 presentation slides based on the podcast about "Fundamental Concepts in Programming Languages" by Christopher Strachey (1967).

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Historical Context & The Communication Problem
- 1967 paper by Christopher Strachey - foundational work in programming language theory
- Identified fundamental communication chaos: programmers, mathematicians using same terms (name, value, expression) but meaning different things
- Described as "uncertain communication at best" between professionals
- Era obsessed with syntax (how to write code) while neglecting semantics (what code actually means)
- Strachey's goal: establish precise vocabulary for discussing programming language concepts
- Paper became geological layer underlying all modern programming language design

## Slide 2: Syntax vs Semantics Distinction
- Critical separation: syntax (notation, how we write) vs semantics (meaning, what happens)
- Revolutionary idea: first understand what you want to express, then worry about notation
- Analogy: mechanic vs rally driver both say "engine" but mean different things (cylinders vs wheel power)
- This confusion led to inconsistent language design and implementation errors
- Strachey advocated for semantics-first approach to language design
- Established framework still used in modern programming language research

## Slide 3: L-values and R-values
- Fundamental distinction for assignment: `x = y + 1`
- L-value (left/location): memory address, the "mailbox number" - constant location
- R-value (right/content): actual value stored, the "letter inside" - can change
- Same variable name means different things on left vs right side of assignment
- Assignment semantics: fetch r-value from y, add 1, store in l-value of x
- Foundation for understanding references, pointers, and memory models in all modern languages

## Slide 4: Parameter Passing Mechanisms
- Call by value: pass r-value (content) - creates copy, original unchanged
- Call by name: pass l-value (location) - can modify original variable
- ALGOL 60 confusion: procedures "chained to their names," not mobile like numbers
- Example confusion: does parameter capture value at call time or reference throughout execution?
- Different languages made different choices (Fortran, Pascal, C all varied)
- Understanding this distinction critical for debugging modern code behavior

## Slide 5: First-Class Procedures
- Revolutionary concept: functions should be "first-class citizens" like numbers
- Functions should have r-values: can be assigned to variables, returned from other functions
- Not just static named procedures - mobile, composable computational units
- Required rethinking what "function value" means - led to closure concept
- Foundation of modern functional programming (JavaScript, Python, Haskell)
- Changed functions from second-class citizens to primary abstraction mechanism

## Slide 6: Closures and Free Variables
- Closure = function + environment capturing free variables (non-parameter variables used in function)
- Environment "freezes context" where function was born, travels with function
- Classic test: `let A = 3; let F(x) = x + A; A = 10; F(5) = ?`
- Answer depends on whether closure captured r-value (3) or l-value (reference to A, now 10)
- CPL language had special syntax letting programmer choose capture mechanism
- Foundation for lexical scoping in modern languages

## Slide 7: Lambda Calculus and Church's Influence
- Deep connection to Alonzo Church's lambda calculus (1930s mathematical foundation)
- Lambda calculus: pure mathematical system for expressing computation through function abstraction
- Strachey bridged abstract mathematics and practical programming languages
- Same variable name can denote different things based on context (polymorphism seeds)
- Influenced how operators work differently for integers, floats, strings
- Theoretical foundation became practical language feature

## Slide 8: Higher-Order Functions and Parametric Polymorphism
- Higher-order functions: functions that take functions as arguments or return them
- Classic example: `map` function - applies operation to each list element
- Type abstraction: "give me function apple→orange and list of apples, get list of oranges"
- Map doesn't care about specific types - works universally for infinite type combinations
- Ancestor of generics (Java), templates (C++), parametric types (Haskell)
- One definition works for unlimited type instantiations

## Slide 9: CPL Language and Composite Data Types
- CPL (Combined Programming Language): Strachey's experimental language implementing these ideas
- User-defined composite types: combine primitive types into custom structures
- Intellectual ancestor of: C structs, object-oriented classes, algebraic types in functional languages
- Demonstrated list operations using LISP functions CAR (first element) and CDR (rest of list)
- Key insight: assignment operations share structure, don't copy entire data trees
- Enabled efficient data manipulation through reference semantics

## Slide 10: Modern Legacy and Fundamental Principles
- Universal principles transcending any specific programming language
- L-values/R-values: precise language for discussing assignment and memory
- First-class functions: foundation of functional programming paradigm
- Closures: essential for modern JavaScript, Python, Swift, Kotlin
- Reference semantics: understanding prevents debugging nightmares with shared data
- Problems diagnosed in JavaScript/Python today were identified by Strachey in 1967
- Not a language manual - timeless theoretical framework for language design

## Slide 11: Question for You
Are we still discovering fundamentally new semantic capabilities in today's world of thousands of languages, libraries, and frameworks? Or are we mostly creating new fashionable syntax for the same powerful ideas Christopher Strachey described half a century ago?
