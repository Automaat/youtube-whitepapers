Generate 11 presentation slides based on the podcast about Stacked Borrows.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Stacked Borrows
- Rust memory safety model for unsafe code blocks
- Aliasing control mechanism for raw pointers in unsafe contexts
- Compiler optimization enabler through defined aliasing rules
- Foundation for understanding Rust's guarantees beyond safe code
- Critical for systems programming and FFI boundaries

## Slide 2: The Aliasing Problem in Rust
- Operations on Y cannot modify X's value when pointers are properly managed
- Compiler needs aliasing information for optimization decisions
- Traditional C/C++ approaches fail in presence of unsafe blocks
- Rust's type system provides guarantees in safe code only
- Unsafe code requires runtime aliasing model

## Slide 3: Core Concept - The Stack
- Every memory location has an associated borrow stack
- Stack tracks all active references (shared and mutable)
- Fundamental for Vec and other standard library types
- Each reference creates a new stack entry (tag)
- Stack operations: push on borrow, pop on invalidation

## Slide 4: How Stacked Borrows Works
- Model operates dynamically during program execution
- Instead of analyzing code, tracks runtime pointer behavior
- Each pointer access checks against current stack state
- Violations caught immediately when rules are broken
- Enables both safety checking and optimization hints

## Slide 5: Permission Model
- SharedReadWrite: unrestricted access permission
- SharedReadOnly: immutable shared access
- Unique: exclusive mutable access
- Disabled: invalidated reference state
- Permission transitions based on stack operations

## Slide 6: The Unbending Rule
- Public API must maintain all invariants
- Private implementation can use unsafe internally
- Abstraction boundaries enforce safety contracts
- Standard library relies heavily on this principle
- UnsafeCell marks explicit aliasing exception points

## Slide 7: Retagging Mechanism
- Every pointer creation triggers retagging operation
- New tag pushed onto memory location's stack
- Allows tracking of reference relationships
- No need to track entire program history
- Local reasoning about current stack state

## Slide 8: Two-Phase Borrows
- Special handling for method call receiver reborrowing
- Model handles interior mutability patterns
- Optimizations for common Rust idioms
- Shared references with mutation capability (UnsafeCell)
- Advanced feature enabling more flexible aliasing

## Slide 9: Compiler Optimizations Enabled
- Unlocks new level of optimization opportunities
- Noalias LLVM attribute generation for mutable references
- Dead store elimination improvements
- Load hoisting and reordering optimizations
- Performance competitive with C/C++ without sacrificing safety

## Slide 10: Real-World Impact
- Seven model violations found in existing Rust codebases
- Model continues to evolve based on discovered edge cases
- Miri interpreter implements runtime checking
- Helps standardize unsafe code semantics
- Foundation for formal verification efforts

## Slide 11: Question for You
Could we preserve safety while enabling optimizations in this model?
