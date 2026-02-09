Generate 11 presentation slides based on the podcast about John McCarthy's 1960 LISP paper.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: LISP - A Revolutionary Approach to AI Programming
- McCarthy's April 1960 paper: not just a language specification, but a philosophical and engineering manifest
- Goal: create a tool for the "Advice Taker" system - a machine that reasons using common sense
- Example: tell the machine "I am at home" and "my desk is at home", then ask "how do I get to my desk?"
- Required a language operating on logic and symbols, not just numbers
- Foundation for symbolic computation and artificial intelligence research

## Slide 2: Conditional Expressions - A New Computational Notation
- Traditional mathematical notation was declarative (states facts), not operational (describes processes)
- McCarthy introduced conditional expressions: `(p1 → e1, p2 → e2, ..., T → en)`
- Example - absolute value: `|x| = (x ≥ 0 → x, T → -x)`
- Evaluates conditions sequentially; first true condition determines the result
- Enables expression of computation paths rather than just equations
- Combines elegance with precision for describing algorithmic processes

## Slide 3: Recursion with Safe Termination
- Conditional expressions enable functions to call themselves without infinite loops
- Classic example - factorial: `n! = (n=0 → 1, T → n × (n-1)!)`
- Execution trace for factorial(2): 2×1!, then 1×0!, then 0!=1, unwinds to result 2
- Conditional acts as a "gate" stopping recursion at the exact right moment
- The branch `n × (n-1)!` is never evaluated when n=0, preventing errors
- Demonstrates universal mechanism for complex algorithms, not just a trick

## Slide 4: S-Expressions - Symbolic Data Structures
- LISP data are S-expressions (symbolic expressions), not numbers or strings
- Built from two primitives: atomic symbols (A, B, "Apple Pie No. 3") and ordered pairs `(E1 · E2)`
- Lists like `(A B C)` are syntactic sugar for nested pairs: `(A · (B · (C · NIL)))`
- NIL is a special atom marking list end
- Entire universe of data built from these two simple building blocks
- Enables thinking in real-world concepts rather than memory addresses

## Slide 5: Five Elementary Operations
- Five primitive functions form complete computational system:
- `ATOM(X)` - predicate checking if X is atomic
- `EQ(X,Y)` - predicate checking if two atoms are identical
- `CONS(X,Y)` - constructs new pair from two elements
- `CAR(X)` - extracts first element of pair (head)
- `CDR(X)` - extracts second element of pair (tail)
- CAR and CDR names from IBM 704: "Contents of Address/Decrement part of Register"

## Slide 6: Recursive List Processing
- Combining five primitives with recursion enables arbitrarily complex operations
- Example - FF(X) finds first atom in nested structure: `FF(X) = (ATOM(X) → X, T → FF(CAR(X)))`
- Execution for `FF((A B) C)`: not atom → take CAR → `(A B)`, not atom → take CAR → `A`, is atom → return `A`
- Works like a drill descending through nested pairs until hitting atomic element
- Can build functions like SUBST (symbol substitution) and EQUAL (tree comparison)
- Complete computational system from minimal foundation

## Slide 7: Homoiconicity - Code as Data
- Revolutionary idea: program instructions use same format as data they process
- Function `CONS(CAR(X), CDR(X))` translates to S-expression list: `(CONS (CAR X) (CDR X))`
- Function name is first atom, arguments are subsequent list elements
- Not magic but elegant representation - recipe for action becomes data structure
- Enables meta-programming: programs that write or modify other programs
- Source of LISP's power in AI research for decades

## Slide 8: APPLY - The Universal Interpreter
- Universal function APPLY brings data-as-code to life
- Takes two arguments: S-expression describing a function, and list of arguments
- APPLY examines function description and executes it, returning result
- Theoretical role: universal Turing machine; practical role: interpreter
- LISP interpreter written in LISP itself - language powerful enough to describe itself
- Opens door to self-modifying programs and program synthesis

## Slide 9: Memory Management - List Structures
- S-expressions implemented as "list structure" in machine memory
- Each pair occupies one machine word: address field stores CAR pointer, decrement field stores CDR pointer
- Entire nested structure is network of pointer-connected words
- Advantage: shared substructures stored once, referenced multiple times
- Example: list `(A B C)` appearing 100 times stored once with 100 pointers
- Huge savings of precious 1960s memory resources

## Slide 10: Garbage Collection - Automatic Memory Reclamation
- Challenge: programs create pairs via CONS, consuming free memory cells
- Free Storage List: simple list linking all available memory cells
- When free list exhausted, system runs "reclamation cycle" (garbage collection)
- Algorithm: start from base registers, follow CAR/CDR pointers marking reachable cells
- Sweep entire memory, return unmarked cells to free list
- Revolutionary cost: occasional pause for cleanup, enormous gain: freed programmers from manual memory tracking
- Legacy: every modern language (Java, Python, C#, Go) inherited this idea

## Slide 11: Question for You
What if we started thinking about all complex systems—not just programs, but biological, economic, and social systems—as large nested recursive structures? What new patterns might we discover?
