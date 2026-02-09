Generate 11 presentation slides based on the podcast about Linear Types by Martin Odersky.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Linear Types
- Linear types ensure each value is used exactly once in program execution
- Proposed by Martin Odersky as extension to type reconstruction systems
- Addresses memory safety and resource management in functional programming
- Combines mathematical purity with practical engineering concerns
- Foundation for modern resource tracking in languages like Rust

## Slide 2: Background - The Observer Pattern Problem
- Traditional observer pattern requires manual subscription/unsubscription management
- Memory leaks occur when observers aren't properly removed from subject
- Type systems before linear types couldn't enforce cleanup guarantees
- Developers relied on discipline and testing rather than compile-time safety
- This motivated research into type-level resource tracking

## Slide 3: Core Concept - Use Exactly Once
- Linear types guarantee each reference is consumed exactly once
- Prevents both use-after-free and resource leaks at compile time
- Functions must explicitly pass linear values through or consume them
- Type system tracks ownership and prevents aliasing of linear resources
- Automatic verification replaces manual lifetime management

## Slide 4: Challenges in Early Linear Type Systems
- Initial implementations were cumbersome and verbose in practice
- Required extensive type annotations from developers
- Limited composability with existing non-linear code
- Poor ergonomics led to low adoption despite theoretical benefits
- Integration with type inference was particularly difficult

## Slide 5: Odersky's Innovation - Type Reconstruction
- Unified linear and non-linear types in single coherent system
- Automatic inference determines which values need linear treatment
- Developers write natural code without excessive annotations
- System reconstructs linear/non-linear distinction during type checking
- Maintains safety guarantees while improving usability

## Slide 6: Practical Application - Safe Resource Management
- File handles, network sockets must be used exactly once
- Type system prevents resource leaks through static analysis
- No runtime overhead for linearity checks
- Compiler generates cleanup code automatically where needed
- Explicit ownership transfer replaces garbage collection for critical resources

## Slide 7: Integration with Existing Type Systems
- Linear types compose with polymorphism and higher-order functions
- Clean separation between linear and unrestricted (copyable) types
- Subtyping allows safe conversion from linear to unrestricted
- Type inference minimizes annotation burden on developers
- Backwards compatibility with non-linear legacy code

## Slide 8: Implementation Techniques
- Type reconstruction algorithm operates in multiple passes
- First pass collects constraints from program structure
- Second pass solves constraint system to determine linearity
- Unification handles polymorphic functions with mixed linear/non-linear parameters
- Efficient implementation adds minimal compilation overhead

## Slide 9: Performance and Optimization Benefits
- In-place updates safe when value has unique reference
- Eliminates defensive copying in many scenarios
- Predictable memory usage without garbage collection pauses
- Compiler can generate more efficient code with ownership information
- Zero-cost abstraction for resource safety

## Slide 10: Influence on Modern Languages
- Rust's ownership system builds on linear type principles
- Clean separation between owned, borrowed, and shared references
- Widespread adoption proves practical value of the approach
- Many techniques from paper appear in production compilers today
- Demonstrates balance between mathematical rigor and engineering pragmatism

## Slide 11: Question for You
Is the key to the next revolution in programming finding the perfect balance between mathematical purity and engineering pragmatism?
