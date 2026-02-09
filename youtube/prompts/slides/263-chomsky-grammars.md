Generate 11 presentation slides based on the podcast about Chomsky's formal grammars and their hierarchy.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Formal Grammars
- Formal grammars provide mathematical framework for describing language structure
- Chomsky hierarchy classifies grammars by expressive power and computational complexity
- Four levels from Type-3 (most restricted) to Type-0 (unrestricted)
- Foundation for compiler design, natural language processing, and formal language theory
- Essential tool bridging linguistics and computer science

## Slide 2: Type-3: Regular Grammars
- Recognized by finite state automata (FSA)
- Linear structure with no memory or nesting
- Defined by regular expressions: patterns without recursion
- Applications: lexical analysis, text pattern matching, simple protocol validation
- Limitations: cannot handle balanced parentheses or nested structures
- Examples: identifiers, keywords, simple tokens in programming languages

## Slide 3: Type-2: Context-Free Grammars
- Recognized by pushdown automata (PDA) with stack memory
- Handles nested structures through recursive production rules
- Foundation for most programming language syntax (BNF notation)
- Enables parsing of arithmetic expressions, balanced parentheses, nested blocks
- More powerful than regular grammars but still decidable
- Examples: JSON, XML, most programming language grammars

## Slide 4: Type-1: Context-Sensitive Grammars
- Production rules can depend on surrounding context
- Recognized by linear bounded automata
- More expressive than context-free but exponentially harder to parse
- Natural language phenomena requiring agreement and dependencies
- Rarely used in practice due to computational complexity
- Example: subject-verb agreement across arbitrary distances

## Slide 5: Type-0: Unrestricted Grammars
- Equivalent to Turing machines in computational power
- No restrictions on production rules
- Can recognize any recursively enumerable language
- Theoretical construct - parsing is undecidable in general
- Too powerful for practical parsing applications
- Demonstrates limits of what grammars can express

## Slide 6: The Chomsky Hierarchy Structure
- Strict containment: Type-3 ⊂ Type-2 ⊂ Type-1 ⊂ Type-0
- Each level adds computational capability and complexity
- Trade-off between expressiveness and parsing efficiency
- Type-3: O(n) parsing time with FSA
- Type-2: O(n³) parsing time with CYK algorithm
- Type-1/Type-0: exponential or undecidable complexity

## Slide 7: Self-Embedding and Recursion
- Self-embedding: grammar rules that refer to themselves with surrounding context
- Enables infinite nesting: "the cat that chased the rat that ate the cheese"
- Key difference between Type-2 (context-free) and Type-3 (regular)
- Pushdown automaton's stack provides memory for nested structures
- Regular automata lack this capability - no center-embedding possible
- Fundamental mechanism for hierarchical structure in languages

## Slide 8: Practical Applications in Compilers
- Lexical analysis uses regular expressions (Type-3)
- Syntax parsing uses context-free grammars (Type-2)
- Most modern languages designed to be parsable with CFG
- Parser generators: Yacc, ANTLR, Bison use CFG notation
- Deterministic subsets (LALR, LL) enable efficient O(n) parsing
- Type-1 and Type-0 avoided due to complexity

## Slide 9: Natural Language and Beyond CFG
- Natural languages exhibit phenomena beyond context-free capability
- Cross-serial dependencies in Swiss German, Dutch
- Long-distance agreement and discontinuous constituents
- However, most practical NLP uses CFG with extensions
- Probabilistic CFG, feature structures add expressive power
- Modern neural approaches sidestep formal grammar hierarchies

## Slide 10: Impact on Computer Science
- Established formal foundation for programming language design
- Enabled systematic compiler construction methodology
- Transformed linguistics from descriptive to mathematical science
- Influenced automata theory and computational complexity
- Chomsky's work connected linguistics, logic, and computation
- Paradigm shift: from ad-hoc approaches to rigorous formal methods

## Slide 11: Question for You
Or perhaps something completely different?
