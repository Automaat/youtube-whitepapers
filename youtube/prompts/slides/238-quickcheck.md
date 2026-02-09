Generate 11 presentation slides based on the podcast about QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: QuickCheck - Automated Property-Based Testing
- Revolutionary shift from example-based to property-based testing in Haskell
- Automatically generates random test cases to verify code properties
- Tests properties that must hold for all inputs, not specific examples
- Dramatically reduces manual test case writing while improving coverage
- Introduced by Claessen and Hughes as lightweight testing framework

## Slide 2: The Core Concept - Properties Over Examples
- Instead of testing specific inputs (e.g., reverse [1,2,3] == [3,2,1])
- Define universal properties (e.g., reverse(reverse xs) == xs for all lists)
- QuickCheck generates hundreds of random inputs automatically
- Developers focus on what should be true, not individual test cases
- Shift from "does it work for this case?" to "does it always work?"

## Slide 3: Random Data Generation with Gen Type
- Heart of QuickCheck is the Gen A type - generator for values of type A
- Gen is a monadic type allowing composition of random generators
- Built-in generators for primitive types (Int, Bool, String, etc.)
- Combine simple generators to create complex data structures
- Example: generate random lists by composing element generators with length generators

## Slide 4: Controlled Randomness - Size Parameter
- QuickCheck starts with small test cases, gradually increasing complexity
- Size parameter controls the magnitude/complexity of generated data
- Small cases (size=1,2) catch simple bugs quickly
- Larger cases (size=50+) expose edge cases and scaling issues
- Prevents overwhelming developers with giant failing examples first

## Slide 5: Shrinking - Finding Minimal Counterexamples
- When test fails, QuickCheck finds smallest failing input automatically
- Instead of "failed on list of 50 elements", shows "fails on [0]"
- Systematic reduction: tries smaller sublists, simpler values
- Makes debugging trivial - minimal example reveals exact problem
- Critical feature that makes QuickCheck practical for real development

## Slide 6: Non-Determinism in Test Suites
- Tests may pass or fail on different runs due to randomness
- This is a feature, not a bug - explores different input spaces each time
- Continuous testing catches bugs that deterministic tests miss
- Statistical confidence increases with repeated executions
- Acceptable tradeoff: broader coverage vs. reproducibility

## Slide 7: Performance Characteristics
- Typical run: 100 test cases generated and checked in seconds
- Computational cost significantly lower than exhaustive testing
- Most bugs found in first 20-50 random cases
- Overhead minimal compared to writing hundreds of manual tests
- Practical for continuous integration and frequent testing

## Slide 8: Real-World Bug Discovery - Substitution Example
- QuickCheck revealed bug in term substitution function (subst s t s a t)
- Manual testing had missed the corner case for years
- Random generation explored input combinations developers hadn't considered
- Found within standard 100-test run without special configuration
- Demonstrates power of property-based approach on production code

## Slide 9: Improving Generators - Avoiding Degenerate Cases
- Initial naive generators often produce useless test data
- Example: random lambda terms mostly deeply nested, unrealistic structures
- Solution: carefully tune generator probabilities and size distributions
- Balance between coverage and realistic inputs improves bug detection
- Generator quality directly impacts testing effectiveness

## Slide 10: Impact on Testing Practice
- Became standard testing tool in Haskell ecosystem
- Inspired ports to dozens of languages (ScalaCheck, Hypothesis, jsverify)
- Changed how developers think about testing: properties not examples
- Integration with type systems enables testing of complex invariants
- Lightweight design encourages adoption without heavy framework overhead

## Slide 11: Question for You
Even if their results may differ for individual runs, can non-deterministic tests provide sufficient confidence in code correctness?
