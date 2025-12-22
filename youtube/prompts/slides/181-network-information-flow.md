Generate 11 presentation slides based on the podcast about Network Information Flow.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Network Information Flow
- Network coding fundamentally changes how we think about routing in networks
- Traditional routing treats network nodes as passive forwarders of packets
- Network Information Flow paper introduces active processing at intermediate nodes
- Key insight: nodes can combine and transform information, not just forward it
- Published in 2000, revolutionizing multicasting and network throughput optimization
- Challenges the assumption that capacity is limited by MaxFlow-MinCut theorem

## Slide 2: The Core Problem
- Traditional multicasting sends separate copies of data to each destination
- Network capacity appears limited when treating nodes as simple routers
- Classic MaxFlow-MinCut theorem suggests theoretical limits for routing
- The butterfly network topology demonstrates the fundamental limitation
- Question: can we achieve better throughput if nodes process information?
- Network coding emerges as the solution to break through routing bottlenecks

## Slide 3: Network Coding Concept
- Network nodes receive different bits from multiple sources
- Instead of forwarding, nodes perform XOR operations on received bits
- Combined information is transmitted as a single packet
- Receivers can decode original data using linear algebra operations
- XOR is reversible: if you have A⊕B and A, you can recover B
- Simple bitwise operations enable dramatic throughput improvements

## Slide 4: The Butterfly Network Example
- Classic topology demonstrating network coding advantages
- Single source multicasting to two destinations through bottleneck link
- Traditional routing requires 3 transmissions, achieves 1.5 bits per transmission
- Network coding with XOR at intermediate node requires only 2 transmissions
- Achieves 2 bits per transmission - 33% throughput improvement
- Demonstrates that routing is suboptimal for multicast scenarios

## Slide 5: Breakthrough Discovery
- Network coding shows routing is not optimal for multicasting
- MaxFlow-MinCut theorem still holds, but for information flow, not packet routing
- Discovery comparable to finding that the speed of light can be approached differently
- Fundamentally changes network design philosophy
- Opens new research directions in wireless networks, P2P systems, and distributed storage
- Theoretical computer science meets practical networking optimization

## Slide 6: Main Theorem
- For single-source multicast, linear network coding achieves maximal capacity
- Capacity equals the minimum of all MaxFlow values from source to each destination
- Theorem proves existence of coding solution achieving this capacity
- No need for complex non-linear coding operations
- Simple XOR operations are sufficient for optimal throughput
- Theorem provides constructive proof with polynomial-time algorithms

## Slide 7: From Difficult to Tractable
- Before network coding, multicast capacity problem was considered computationally hard
- Routing-based approaches led to NP-complete optimization problems
- Network coding transforms the problem into tractable linear algebra
- Key insight: think in terms of information flows, not packet paths
- Allows efficient algorithms for finding optimal coding schemes
- Computational complexity drops dramatically with coding perspective

## Slide 8: Acyclic Graph Simplification
- Instead of analyzing complex graphs with cycles, create acyclic time-expanded graphs
- Each time step creates a new layer of nodes in the expanded graph
- Cycles in original topology become paths in time-expanded representation
- Linear algebraic methods can be applied to acyclic structures
- Enables polynomial-time algorithms for finding coding solutions
- Transforms hard graph problems into manageable linear systems

## Slide 9: Multiple Sources Extension
- Original theorem focuses on single-source multicast scenarios
- Multiple sources scenario is significantly more complex
- Determining achievable rate regions becomes harder problem
- No simple characterization like MaxFlow-MinCut for multi-source case
- Still an active research area with open questions
- Practical applications often use heuristics and approximations

## Slide 10: Practical Impact
- Network coding changes how we think about network nodes
- Nodes become active processors of information, not just packet forwarders
- Applications in wireless mesh networks, satellite communications, and content distribution
- Random linear network coding enables practical distributed implementations
- Trade-offs between coding complexity and throughput gains
- Implementation challenges include computational overhead and synchronization

## Slide 11: Question for You
What are the practical implementation challenges and computational complexity trade-offs when deploying network coding in real-world systems?
