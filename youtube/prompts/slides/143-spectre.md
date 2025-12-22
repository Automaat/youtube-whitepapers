Generate 11 presentation slides based on the podcast about Spectre.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Spectre Attack - Exploiting Speculative Execution

- Discovered in 2018 as critical CPU vulnerability affecting Intel, AMD, and ARM processors
- Exploits speculative execution optimization where processors predict code paths before confirmation
- Allows attackers to read privileged memory including passwords, encryption keys, and kernel data
- Works across process boundaries and security domains without leaving traditional attack traces
- Named Spectre because threat haunts speculative execution across processor architectures

## Slide 2: Speculative Execution Fundamentals

- Modern processors predict branch outcomes to avoid pipeline stalls and maintain performance
- Branch Target Buffer (BTB) stores history of conditional jumps and their outcomes
- Processor executes predicted code path speculatively before condition is resolved
- On correct prediction, results are committed; on misprediction, results are discarded
- Critical issue: discarded results leave microarchitectural side effects in cache state

## Slide 3: Cache-Based Side Channel Attack

- Speculative execution modifies CPU cache state before rollback occurs
- Cache timing differences reveal which memory addresses were speculatively accessed
- Attacker measures access time to probe arrays: fast=cached (recently accessed), slow=not cached
- Flush+Reload technique: flush cache line, trigger victim code, measure reload time
- Side channel converts protected memory values into observable timing patterns

## Slide 4: Training the Branch Predictor

- Attackers manipulate BTB by repeatedly executing code with predictable patterns
- Train processor to predict specific branch direction through controlled inputs
- After training, inject malicious input that causes misprediction
- During misprediction window, speculatively execute code accessing privileged memory
- Predictor's "muscle memory" becomes attack vector for controlled speculation

## Slide 5: Cross-Domain Information Leakage

- Spectre breaks isolation between processes, virtual machines, and browser tabs
- JavaScript attack demonstrated reading data from different browser tabs
- Google Project Zero proved concept with kernel memory reads from userspace
- Works across virtualization boundaries and containerized environments
- Undermines fundamental security assumptions about memory protection

## Slide 6: Indirect Branch Prediction Vulnerability

- Indirect branches (function pointers, virtual calls) have unpredictable targets at compile time
- BTB uses partial address bits for indexing, creating aliasing between different code locations
- Attacker trains predictor with one code location, triggers speculation at another
- Enables "gadget" attacks using existing code fragments as speculative execution primitives
- No new malicious code needed - exploits legitimate code through misprediction

## Slide 7: Gadget-Based Exploitation

- Gadgets are code fragments in existing programs that become exploit primitives
- Attacker chains gadgets to build complex speculative execution payloads
- Example: array bounds check gadget that speculatively reads out-of-bounds data
- Similar to Return-Oriented Programming (ROP) but using speculative execution instead of stack
- Makes exploitation possible without injecting custom code or bypassing DEP/ASLR

## Slide 8: Industry Response and Mitigation Impact

- Vulnerability affected virtually all modern processors from Intel, AMD, ARM
- Required coordinated disclosure and patching across operating systems and browsers
- Mitigations included: retpoline, IBRS (Indirect Branch Restricted Speculation), IBPB (Indirect Branch Predictor Barrier)
- Performance penalty ranged from 5% to 30% depending on workload characteristics
- Demonstrated fundamental tension between security and performance optimization

## Slide 9: Performance Cost of Mitigation

- Software patches significantly impacted performance in I/O-intensive workloads
- Database and virtualization workloads experienced measurable slowdowns
- Kernel-heavy operations suffered most due to increased context switching overhead
- Some environments chose to accept risk rather than enable full mitigations
- Long-term solution requires hardware redesign with security-aware speculation

## Slide 10: Detection and Defense Challenges

- Traditional security tools cannot detect Spectre exploitation in progress
- No memory corruption or privilege escalation in conventional sense occurs
- Requires statistical analysis and timing measurements to detect attacks
- Defense requires architectural changes, not just software patches
- Highlighted need for security considerations in microarchitecture design phase

## Slide 11: Question for You

What security assumptions in your current systems might be undermined by microarchitectural side channels like Spectre?
