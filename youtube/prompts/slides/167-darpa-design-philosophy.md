Generate 11 presentation slides based on the podcast about David Clark's "The Design Philosophy of the DARPA Internet Protocols" (1988).

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: DARPA's Original Mission
- Goal: connect existing heterogeneous networks (ARPANET, radio, satellite)
- Not a unified network - internetworking architecture
- Document from 1988 with 2013 critical commentary by author
- Foundation for understanding why Internet works the way it does

## Slide 2: Design Priority Hierarchy
- First priority: survivability during network failures
- Communication must work at any cost (military roots)
- Lower priorities: variety of services, resource management, cost accounting
- Security not on the list - small trusted community in 1988
- Clark's 2013 update: security should be priority #1 today

## Slide 3: Survivability Through Fault Tolerance
- TCP connection must survive intermediate network failures
- If two machines communicate and router fails mid-connection
- Communication continues with minimal disruption
- More ambitious than simple redundancy
- Requires fundamental architectural decisions

## Slide 4: Fate Sharing Principle
- Core innovation: connection state stored only in end hosts
- Routers are stateless - no connection tracking
- Router failure: packets reroute, lost packets retransmitted
- End host failure: connection lost anyway (state shares fate)
- Trade-off: eliminates single point of failure, harder to implement features

## Slide 5: The Datagram as Universal Building Block
- IP datagram: simple best-effort packet delivery
- No guarantees: delivery, order, or integrity
- Minimal common denominator for heterogeneous networks
- Routers only forward packets without state
- Foundation for network flexibility and longevity

## Slide 6: Transport Layer Diversity
- Single monolithic protocol insufficient for all needs
- TCP: reliable, ordered delivery (file transfers, web)
- UDP: fast, low-latency delivery (voice, video, debugging)
- Example: Xnet debugging tool needs packets during failures
- Example: Voice calls prefer low jitter over 100% reliability

## Slide 7: TCP vs UDP Trade-offs
- TCP retransmissions cause variable latency (jitter)
- UDP accepts packet loss for stable timing
- Brief silence better than multi-second pause in voice calls
- Separation: IP handles routing, transport layer handles reliability
- Architecture enables future protocols without IP changes

## Slide 8: End-to-End Argument
- Functions belong at end hosts unless performance requires otherwise
- Application-level checksums more reliable than network-level
- Examples: encryption, compression, error correction
- Enables innovation without network modifications
- Network remains simple and transparent

## Slide 9: Practical Implementation - TTL and Traceroute
- Time To Live (TTL): prevents infinite routing loops
- Each router decrements TTL, drops packet at zero
- Traceroute exploit: sends packets with increasing TTL values
- First packet TTL=1, second TTL=2, maps entire route
- Using failure mechanism for diagnostics - works but inelegant

## Slide 10: Design Consequences and Legacy
- Architecture enabled Internet to run on unforeseen technologies
- From twisted pair to fiber optic to 5G
- Price: problems we face today (security, accounting, QoS)
- Clark's 1988 suggestion: next generation might not use datagrams
- Fundamental tension: simple resilient core vs intelligent awareness

## Slide 11: Question for You
After more than 30 years, are we still trapped in the same fundamental tension between the simplicity and resilience of the network core and the intelligence and awareness we increasingly demand from it?
