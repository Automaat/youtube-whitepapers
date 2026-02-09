Generate 11 presentation slides based on the podcast about "Compiling with Continuations".

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Continuation Passing Style
- CPS transforms programs to make control flow explicit through continuations
- Every function receives an additional continuation parameter representing "what happens next"
- Enables powerful optimizations by making program structure transparent to compiler
- Original ML compiler implementation demonstrated CPS viability for production systems

## Slide 2: Crystalline Structure of CPS
- CPS representation reveals clear program structure unlike traditional intermediate forms
- Makes control flow and data flow relationships explicit and analyzable
- Functions never return values directly - always pass results to continuation
- Transformation creates uniform representation suitable for aggressive optimization

## Slide 3: Basic CPS Transformation Mechanics
- Functions pass computed values to continuation instead of returning
- Example: PROD_PRIMES function converted to continuation-passing style
- Continuation parameter captures "rest of computation" after function completes
- Every function call becomes tail call in CPS representation

## Slide 4: IS_PRIME Example in CPS
- Traditional recursive function converted to continuation form
- Each recursive call passes continuation representing remaining computation
- Base cases directly invoke continuation with result
- Eliminates traditional call stack through systematic transformation

## Slide 5: Code Structure and Representation
- ML compiler uses CPS as primary intermediate representation
- Functions represented as continuation-accepting transformations
- Enables systematic analysis of program behavior
- Clean separation between computation and control flow

## Slide 6: Dead Code Elimination
- CPS makes unused computations immediately visible
- If continuation is never invoked, entire computation branch can be eliminated
- More aggressive than traditional dead code analysis
- Example: unreachable code paths identified through continuation flow

## Slide 7: Continuation Inlining and Optimization
- Inlining continuations eliminates administrative overhead
- If continuation G is used only once, inline at call site
- Reduces indirection and enables further optimization opportunities
- Creates optimization cascade as inlining exposes new opportunities

## Slide 8: Register Allocation Implications
- CPS impacts register allocation strategy significantly
- Explicit continuation calls affect register lifetime analysis
- Traditional register allocation techniques require adaptation
- Control flow transparency aids in allocation decisions

## Slide 9: Primary Intermediate Representation
- CPS serves as main IR throughout compilation pipeline
- All optimization passes operate on CPS form
- Uniform representation simplifies compiler construction
- From parsing through code generation, CPS maintained

## Slide 10: Aliasing and Memory Safety
- CPS transformation affects aliasing analysis
- Two different names potentially referring to same memory location
- Explicit data flow in CPS aids alias detection
- Critical for optimization safety and correctness guarantees

## Slide 11: Question for You
What new programming architectures and programming paradigms could we discover then?
