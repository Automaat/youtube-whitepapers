Generate 11 presentation slides based on the podcast about RFC 1: Host Software.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: RFC 1: The Digital Rosetta Stone (April 7, 1969)

- First Request for Comments document by Steve Crocker at UCLA
- Published before the Moon landing, marking ARPANET's birth
- Not a final specification but an invitation to collaborative discussion
- Established "Request for Comments" culture: open academic cooperation
- DNA of early internet development through shared problem-solving

## Slide 2: ARPANET Architecture: Hosts and IMPs

- Host: large university computers running applications
- IMP (Interface Message Processor): dedicated network gateway for each host
- IMP handled all network operations for the host
- Host sent messages up to 8,000 bits to local IMP
- IMP divided messages into ~1,000-bit packets for transmission
- Early implementation of packet switching concept

## Slide 3: Network Integrity and Error Control

- IMP guaranteed transmission integrity between network nodes
- 24-bit Cyclic Check Sum for error detection
- Hosts didn't worry about bit-level errors between IMPs
- Error handling abstracted to lower network layer
- Foundation for layered network architecture

## Slide 4: Logical Links: 32 Virtual Connections

- Each host pair had 32 pre-allocated bidirectional logical links
- Links always active (like 32 dedicated telephone lines)
- Static allocation simplified IMP programming
- Traded memory efficiency for implementation simplicity
- Priority: reliability and ease of programming over optimization

## Slide 5: Flow Control with RFNM

- RFNM (Request for Next Message) prevented receiver overload
- Sender couldn't transmit next message until RFNM received
- Simple but effective congestion prevention mechanism
- Only worked with one or two congestion sources
- Required gentlemen's agreement: hosts cooperated voluntarily

## Slide 6: Simple Use: TTY Remote Terminal

- Link 0 reserved for OS-to-OS communication
- Request sent via Link 0 to establish connection (e.g., Link 15)
- Remote computer behaved like local TTY terminal
- Race condition solved by host ID priority scheme
- Lower ID host yielded during simultaneous link requests

## Slide 7: Deep Use: File-Like Connections

- Second connection type for efficient data transfer
- No scanning for special control characters
- Treated data as pure binary stream
- Used buffering for large block transfers
- Optimized for throughput instead of interactivity

## Slide 8: The Half-Second Delay Problem

- Round-trip latency estimated at 0.5 seconds per keystroke
- Example: typing "HELP" with corrections = 9 keystrokes
- Waiting for echo after each key would be unbearable
- Challenge identified: user experience in face of network delay
- Same problem modern UX designers face today

## Slide 9: DEL: Display Controlling Element Language

- Revolutionary solution: send executable code to client machine
- Remote server sends small DEL program to local host
- Local "Frontend" program handles all terminal interactions instantly
- Only final edited command sent over network as single message
- Predecessor to modern JavaScript client-side execution model

## Slide 10: Open Questions and Planned Experiments

- Why 8-bit link field for only 32 links? (planning for scale)
- Missing detailed host-IMP interface specification
- Checksum problems when IMP modifies character encoding
- Experiment 1: SRI's NLS system via TTY terminals with DEL
- Experiment 2: Full graphical NLS with mouse remotely from UCLA and Utah

## Slide 11: Question for You

If the creators of RFC 1 solved network delay in 1969 by sending executable code to the client (DEL), are modern web applications just a more sophisticated version of the same fundamental solution?
