Generate 11 presentation slides based on the podcast about "A Catalogue of Optimizing Transformations" by Frances E. Allen and John Cocke.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Compiler Optimization Catalog
- Systematic catalogue of compiler optimization transformations
- Focus on procedure integration and interprocedural analysis
- Foundation laid by Allen and Cocke for modern compiler design
- Key techniques: constant folding, dead code elimination, code motion

## Slide 2: Procedure Integration and Open Linkage
- Procedure integration enables cross-function optimizations
- Open linkage concept allows inlining function calls
- Modern equivalent: inline functions in C++ and other languages
- Enables compiler to see and optimize larger code contexts

## Slide 3: Pure Functions and Side Effect Analysis
- Pure functions produce no side effects beyond return values
- Compiler can analyze which global variables functions modify
- Side effect analysis enables aggressive optimization opportunities
- Critical for determining when functions can be reordered or eliminated

## Slide 4: Parallel Execution Opportunities
- Understanding function dependencies opens parallelization potential
- Compiler can identify independent computations
- Enables automatic parallel execution on multicore systems
- Foundation for modern auto-vectorization and parallel code generation

## Slide 5: Constant Folding Optimization
- Compile-time evaluation of constant expressions
- Reduces runtime computation overhead
- Example: `2 + 3` becomes `5` at compile time
- Idempotent transformation that consistently produces same results

## Slide 6: Dead Code Elimination
- Removes unreachable or unused code segments
- Reduces binary size and improves cache performance
- Identifies code that never executes or whose results are never used
- Clean-up transformation after other optimizations create dead code

## Slide 7: Code Motion and Loop Unswitching
- Moving loop-invariant computations outside loops
- Loop unswitching moves conditional checks outside loop bodies
- Reduces redundant computation in tight loops
- Significant performance improvements in iterative algorithms

## Slide 8: Register Allocation Optimization
- Efficient mapping of variables to CPU registers
- Minimizes expensive memory access operations
- Uses graph coloring and interference analysis
- Critical for maximizing performance on register-constrained architectures

## Slide 9: Interaction Between Optimizations
- Multiple optimization passes can interfere or enable each other
- Dead code elimination creates opportunities for further optimization
- Order of optimization passes affects final code quality
- Requires careful orchestration of transformation sequence

## Slide 10: Impact on Compiler Design
- Established framework for modern optimizing compilers
- Thousands of potential optimization passes in production compilers
- Balance between compilation time and code quality
- Foundation for GCC, LLVM, and other modern compiler infrastructures

## Slide 11: Question for You
Or perhaps, on the contrary, does it open up completely new vistas that Allen and Cocke never even dreamed of?
