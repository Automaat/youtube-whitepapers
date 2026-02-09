Generate 11 presentation slides based on the podcast about YACC (Yet Another Compiler-Compiler).

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to YACC
- YACC is a parser generator tool for creating compilers
- Takes grammar specification as input, generates C code parser
- Works in tandem with Lex for lexical analysis
- Widely adopted tool that shaped compiler construction practices
- Published in 1975 by Stephen C. Johnson at Bell Labs

## Slide 2: How YACC Works - Input and Output
- Input: Grammar specification file defining language syntax rules
- Grammar written in BNF-like notation with actions
- YACC processes specification to generate ytab.c file
- Output is complete C source code for parser implementation
- Generated parser can be compiled and linked with other code

## Slide 3: Integration with Lex
- Lex generates lexical analyzer (tokenizer)
- YACC parser calls Lex to get tokens
- Two-phase compilation: Lex breaks input into tokens, YACC parses structure
- Clean separation between lexical and syntactic analysis
- Combined tools create complete front-end for compilers

## Slide 4: Grammar Rules and Syntax
- Rules define productions like "expression: expression '+' term"
- Left side is non-terminal, right side is pattern to match
- Supports recursive rules for complex nested structures
- Actions in curly braces execute when rule matches
- Terminal symbols come from Lex, non-terminals defined in grammar

## Slide 5: Parser Generation Process
- YACC analyzes grammar to build parsing tables
- Creates LR(1) or LALR parser automatically
- Handles shift-reduce and reduce-reduce decisions
- Reports conflicts that need resolution
- Generates efficient table-driven parser code

## Slide 6: Semantic Actions
- Code blocks attached to grammar rules
- Execute when parser recognizes pattern
- Build abstract syntax trees or symbol tables
- Access values of matched symbols via $1, $2, etc.
- Return value via $$ for use in parent rules

## Slide 7: Example - Simple Assignment
- Input: "a = 7"
- Lex tokenizes: IDENTIFIER('a'), EQUALS, NUMBER(7)
- Parser matches assignment rule
- Semantic action builds AST node
- Result stored in parse tree for code generation

## Slide 8: Conflict Resolution
- Shift-reduce conflicts: should parser shift token or reduce rule?
- Reduce-reduce conflicts: multiple rules match same input
- Operator precedence declarations resolve ambiguities
- Default: shift takes priority over reduce
- Can lead to subtle, hard-to-debug parsing errors

## Slide 9: Operator Precedence and Associativity
- Declare precedence levels for operators
- Specify left or right associativity
- Resolves grammar ambiguities without rewriting rules
- Examples: + and - same precedence, left associative
- * and / higher precedence than + and -

## Slide 10: Accessing Parsed Values
- $1, $2, $3 reference symbols in current rule
- $1 is first symbol, $2 is second, etc.
- $$ sets return value for the rule
- Values passed up the parse tree
- Enables bottom-up evaluation during parsing

## Slide 11: Question for You
Is proper conflict resolution achieved through careful grammar design or explicit precedence declarations?
