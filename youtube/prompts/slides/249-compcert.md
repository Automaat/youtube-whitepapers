Generate 11 presentation slides based on the podcast about CompCert: Formally Verified Optimizing C Compiler.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: CompCert - Verified C Compiler
- First formally verified optimizing C compiler with machine-checked correctness proof
- Targets safety-critical embedded systems where compiler bugs are unacceptable
- Guarantees compiled program preserves exact semantics of source C code
- Proven using Coq proof assistant with complete mechanized verification

## Slide 2: The Compiler Correctness Problem
- Traditional compilers like GCC contain bugs that can silently introduce errors
- Compiled program may behave differently than source code intends
- Critical for safety systems: aviation, medical devices, nuclear control
- CompCert provides mathematical proof that compilation preserves program behavior

## Slide 3: Supported C Language Features
- Full ISO C90 (ANSI C) language support with most C99 extensions
- Pointers, structures, unions, arrays with complete semantics
- Loops, recursion, function pointers, goto statements
- Variable-argument functions (varargs) and dynamic memory allocation
- Missing: longjmp/setjmp, inline assembly, unstructured switch statements

## Slide 4: Multi-Stage Compilation Pipeline
- 14 distinct compilation passes from C to assembly code
- Each pass performs small, verifiable transformation independently
- Early stages: type checking, normalization, control flow simplification
- Middle stages: register allocation, instruction selection, optimizations
- Late stages: assembly generation for PowerPC architecture

## Slide 5: Formal Verification Approach
- Each compilation pass proven correct using Coq theorem prover
- Semantic preservation theorem: if source program has behavior B, compiled code has same behavior B
- Proofs compose: overall correctness follows from individual pass correctness
- Machine-checked proofs eliminate human error in verification process

## Slide 6: Performance vs Correctness Trade-offs
- CompCert slower than GCC -O1 optimization level by ~10%
- Avoids aggressive optimizations that are difficult to verify formally
- Focuses on correctness-preserving transformations with high confidence
- Acceptable performance penalty for safety-critical applications

## Slide 7: Memory Model and Semantics
- Precise operational semantics for C memory operations defined in Coq
- Handles pointer arithmetic, type casting, undefined behavior explicitly
- Block-based memory model with provenance tracking for safety
- Formally specifies what transformations preserve observable behavior

## Slide 8: Verified vs Unverified Components
- Verified core: parser, type checker, all optimization passes, code generator
- Unverified guardian: validator checks verification assumptions before proceeding
- Unverified components: assembler, linker (rely on external tools)
- If guardian detects violation, compilation halts with error - no silent bugs

## Slide 9: Practical Results and Performance
- Successfully compiles real embedded C programs for safety-critical systems
- Code size within 10% of GCC output for most benchmarks
- Execution speed 87-90% of GCC -O1 optimized code on PowerPC
- Proof development: ~50,000 lines of Coq specifications and proofs

## Slide 10: Impact on Compiler Research
- Demonstrates feasibility of building realistic verified compilers
- Established foundation for formal compiler verification methodology
- Influenced CompCertX, CakeML, Vellvm and other verified compiler projects
- Shows formal methods can scale to complex systems software

## Slide 11: Question for You
What are the implications of having formally verified compilers for the foundations of tools we use to create software?
