Generate 11 presentation slides based on the podcast about Stuxnet.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Stuxnet

- First documented cyber weapon designed for physical sabotage
- Discovered in 2010, targeting Iranian nuclear enrichment facilities
- Most sophisticated malware ever analyzed at discovery time
- Combined multiple zero-day exploits with rootkit capabilities

## Slide 2: Digital Sabotage Operation

- Pure digital sabotage campaign against physical infrastructure
- Targeted Siemens Step 7 PLCs (Programmable Logic Controllers)
- Designed to manipulate industrial control systems undetected
- Represented new era in cyber warfare capabilities

## Slide 3: Attribution and Analysis

- Geographic analysis revealed concentration in Iran
- Code contained string "MYRTUS" (possible biblical reference)
- Attribution pointed to nation-state actors with significant resources
- Sophisticated attack required deep knowledge of target systems

## Slide 4: Initial Infection Vector

- Primary distribution via USB drives (removable media)
- Exploited Windows autorun vulnerabilities
- Spread through air-gapped networks isolated from internet
- Required physical access or insider cooperation

## Slide 5: Air-Gap Penetration

- Overcame secure, isolated network architecture
- Used social engineering and supply chain infiltration
- Exploited trust relationships between contractors and facility
- Demonstrated vulnerability of air-gapped systems

## Slide 6: Zero-Day Exploit Arsenal

- Leveraged four different Windows zero-day vulnerabilities
- LNK/PIF vulnerability (CVE-2010-2568)
- Print spooler vulnerability
- Task scheduler privilege escalation
- Kernel-mode driver vulnerabilities

## Slide 7: Unprecedented Scale

- Used two stolen digital certificates for code signing
- Certificates from Realtek and JMicron legitimized malware
- Bypassed Windows driver signing requirements
- Demonstrated supply chain compromise capabilities

## Slide 8: Stealth and Persistence

- Rootkit components hid malware from antivirus detection
- Even curious investigators couldn't detect presence
- Multiple layers of obfuscation and encryption
- Self-preservation mechanisms ensured longevity

## Slide 9: PLC Manipulation

- Programmed to completely hide its modifications
- Altered centrifuge rotation speeds while showing normal readings
- Caused physical damage through frequency manipulation
- Operators saw fake data indicating normal operations

## Slide 10: Implications and Legacy

- Demonstrated feasibility of cyber-physical attacks
- Raised questions about cyber warfare ethics and norms
- Showed nation-states could conduct covert digital operations
- Changed perception of critical infrastructure security

## Slide 11: Question for You

How many such silent, undetected digital operations might be running right now, achieving their objectives in absolute secrecy?
