Generate 11 presentation slides based on the podcast about Google Spanner.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Google Spanner

- Google's globally distributed database system combining RDBMS with NoSQL scalability
- First system to provide externally consistent distributed transactions at global scale
- Built to replace MySQL and Bigtable for applications requiring both SQL and horizontal scaling
- Novel approach using synchronized atomic clocks (TrueTime API) for distributed consensus

## Slide 2: The Fundamental Challenge

- Traditional distributed databases: choose between strong consistency OR global scale
- CAP theorem constraints: consistency vs availability in network partitions
- MySQL: strong consistency but limited horizontal scaling
- Bigtable: massive scale but eventually consistent, no multi-row transactions
- Spanner's goal: break this trade-off with external consistency at global scale

## Slide 3: TrueTime API Architecture

- Exposes clock uncertainty as first-class API primitive (epsilon value)
- Returns time interval [earliest, latest] instead of single timestamp
- TT.now() provides current time with bounded uncertainty
- TT.after(t) and TT.before(t) for temporal comparisons
- Uncertainty typically 1-7 milliseconds across Google's network

## Slide 4: Atomic Clocks and GPS Synchronization

- Each datacenter equipped with atomic clocks and GPS receivers
- Multiple time masters per datacenter for redundancy
- Continuous synchronization protocol reduces clock drift
- Hardware-level investment in time accuracy infrastructure
- Bounded uncertainty guarantee critical for correctness proofs

## Slide 5: Globally Synchronized Transactions

- Two-phase commit protocol extended with TrueTime-based waiting
- Commit wait: delay until TT.now().earliest > commit timestamp
- Ensures external consistency: if T1 completes before T2 starts, T1's timestamp < T2's timestamp
- Transactions across multiple datacenters maintain strict serializability
- Paxos groups manage replicated state within regions

## Slide 6: Read-Write Transaction Protocol

- Acquire locks on all modified data across participating Paxos groups
- Choose commit timestamp s = TT.now().latest
- Wait until TT.now().earliest > s (commit wait period)
- Release locks only after commit wait completes
- Guarantees: all replicas see consistent ordering regardless of geographical location

## Slide 7: Lock-Free Read-Only Transactions

- No locks required for read-only transactions
- Read at timestamp = TT.now().latest
- Safe snapshots guaranteed by commit wait in read-write transactions
- Dramatically reduces latency for analytical queries
- Critical feature for global applications requiring low-latency reads

## Slide 8: Performance Characteristics

- Commit wait adds 5-10ms latency to write transactions (epsilon-dependent)
- Read-only transactions: no additional latency from distributed consensus
- Transparent trade-off: bounded additional write latency for lock-free reads
- Latency scales with geographical distribution of transaction participants
- Real-world production performance validated across Google's infrastructure

## Slide 9: Automatic Resharding and Migration

- Dynamic data migration between Paxos groups without downtime
- Automatic resharding based on load and data growth
- Directory-level migration granularity
- No human intervention required for rebalancing
- Maintains consistency guarantees during resharding operations

## Slide 10: Comparison with Contemporary Systems

- MySQL: strong consistency, limited scale, manual sharding required
- Bigtable: massive scale, eventual consistency, no cross-row transactions
- Megastore: ACID transactions but significantly higher latencies
- Spanner: combines SQL semantics with NoSQL scale and global consistency
- Unique position in consistency-availability-latency trade-off space

## Slide 11: Question for You

What happens when clock uncertainty in a global network approaches zero?
