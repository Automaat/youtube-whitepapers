Generate 11 presentation slides based on the podcast about Oxide: The Essence of Rust.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Oxide - Formalizing Rust's Ownership
- First formal model of Rust's core type system including ownership and borrowing
- Addresses the challenge of verifying Rust's memory safety guarantees
- Provides mathematical foundation for understanding Rust's borrow checker
- Enables formal reasoning about safe and unsafe code interactions

## Slide 2: The Challenge - Rust's Ownership System Complexity
- Ownership system prevents data races and memory errors at compile time
- Complex rules around borrowing, lifetimes, and mutable/immutable references
- Compiler must track ownership transfers and borrow lifetimes precisely
- Need for formal verification to ensure soundness of type system

## Slide 3: Oxide's Core Components - Semantic Model
- Syntactic types (surface-level Rust types programmers write)
- Semantic types (runtime representation with ownership tracking)
- Loan tracking mechanism to manage active borrows
- Permission system controlling read/write/move access to memory locations

## Slide 4: Permission Model - Fine-Grained Access Control
- Three permission types: readable, writable, movable
- Permissions change dynamically based on borrows and ownership transfers
- Mutable borrow requires exclusive writable permission
- Immutable borrow allows multiple simultaneous readable permissions
- Move operation transfers ownership and invalidates source

## Slide 5: Loan Tracking - Managing Borrows and Lifetimes
- Loans track active references and their validity regions
- Each borrow creates a loan that must be properly ended
- Nested borrows require careful permission management
- Ensures references cannot outlive the data they point to

## Slide 6: Ownership Transfer - How Move Semantics Work
- When ownership transfers, original location loses all permissions
- Move invalidates source variable preventing use-after-move errors
- Compiler tracks ownership flow through function calls and assignments
- Prevents double-free and use-after-free vulnerabilities

## Slide 7: Non-Lexical Lifetimes (NLL) - Advanced Borrow Checking
- Traditional lifetimes tied to lexical scopes too restrictive
- NLL allows borrows to end when last use occurs, not at scope end
- Enables more flexible borrowing patterns that are still safe
- Major improvement in Rust ergonomics without sacrificing safety

## Slide 8: Reborrowing - Temporary Permission Delegation
- Allows creating new borrows from existing references
- Temporary suspension of permissions on original borrow
- Enables passing borrowed references through function chains
- Precise tracking ensures all reborrows respect original loan constraints

## Slide 9: Soundness Guarantees - Type Safety Theorems
- Progress theorem: well-typed programs don't get stuck
- Preservation theorem: well-typed programs remain well-typed during execution
- Type soundness ensures memory safety guarantees hold
- Formal proof that unsafe code boundaries are properly isolated

## Slide 10: Impact - Rust Belt and Future Verification
- Oxide provides foundation for Rust Belt verification framework
- Enables machine-checked proofs of Rust program correctness
- First rigorous formalization of Rust's ownership system
- Opens path for verifying critical systems written in Rust

## Slide 11: Question for You
Are we witnessing the beginning of the end for an entire class of bugs related to concurrent data access?
