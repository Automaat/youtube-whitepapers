Generate 11 presentation slides based on the podcast about KLEE: Unassisted and Automatic Generation of High-Coverage Tests for Complex Systems Programs.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to KLEE - Symbolic Execution Engine

- KLEE is an automatic test generation tool using symbolic execution
- Explores all possible execution paths through a program systematically
- Designed for complex system programs written in C
- Developed at Stanford University, published in 2008
- Aims to achieve high code coverage and detect bugs automatically

## Slide 2: The Challenge of Software Testing

- Even simple programs have exponentially many execution paths
- Manual testing cannot cover all possible inputs and edge cases
- Traditional random testing (fuzzing) is inefficient and unpredictable
- Critical bugs often hide in rarely-executed code paths
- Need for systematic, comprehensive testing approach

## Slide 3: Symbolic Execution vs Fuzzing

- Fuzzing: randomly generates inputs hoping to trigger crashes
- Symbolic execution: treats inputs as symbolic variables, not concrete values
- Explores program paths systematically using constraint solving
- Each branch creates new constraints on symbolic variables
- Guarantees to explore all reachable program states

## Slide 4: How KLEE Works - Core Mechanism

- Replaces concrete input values with symbolic variables
- Tracks constraints on variables at each program branch
- Uses constraint solver (STP) to determine path feasibility
- Forks execution state at each conditional branch
- Generates concrete test cases from constraint solutions

## Slide 5: State Space Exploration Strategies

- Cannot explore infinite state space exhaustively
- Uses heuristics to prioritize which states to explore first
- Tracks code coverage to guide exploration toward untested code
- Manages execution state tree to avoid exponential blowup
- Balances breadth-first and depth-first exploration strategies

## Slide 6: Finding Bugs with KLEE

- Detects buffer overflows, null pointer dereferences, assertion failures
- Automatically generates minimal test cases that reproduce bugs
- Reports exact execution path leading to each bug
- Provides concrete input values that trigger the error
- Can verify absence of certain bug classes in explored paths

## Slide 7: KLEE vs Real-World Software

- Tested on GNU Coreutils (89 programs, ~80k lines of code)
- Achieved over 90% line coverage on most utilities
- Found 56 serious bugs in widely-used production software
- Tested on BusyBox embedded utilities
- Discovered 21 bugs including critical filesystem corruption issues

## Slide 8: Critical Bug Discoveries

- Buffer overflow in `paste` utility from Coreutils
- Integer overflow leading to buffer overrun in BusyBox
- Data corruption in BusyBox `cp` command copying files
- Memory safety violations in mature, well-tested code
- Bugs that had existed undetected for years in production systems

## Slide 9: Performance and Scalability

- Can analyze ~100,000 lines of code in hours
- Constraint solving is the main performance bottleneck
- Uses optimizations: constraint caching, state merging
- Achieved better coverage than manual test suites in less time
- Practical for integration into development workflows

## Slide 10: Impact and Legacy

- Demonstrated symbolic execution viability for real-world systems
- Found critical bugs in HISTAR operating system kernel
- Influenced modern testing tools (AFL, libFuzzer with symbolic execution)
- Showed that formal methods can be automated and practical
- Bridged gap between academic research and industry practice

## Slide 11: Question for You

But what if we could automatically create software whose correctness is mathematically proven at the time of writing?
