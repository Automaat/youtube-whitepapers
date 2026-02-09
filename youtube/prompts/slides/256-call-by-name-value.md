Generate 11 presentation slides based on the podcast about Gordon Plotkin's 1975 paper "Call-by-Name, Call-by-Value and the Lambda Calculus".

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Two Fundamental Evaluation Strategies
- Call-by-value: eager evaluation - arguments computed before function invocation
- Call-by-name: lazy evaluation - arguments computed only when needed
- Both strategies existed in practice, but theoretical foundations were unclear
- Lambda calculus used normal order reduction (similar to call-by-name)
- Real implementations like SECD machine used call-by-value
- This mismatch created fundamental problems between theory and practice

## Slide 2: The SECD Machine and ISWIM Language
- SECD: Stack, Environment, Control, Dump - components needed for program execution
- Designed for ISWIM functional programming language (early 1970s)
- Implemented call-by-value semantics in practice
- Lambda calculus theory assumed call-by-name (normal order reduction)
- Growing gap between elegant mathematical theory and working computers
- Need for rigorous formalization of both evaluation strategies

## Slide 3: Problem 1 - Infinite Loops and Evaluation Order
- Call-by-value acts like an overeager assistant - computes everything immediately
- If argument computation enters infinite loop, entire program hangs
- Call-by-name might never evaluate that argument if unused
- Example: function that ignores its argument succeeds with call-by-name, fails with call-by-value
- Fundamental difference in termination behavior between strategies
- Theory (normal order) and practice (call-by-value) diverge on program behavior

## Slide 4: Problem 2 - Restrictions on Lambda Calculus
- Plotkin recognized call-by-value as important and natural evaluation strategy
- Required developing new theoretical framework specifically for call-by-value
- Cannot simply apply existing lambda calculus rules to call-by-value semantics
- Standard beta reduction doesn't work correctly with eager evaluation
- Need formal rules that match actual machine behavior
- Foundation for bridging theory-practice gap

## Slide 5: Call-by-Value Constraint on Beta Reduction
- Key restriction: value cannot be an expression that still needs computation
- Example: "2 + 3" must reduce to "5" before being passed to function
- Beta reduction in call-by-value only applies when argument is already a value
- Function won't start working until it receives final, computed components
- This constraint ensures eager evaluation semantics are preserved
- Fundamental difference from standard lambda calculus reduction rules

## Slide 6: The Standardization Theorem
- Second fundamental and beautiful result in Plotkin's work
- Proves that in call-by-value, order of reductions doesn't matter for final result
- Can reduce any expression in any order and get the same value
- Provides strong theoretical guarantees for compiler optimizations
- Ensures deterministic behavior regardless of evaluation order choices
- Critical property for reasoning about program correctness

## Slide 7: CPS Transformation - Continuation Passing Style
- Simple function wrapping mechanism to make control flow explicit
- Instead of returning values, functions call continuations with results
- Every computation receives a "what to do next" function
- Makes evaluation order explicit and controllable
- Bridge between different evaluation strategies
- Powerful technique for compiler transformations

## Slide 8: CPS Applications Beyond Single Program
- Not just theoretical exercise - practical compiler technique
- Used extensively in optimizing compilers for functional languages
- Enables sophisticated program transformations and optimizations
- Makes control flow manipulation explicit and analyzable
- Standard technique in modern compiler implementations
- Connects abstract theory to concrete compiler engineering

## Slide 9: Impact on Compiler Optimizations
- Consider optimization: "print(complexCalculation() + 0)" → "print(complexCalculation())"
- Mathematically sound (adding zero changes nothing)
- But what if complexCalculation() has side effects?
- In call-by-value with side effects, this optimization is unsafe
- Call-by-name semantics interact differently with side effects
- Choice of evaluation strategy directly impacts compiler optimization safety

## Slide 10: Modern Language Design Implications
- Choice between eager and lazy evaluation shapes entire language character
- Haskell chose lazy evaluation (call-by-name) - evaluates only what's needed
- Most mainstream languages chose eager evaluation (call-by-value)
- Each choice brings trade-offs in performance, reasoning, and program behavior
- Languages like Scala allow mixing both strategies
- Plotkin's work provides theoretical foundation for understanding these choices

## Slide 11: Question for You
Are call-by-name and call-by-value fundamentally different computational models, or can they be unified under a common theoretical framework? Will there always be an insurmountable barrier between them?
