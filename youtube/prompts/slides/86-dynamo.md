Generate 11 presentation slides based on the podcast about Amazon Dynamo.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Amazon Dynamo

- Distributed key-value storage system powering Amazon's high-availability services
- Designed for always-on experience: shopping cart must always accept writes
- Built for extreme reliability and scalability at Amazon's scale
- Trade-offs: consistency vs availability - chose availability
- Real-world production system serving critical Amazon infrastructure

## Slide 2: Core Design Assumptions

- Simple key-value interface: get and put operations only
- Values are opaque binary objects (no complex queries needed)
- ACID properties relaxed in favor of availability
- No isolation guarantees - focus on eventual consistency
- Weak consistency model acceptable for target applications

## Slide 3: Consistent Hashing and Partitioning

- Data distributed across nodes using consistent hashing ring
- Each node responsible for range of keys on the ring
- Virtual nodes enable load balancing and heterogeneous hardware support
- Automatic data redistribution when nodes join or leave
- Minimizes data movement during cluster topology changes

## Slide 4: Replication Strategy

- N replicas for each data item (typically N=3)
- Coordinator node replicates to N-1 successor nodes on hash ring
- Preference list defines replication targets for each key
- Handles node failures transparently by skipping failed nodes
- Physical nodes, not virtual nodes, used for replica placement

## Slide 5: Sloppy Quorum and Hinted Handoff

- R + W > N ensures overlap for consistency (typical: R=2, W=2, N=3)
- Sloppy quorum: temporary replicas when primary nodes unavailable
- Hinted handoff returns data to original nodes when they recover
- Trades strict consistency for write availability
- Always-writable design: system never rejects writes

## Slide 6: Vector Clocks for Versioning

- Tracks causality and detects concurrent updates
- Each write includes vector clock showing version history
- Reading may return multiple conflicting versions
- Application responsible for conflict resolution (not the database)
- Enables detection of concurrent vs sequential updates

## Slide 7: Application-Level Conflict Resolution

- Conflicts pushed to application layer during reads
- Shopping cart example: merge concurrent adds, preserve all items
- Write operations include context from previous read
- Syntactic reconciliation (latest timestamp) vs semantic (business logic)
- Application has domain knowledge to resolve conflicts correctly

## Slide 8: Merkle Trees for Anti-Entropy

- Each node maintains Merkle tree per key range
- Periodic comparison of tree hashes between replicas
- Identifies divergent data efficiently without comparing all keys
- Minimizes data transfer during synchronization
- Background process ensures eventual consistency

## Slide 9: Failure Detection with Gossip Protocol

- Decentralized failure detection using gossip messages
- Nodes periodically exchange membership and liveness information
- No single point of failure for cluster membership
- Local knowledge eventually converges across cluster
- Temporary network partitions handled gracefully

## Slide 10: Tunable Consistency and Durability

- Per-operation tuning of R and W values
- Durable writes: W=N ensures all replicas written before acknowledgment
- Fast writes: W=1 with async replication for lower latency
- Business requirements drive consistency vs performance trade-off
- Same system supports different consistency needs per use case

## Slide 11: Question for You

What other areas of software engineering could benefit from consciously shifting responsibility to the application layer to unlock new capabilities?
