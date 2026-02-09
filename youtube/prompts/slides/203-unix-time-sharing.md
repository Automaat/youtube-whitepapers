Generate 11 presentation slides based on the podcast about "The UNIX Time-Sharing System".

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Revolutionary Design Philosophy
- Everything is a file: devices, directories, and regular files share unified interface
- Simple, elegant abstractions that hide hardware complexity
- Hierarchical file system with mountable volumes
- Minimalist approach: small tools that do one thing well
- Written in C language for portability across hardware platforms
- Design principles that influenced all modern operating systems

## Slide 2: The File System Architecture
- Hierarchical tree structure starting from root directory
- I-node system: metadata separated from file names
- Each i-node contains file attributes, ownership, permissions, timestamps
- Hard links: multiple directory entries pointing to same i-node
- Efficient disk space management with block allocation
- Special files representing devices treated as regular files

## Slide 3: Process Model and Management
- Every process created by forking parent process
- Fork creates exact copy of parent process
- Exec replaces process image with new program
- Parent-child process relationships form process tree
- Init process (PID 1) as ancestor of all user processes
- Simple process lifecycle: fork, exec, wait, exit

## Slide 4: The Shell - Command Interpreter
- User interface to the operating system
- Interactive command execution and scripting capabilities
- Job control: background and foreground processes
- Command history and line editing
- Variable expansion and command substitution
- Scripts as executable programs using shebang (#!)

## Slide 5: Input/Output Redirection
- Standard input (stdin), output (stdout), error (stderr) streams
- Redirect output to files using > and >> operators
- Redirect input from files using < operator
- File descriptors as abstraction for I/O channels
- Programs unaware of redirection - handled by shell
- Separation of concerns: logic vs. I/O destination

## Slide 6: Pipes - The Power of Composition
- Connect output of one program to input of another
- Vertical bar | operator for creating pipelines
- Data flows through chain of simple utilities
- Filter programs: grep, sort, uniq, wc, sed, awk
- Complex operations built from simple building blocks
- Philosophy: write programs that work together

## Slide 7: Classic Pipeline Examples
- `ls | grep pattern` - filter file listings
- `cat file | sort | uniq` - remove duplicates
- `ps aux | grep process | awk '{print $2}'` - extract process IDs
- `find . -name "*.c" | wc -l` - count C source files
- Composability enables unlimited combinations
- Each tool focused, testable, reusable

## Slide 8: Development Tools Ecosystem
- C compiler (cc) integrated into system
- Make for automated build management
- Debugger (adb, later gdb) for program analysis
- Version control systems (SCCS, later RCS)
- Text processing: troff, nroff, eqn, tbl
- Development environment as core system feature

## Slide 9: Simplicity as Design Goal
- Small kernel with minimal complexity
- User programs implement policy, kernel provides mechanism
- No special cases or exceptions in design
- Code clarity over performance optimization
- Easy to understand, modify, and extend
- Rapid development and iteration enabled by simplicity

## Slide 10: Legacy and Impact
- Foundation for Linux, BSD, macOS, Android operating systems
- POSIX standards based on UNIX interfaces
- Shell scripting as universal automation tool
- Pipes and filters pattern in modern data processing
- Philosophy influences microservices and cloud architecture
- Design principles remain relevant 50+ years later

## Slide 11: Question for You
What element of UNIX design philosophy has been lost in modern systems that cannot be consciously recreated?
