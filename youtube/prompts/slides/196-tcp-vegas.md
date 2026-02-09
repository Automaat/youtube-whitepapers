Generate 11 presentation slides based on the podcast about TCP Vegas congestion control algorithm.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to TCP Vegas
- New congestion avoidance mechanism designed to prevent packet loss before it occurs
- Created as alternative to reactive TCP Reno approach
- Focuses on proactive bandwidth detection rather than waiting for packet drops
- Aims to maintain optimal throughput while avoiding network congestion
- Represents shift from loss-based to delay-based congestion control

## Slide 2: The Problem with TCP Reno
- Reno uses packet loss as primary congestion signal
- Continuously increases sending rate until packets are dropped
- Half a second delay in high-speed networks is extremely wasteful
- Creates "sawtooth" pattern of bandwidth utilization
- Reactive approach leads to inevitable congestion and recovery cycles
- Inefficient use of available bandwidth

## Slide 3: TCP Vegas Core Innovation - RTT Monitoring
- Measures Round Trip Time (RTT) continuously during transmission
- Compares actual RTT against minimum observed RTT (BaseRTT)
- Uses RTT difference to detect queue buildup in network
- Calculates expected throughput vs actual throughput
- Proactive detection before packet loss occurs
- Maintains window size that keeps network optimally utilized

## Slide 4: The Vegas Algorithm - Alpha and Beta Thresholds
- Two key parameters: Alpha (lower threshold) and Beta (upper threshold)
- Diff = Expected throughput - Actual throughput
- If Diff < Alpha: increase congestion window (network underutilized)
- If Diff > Beta: decrease congestion window (queues building up)
- If Alpha ≤ Diff ≤ Beta: maintain current window size (optimal zone)
- Fine-grained control compared to Reno's aggressive adjustments

## Slide 5: Expected vs Actual Throughput Calculation
- Expected = WindowSize / BaseRTT (ideal throughput)
- Actual = WindowSize / CurrentRTT (observed throughput)
- Growing difference indicates packets queuing in network buffers
- Vegas detects congestion before buffers overflow and drop packets
- Allows preemptive window adjustment
- More stable and predictable bandwidth utilization

## Slide 6: Vegas Congestion Detection Strategy
- Monitors packets in flight vs packets at destination
- Detects when packets are stuck in network queues
- RTT increase signals buffer buildup along path
- Responds by reducing transmission rate gradually
- Prevents the "cliff edge" behavior of loss-based algorithms
- Maintains higher average throughput with lower variance

## Slide 7: Performance Comparison - Vegas vs Reno
- Vegas achieves 40-70% better throughput in many scenarios
- Significantly reduced packet retransmissions (37-71% fewer)
- More stable bandwidth utilization without sawtooth oscillations
- Lower latency for competing traffic sharing same links
- Particularly effective in high bandwidth-delay product networks
- Better fairness when competing with other Vegas flows

## Slide 8: Real-World Testing and Validation
- Tested extensively in laboratory and production networks
- Demonstrated consistent improvements across various network conditions
- Paper presents hard evidence of effectiveness through measurements
- Network providers showed interest in deployment
- Implementation complexity higher than Reno but manageable
- Required careful tuning of Alpha and Beta parameters

## Slide 9: Challenges and Limitations
- Fairness issues when competing with aggressive Reno flows
- Vegas backs off while Reno continues to increase, leading to starvation
- Difficult to achieve widespread adoption due to compatibility
- Requires accurate RTT measurements and stable baseline
- Route changes can invalidate BaseRTT assumptions
- Best results achieved when all flows use Vegas

## Slide 10: Legacy and Impact on Congestion Control
- Pioneered delay-based congestion control paradigm
- Influenced later algorithms like FAST TCP, BBR, and others
- Demonstrated that proactive control outperforms reactive approaches
- Showed importance of measuring network state continuously
- Highlighted deployment challenges of incompatible improvements
- Remains foundational work in network congestion control research

## Slide 11: Question for You
How can a superior congestion control algorithm achieve global adoption in a decentralized system without a single governing authority?
