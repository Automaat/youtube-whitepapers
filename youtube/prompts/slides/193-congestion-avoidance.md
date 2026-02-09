Generate 11 presentation slides based on the podcast about "Congestion Avoidance and Control" by Van Jacobson and Michael J. Karels.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to TCP Congestion Problem
- TCP originally designed without congestion control mechanisms
- Network congestion caused severe performance degradation in 1980s
- Internet was experiencing "congestion collapse" - throughput dropped dramatically
- This paper introduced foundational algorithms that saved the Internet from collapse

## Slide 2: Conservation of Packets Principle
- Core idea: new packet enters network only when old packet leaves
- ACK (acknowledgment) signals that packet successfully traversed the network
- ACK acts as a "clock" controlling sending rate - one ACK, one new packet
- Self-clocking mechanism naturally adapts to network capacity
- Prevents overwhelming the network with excessive traffic

## Slide 3: Slow Start Algorithm
- Initial problem: how to establish the packet conservation "clock"?
- Slow start exponentially increases CWND (congestion window) at connection start
- Start with CWND = 1, double with each RTT (round-trip time)
- Exponential growth allows rapid discovery of available bandwidth
- Prevents initial burst that would cause immediate congestion

## Slide 4: Timeout and Congestion Detection
- Packet timeout indicates network congestion (packet stuck in queue)
- Timeout triggers congestion recovery mechanism
- Reset and restart slow start to re-establish proper sending rate
- Timeout is clear signal that network capacity was exceeded
- System must back off and probe capacity more conservatively

## Slide 5: Congestion Avoidance Phase
- After successful slow start, switch to congestion avoidance mode
- Linear increase instead of exponential: increment CWND by 1/CWND per ACK
- Additive increase per RTT cycle prevents aggressive growth
- Probes for additional capacity without causing congestion
- Maintains stable operation near network capacity limit

## Slide 6: Slow Start Threshold (ssthresh)
- ssthresh defines boundary between slow start and congestion avoidance
- After timeout, set ssthresh = CWND/2 (half of congestion point)
- Exponential growth (slow start) until reaching ssthresh
- Then switch to linear growth (congestion avoidance)
- Balances fast recovery with conservative probing

## Slide 7: Practical Implementation Results
- Testing showed dramatic throughput improvements
- Without algorithms: severe performance degradation under congestion
- With algorithms: stable, high utilization even under load
- Figure 8 comparison demonstrated effectiveness empirically
- Algorithms enabled Internet scalability in following decades

## Slide 8: Impact on Network Architecture
- These algorithms became fundamental to TCP/IP stack
- Implemented in all modern TCP implementations
- Enabled Internet to scale from thousands to billions of devices
- Foundation for subsequent congestion control innovations (TCP Reno, CUBIC, BBR)
- Demonstrated importance of end-to-end congestion control

## Slide 9: Key Technical Parameters
- CWND: congestion window controlling number of unacknowledged packets
- RTT: round-trip time used for timing calculations
- ssthresh: threshold switching between growth modes
- RTO: retransmission timeout calculated from RTT measurements
- Multiplicative decrease (factor of 2) for congestion response

## Slide 10: Long-term Significance
- Published 1988, still relevant today
- Solved "congestion collapse" problem threatening early Internet
- Established principles for distributed congestion control
- Influenced decades of networking research and development
- Example of elegant solution to complex distributed systems problem

## Slide 11: Question for You
Where does the compromise lie?
