Generate 11 presentation slides based on the podcast about LLVM: A Compilation Framework for Lifelong Program Analysis and Transformation.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction - The Silent Hero of Modern Software
- LLVM powers iPhone, PlayStation, Chrome, and countless other systems
- Paper by Chris Lattner and Vikram Adve: compilation framework for lifelong program analysis
- Key concept: "Lifelong" compilation - not one-time act, but continuous evolution
- Fundamental shift: compiled code as living document, not frozen artifact
- Enables code to improve throughout application lifecycle
- Breaks traditional thinking about compilation finality

## Slide 2: The Pre-LLVM Problem Space
- Developers stuck between performance and flexibility trade-offs
- Traditional compilers (GCC): fast machine code but lost high-level information
- Optimizations happened in isolated silos, linker had no semantic knowledge
- Virtual machines (JVM): runtime flexibility but imposed strict models
- Profile Guided Optimization (PGO) optimized for assumptions, not actual user behavior
- Need for universal intermediate representation that preserves context

## Slide 3: LLVM IR - The Universal Language
- Common intermediate representation between source and machine code
- "Latin of programming world" - universal logical language for optimizers
- Language-independent, well-defined representation
- Not beautiful source code, not raw machine code - something in between
- Enables universal communication between all compilation stages
- Foundation for all LLVM capabilities and innovations

## Slide 4: Type System - Preserving Semantic Context
- Language-independent type system defines fundamental building blocks
- Pointers, arrays, structures understandable by any programming language
- Optimizer maintains understanding of data shape even at low level
- Knows it's dealing with "array of objects" not shapeless memory blob
- Preserves precious context throughout entire compilation pipeline
- Enables type-aware optimizations previously impossible

## Slide 5: SSA Form - Eliminating Ambiguity
- Static Single Assignment: each virtual register assigned value only once
- Each variable version gets unique serial number - no ambiguity
- Eliminates all ambiguities in data flow tracking
- Trivially simple data flow enables powerful optimization classes
- Simplifies complex dependencies into set of one-way highways
- Fundamental enabler for modern optimization techniques

## Slide 6: Explicit Pointers and Exception Handling
- GetElementPtr instruction instead of raw pointer arithmetic
- Type-aware address calculation preserves structural information
- Explicit exception handling: invoke instruction with two possible exits
- C++ exceptions visible as explicit control flow graph paths
- Destructors modeled as explicit unwind blocks
- Everything visible and optimizable, no black magic

## Slide 7: The Five Key Capabilities
- Persistent Program Information: IR preserved through entire lifecycle
- Offline Code Generation: pre-generate optimized native code, not just JIT
- User-Based Profiling: collect real performance data, re-optimize in background
- Transparent Runtime Model: no imposed object model or garbage collector
- Uniform Whole-Program Compilation: optimize app + libraries + system libs together

## Slide 8: Practical Results - Size and Performance
- LLVM binaries with rich IR comparable to x86 machine code size
- 25% smaller than SPARC architecture binaries - SSA extremely compact
- Advanced global optimizations faster than GCC total compilation time
- Dead global elimination performed quickly, suitable for background optimization
- Proof of practical design, not just theoretical elegance
- Enables deep whole-program analysis GCC couldn't perform

## Slide 9: Type Information Recovery
- Data Structure Analysis verified types for 68% of static memory operations
- Phenomenal result in C language - a non-type-safe language
- Recovers invaluable information even from unsafe code
- Demonstrates robustness across different programming paradigms
- Enables optimizations previously impossible in unsafe languages
- Shows LLVM's power to understand code beyond source language limitations

## Slide 10: Philosophy Shift - Living Code Documents
- Not just better compiler - entirely different compilation philosophy
- Compiled code as cloud document (constantly editable) vs stone tablet (immutable)
- LLVM IR as language enabling living document model
- Reconciled fire and water: native performance + VM flexibility
- Shaped software landscape for two decades
- Foundation for implementing higher-level VMs (JVM, CLI) on top

## Slide 11: Question for You
Since we have such a universal, low-level optimization foundation, what is the future of monolithic virtual machines tailored to single languages? Won't they eventually become just sets of libraries running on shared, globally-optimized infrastructure provided by LLVM?
