Generate 11 presentation slides based on the podcast about ZooKeeper: Wait-free coordination for Internet-scale systems.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: ZooKeeper Overview & Design Goals

- ZooKeeper is a coordination service for distributed systems providing wait-free data objects called znodes
- Designed for high-throughput, read-dominant workloads at Internet scale
- Provides simple API: create, delete, exists, getData, setData, getChildren with watch notifications
- Guarantees FIFO client order and linearizable writes across all operations
- No blocking primitives - coordination built using wait-free shared objects

## Slide 2: Wait-Free Coordination Model

- Traditional coordination uses blocking primitives (locks, barriers) which hurt performance
- ZooKeeper provides wait-free objects allowing clients to implement coordination without waiting
- Clients never block on ZooKeeper operations - always make progress
- Single client can pipeline multiple requests for maximum throughput
- Watches enable event-driven coordination without polling

## Slide 3: ZNode Hierarchy & Watch Mechanism

- ZNodes organized in hierarchical namespace like filesystem (e.g., /app/config)
- Two types: regular znodes and ephemeral znodes (deleted when session ends)
- Clients set watches on znodes to receive notifications on changes
- Watch triggers once, then must be reset - prevents unnecessary notifications
- Enables efficient publish-subscribe patterns for configuration and membership

## Slide 4: Session Guarantees & Client Properties

- Sessions maintain FIFO ordering - client sees own writes in order
- Session timeout mechanism detects client failures via heartbeats
- Client library handles session reconnection and watch re-establishment
- Zxid (ZooKeeper transaction id) ensures monotonic consistency across servers
- Client reads may see stale data but never go backwards in time

## Slide 5: Read/Write Performance Characteristics

- Reads served locally from any replica without coordination - highly scalable
- Writes go through leader using atomic broadcast (Zab protocol)
- Read throughput scales linearly with number of servers
- Write throughput limited by leader but still handles thousands of ops/sec
- System optimized for read-heavy workloads (typical ratio: 10:1 reads to writes)

## Slide 6: Implementing Coordination Primitives

- Configuration management: clients watch config znode, receive updates on change
- Group membership: ephemeral sequential znodes show live members
- Distributed locks: create ephemeral znodes, watch predecessor for lock acquisition
- Leader election: lowest sequential znode becomes leader, others watch predecessor
- Barriers: wait for all participants to create znodes before proceeding

## Slide 7: Zab: ZooKeeper Atomic Broadcast

- Zab ensures atomic delivery and total ordering of write operations
- Leader-based protocol with two phases: leader election and atomic broadcast
- All writes forwarded to leader, then broadcast to followers
- Majority quorum required for commit - tolerates f failures with 2f+1 servers
- Crash recovery rebuilds state from transaction logs and snapshots

## Slide 8: Linearizable Writes vs Eventual Consistency Reads

- Writes are linearizable - appear atomically to all clients in global order
- Reads are not linearizable - may return stale data from replica
- Sync operation available to force read consistency (flushes pending writes)
- Trade-off enables high read performance while maintaining write correctness
- Most coordination patterns work correctly with this consistency model

## Slide 9: Real-World ZooKeeper Usage

- Used in production at Yahoo for Katta (search), Fetching Service (crawl coordinator)
- Replaced custom coordination code with 200-300 lines of ZooKeeper client code
- Handles thousands of concurrent clients and millions of znodes
- Typical deployment: 3-5 server ensemble for fault tolerance
- Proven stable at Internet scale with minimal operational overhead

## Slide 10: Performance & Scalability Results

- Benchmark: 3.4K-13K writes/sec, 21K-94K reads/sec on 7-node cluster
- Read throughput scales linearly: 2x servers = 2x read capacity
- Write latency: ~1-2ms for small writes, reads under 1ms when served locally
- Handles client churn (session timeouts) efficiently with batched session management
- System optimized for read-dominated workloads common in coordination scenarios

## Slide 11: Question for You

Are you optimizing your distributed system for reads over writes, and could wait-free coordination improve your architecture?
