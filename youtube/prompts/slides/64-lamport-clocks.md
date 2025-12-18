Generate 11 presentation slides based on the podcast about "Time, Clocks, and the Ordering of Events in a Distributed System" by Leslie Lamport (1978).

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Problem - No Universal "Now"

- Airplane reservation scenario: Frankfurt vs New York clicking simultaneously
- Traditional notion of time fails in distributed systems
- No single universal clock across global networks
- Communication delays make "simultaneous" meaningless
- Fundamental challenge: determining event ordering across distributed nodes
- Network latency prevents instant information propagation

## Slide 2: Causality Over Clock Time

- Lamport's key insight: focus on cause-and-effect, not wall-clock time
- "Happened-before" relation (→) defines partial ordering
- Three fundamental rules for happened-before:
  - Events on same computer maintain sequential order
  - Message send always happens before message receive
  - Transitivity: if A → B and B → C, then A → C
- Only events with causal connection can be ordered

## Slide 3: Concurrent Events

- Concurrent events: no causal relationship between them
- System cannot determine which occurred first
- Represented as "cousins" in event genealogy tree
- Example: Frankfurt and New York reservations are concurrent
- Neither event is cause or effect of the other
- System must handle this ambiguity explicitly

## Slide 4: Logical Clocks - Simple Counters

- Each computer maintains its own logical clock (simple counter)
- Starts at zero, increments upward
- Purpose: assign numbers to events, not measure seconds
- Clock Condition: if A → B, then C(A) < C(B)
- Numbers reflect causality, not physical time
- Foundation for distributed event ordering

## Slide 5: Two Clock Update Rules

- Rule 1 (local events): increment counter before each internal event
- Rule 2 (message passing): sender includes timestamp with message
- Receiver updates: max(local_clock, message_timestamp) + 1
- Messages carry information about sender's causal history
- Ensures clock condition is maintained across network
- Simple algorithm, powerful guarantees

## Slide 6: Total Ordering - Breaking Ties

- Partial ordering insufficient for resource allocation decisions
- Need single, consistent ordering across all events
- Solution: combine timestamp with process ID
- Tie-breaking rule: if timestamps equal, lower process ID wins
- Creates total ordering visible to all processes
- Arbitrary but deterministic resolution of concurrent events

## Slide 7: Mutual Exclusion Algorithm

- Fully decentralized resource access control
- Each process sends timestamped request to all others
- Process waits for acknowledgments from all peers
- Grants itself access when it has earliest timestamp
- All processes make identical decisions independently
- No central coordinator needed

## Slide 8: The Anomaly Problem

- User A calls user B about completing action X
- System may show X happening after phone call
- Logical clocks cannot prevent external-world inconsistencies
- External events (phone calls) invisible to distributed system
- Violates human perception of causality
- Requires anchoring to physical reality

## Slide 9: Physical Clock Synchronization

- Logical clocks must be bounded relative to physical time
- Two synchronization conditions:
  - Bounded drift: clocks tick at similar rates
  - Bounded skew: maximum difference between any two clocks
- Synchronization window (ε) defines acceptable divergence
- Periodic synchronization messages maintain bounds
- Network delay must be smaller than ε
- Balances logical consistency with physical time

## Slide 10: Real-World Impact

- Published 1978, foundation of modern distributed systems
- Powers: distributed databases, cloud computing, blockchain
- Google, Amazon, Facebook built on these principles
- Consensus mechanisms derive from Lamport's work
- Vector clocks extend the basic concept
- Continues to influence system design 45+ years later

## Slide 11: Question for You

Lamport clearly distinguished between events inside the system and external events (like phone calls). Today, this boundary is increasingly blurred. Our systems constantly interact with humans, billions of IoT devices, and hundreds of other systems. Where does "the system" end in such a world? How must Lamport's ideas evolve when external and internal causality intertwine in ways nobody in 1978 could imagine?
