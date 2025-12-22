Generate 11 presentation slides based on the podcast about Smashing the Stack for Fun and Profit.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Buffer Overflow Attacks

- Buffer overflow: writing data beyond allocated memory boundaries
- Classic exploit technique targeting x86 architecture stack
- Enables arbitrary code execution by overwriting return addresses
- Foundation paper from Phrack magazine that defined modern exploitation
- Understanding requires knowledge of C memory layout and assembly

## Slide 2: The Stack Memory Model

- Stack grows downward in memory (from high to low addresses)
- Function call pushes return address onto stack
- Local variables allocated on stack frame
- Frame pointer (EBP) and stack pointer (ESP) track current frame
- Buffer overflow occurs when copying data without bounds checking

## Slide 3: Anatomy of a Function Call

- Caller pushes arguments onto stack in reverse order
- CALL instruction pushes return address (EIP)
- Callee pushes old frame pointer and sets up new frame
- Local variables allocated by moving stack pointer
- Return instruction pops saved EIP and jumps back

## Slide 4: The Buffer Overflow Vulnerability

- Simple example: buffer[16] with strcpy() from user input
- No bounds checking allows writing past buffer end
- Overwriting return address redirects execution flow
- Author demonstrates with concrete memory layout examples
- Vulnerability present in standard C library functions

## Slide 5: Crafting Exploit Shellcode

- Shellcode: machine code that spawns a shell process
- Must avoid null bytes (0x00) which terminate strings
- Typical size: 24-45 bytes for execve("/bin/sh") syscall
- Written in assembly and hand-encoded as hex bytes
- Example: execve system call with string pointer setup

## Slide 6: The NOP Sled Technique

- Challenge: exact stack address unknown due to environment variables
- NOP sled: large sequence of 0x90 (no-operation) instructions
- Jumping anywhere in sled eventually reaches shellcode
- Makes exploit reliable without knowing precise addresses
- Typical sled size: hundreds of bytes before payload

## Slide 7: Overwriting the Return Address

- Fill buffer with NOP sled + shellcode + repeated return address
- Return address points into middle of NOP sled
- When function returns, execution slides into shellcode
- Example: 0x41414141 overflow test becomes real address
- Successful exploit grants shell with target program privileges

## Slide 8: Dealing with String Termination

- Problem: shellcode contains "/bin/sh" string with null bytes
- Solution: construct string on stack at runtime
- Use relative addressing and self-modifying techniques
- CALL instruction pushes next address (string location) onto stack
- Shellcode retrieves own string pointer from stack

## Slide 9: Historical Impact and Defense Evolution

- Paper published in 1996, defined exploitation methodology
- Led to widespread understanding of memory corruption bugs
- Sparked development of protection mechanisms (DEP, ASLR, stack canaries)
- Despite defenses, buffer overflows remain relevant today
- Modern exploits chain multiple techniques to bypass protections

## Slide 10: From Theory to Practice

- Small code changes (16-byte buffer) enable complete system compromise
- Demonstration shows exploit reliability with NOP sled padding
- Environment variables and stack layout affect exploit success
- Real-world exploitation requires adapting to target system specifics
- Paper democratized knowledge previously known to few security researchers

## Slide 11: Question for You

If modern systems have stack canaries, DEP, and ASLR protections, why do buffer overflow vulnerabilities still lead to successful exploits today?
