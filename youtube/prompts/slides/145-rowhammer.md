Generate 11 presentation slides based on the podcast about Rowhammer attacks.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Rowhammer

- Hardware vulnerability in DRAM memory discovered in 2014
- Exploitation through repeated memory access patterns
- Impact on memory isolation and security guarantees
- Physical phenomenon affecting modern high-density memory chips

## Slide 2: DRAM Memory Isolation Principle

- Memory access to address A should not affect data at address B
- Fundamental assumption for operating system security
- Process isolation relies on memory independence
- Violation of this principle enables privilege escalation

## Slide 3: DRAM Refresh Mechanism

- DDR3 memory requires refresh every 64 milliseconds
- Capacitors lose charge over time and need periodic restoration
- Refresh cycle ensures data integrity
- Standard operating procedure for DRAM controllers

## Slide 4: Row Structure in DRAM

- Memory cells organized in rows within banks
- Adjacent rows share physical proximity on silicon
- Electrical interference possible between neighboring rows
- Row addressing determines which cells are activated

## Slide 5: Evolution of Memory Vulnerability

- Older memory modules were resistant to bit flips
- Modern high-density chips more susceptible to interference
- Smaller transistors and reduced voltage margins
- Increased vulnerability with each technology generation

## Slide 6: Sequential vs. Targeted Access

- Normal memory access follows sequential patterns
- Rowhammer uses intentional repeated access to specific rows
- Rapid hammering of target addresses causes electrical disturbance
- Non-sequential patterns bypass standard protections

## Slide 7: Bit Flip Consequences

- Single bit flip can change value from 0 to 1 or vice versa
- Multiple bit flips dramatically increase attack possibilities
- Can modify security-critical data structures
- Enables privilege escalation and protection bypass

## Slide 8: Limitations of Existing Defenses

- ECC (Error-Correcting Code) insufficient against targeted attacks
- ECC designed for random single-bit errors, not systematic attacks
- Standard memory protection mechanisms don't address physical layer
- Hardware-level vulnerability requires hardware-level solutions

## Slide 9: Attack Probability and Detection

- DRAM controller can detect Rowhammer patterns with certain probability
- Sophisticated attacks can evade simple detection mechanisms
- Trade-off between performance and security monitoring
- Probabilistic nature makes defense challenging

## Slide 10: Attack Requirements and Constraints

- Requires precise physical memory mapping information
- Attacker needs to identify vulnerable memory locations
- Knowledge of DRAM organization and row adjacency essential
- Timing and access patterns must be carefully controlled

## Slide 11: Question for You

Has Rowhammer evolved into a separate research field since its publication?
