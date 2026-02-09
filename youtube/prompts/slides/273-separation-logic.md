Generate 11 presentation slides based on the podcast about Separation Logic by John Reynolds.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Separation Logic
- Revolutionary approach to program verification with pointer manipulation
- Created by John Reynolds to solve limitations of classical Hoare logic
- Enables local reasoning about heap memory and shared state
- Foundation for modern verification tools analyzing real-world programs
- Key innovation: separating conjunction operator for disjoint memory regions

## Slide 2: Pointer Aliasing Problem in Classical Logic
- In-place list reversal as motivating example
- Classical preconditions require listing all memory NOT modified
- Negative specifications become impractical for real programs
- Aliasing makes it impossible to verify pointer operations locally
- Reynolds recognized fundamental limitation of traditional approaches

## Slide 3: Core Innovation - Positive State Description
- Describe only memory cells that EXIST and are relevant
- Avoid specifying what doesn't exist or isn't modified
- Enables compositional reasoning about heap structures
- Natural way to express pointer manipulation invariants
- Shifts from global to local memory reasoning

## Slide 4: Separating Conjunction Operator
- Star operator (*) combines disjoint heap fragments
- P * Q means P holds on one part, Q on another, and they don't overlap
- Enforces spatial separation at the logical level
- Brilliant solution to frame problem in verification
- Makes invariants significantly simpler to express

## Slide 5: Frame Rule - Local Reasoning
- If {P} C {Q} then {P * R} C {Q * R}
- Command C can execute on fragment satisfying P
- Rest of heap (R) remains unchanged automatically
- No need to explicitly list unmodified memory
- Enables modular verification of large programs

## Slide 6: Verification Example - In-Place List Reversal
- Precondition: list(x, α) describes linked list from x with values α
- Postcondition: list(y, reverse(α)) after reversal
- Invariant tracks partially reversed list structure
- Much simpler than classical Hoare logic specification
- Demonstrates power of local reasoning

## Slide 7: Extension to Concurrency
- Critical section rule for synchronized access to shared resources
- Resource invariant describes shared state properties
- Process temporarily owns resource during critical section
- After exit, resource returns to shared pool
- Enables verification of concurrent programs with locks

## Slide 8: Recursive Predicates for Data Structures
- list(i, α) predicate recursively defines linked list structure
- tree(i) predicate for binary tree verification
- Base cases and recursive cases express structure inductively
- Predicates compose naturally with separating conjunction
- Handles complex heap-allocated data structures

## Slide 9: Beyond Simple Disjointness
- Separation logic handles more than just separate memory regions
- Can express partial sharing and ownership transfer
- Applicable to concurrent processes and resource management
- Extensions for permissions and fractional ownership
- Foundation for tools like VeriFast and Viper

## Slide 10: Impact on Modern Verification
- Separation logic revolutionized program verification field
- Enabled practical verification of operating systems and browsers
- Inspired development of Rust's borrow checker
- One elegant statement solves fundamental problem
- Continues to influence programming language design

## Slide 11: Question for You
How does separation logic handle inter-process communication or shared resources that by definition are not disjoint?
