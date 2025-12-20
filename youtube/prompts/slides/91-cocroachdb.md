Generate 11 presentation slides based on the podcast about CockroachDB.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to CockroachDB

- Distributed SQL database designed for global scalability
- Built to provide ACID guarantees across geographically distributed data
- Combines consistency of traditional SQL with scale of NoSQL systems
- Inspired by Google Spanner architecture

## Slide 2: Layered Architecture

- Comparison to traditional databases: storage and SQL layers separated
- Transaction layer handles distributed coordination
- Distribution layer manages data replication across nodes
- Storage layer persists data locally on each node
- Clean separation enables horizontal scaling

## Slide 3: Replication and Leaseholder Model

- Data divided into ranges, each replicated three times
- One replica in each group acts as leaseholder
- Leaseholder coordinates reads and writes for its range
- Ensures consistency while distributing load
- Automatic failover when leaseholder becomes unavailable

## Slide 4: Transaction Layer and Distributed Coordination

- Core system handles distributed transactions across ranges
- Coordinates with leaseholders to ensure ACID properties
- Uses two-phase commit protocol for multi-range transactions
- Manages transaction isolation and conflict resolution
- Provides serializable isolation level by default

## Slide 5: Hybrid Logical Clock (HLC)

- Combines physical time with logical counters
- Enables causality tracking without perfect clock synchronization
- Carries temporal information for ordering distributed events
- Allows efficient timestamp-based concurrency control
- Critical for distributed transaction correctness

## Slide 6: Write Path and Consensus

- Write operations first wait for acknowledgment from majority
- Uses Raft consensus protocol for replication
- Ensures durability before returning success to client
- Coordinated through leaseholder for each range
- Provides strong consistency guarantees

## Slide 7: Geo-Partitioning and Data Locality

- Intelligent feature for distributing data by geography
- Supports compliance requirements like GDPR
- Example: EU users' data stays in EU, US data in USA, Australia data in Australia
- Reduces latency by keeping data close to users
- Maintains global consistency while respecting data sovereignty

## Slide 8: Performance Trade-offs

- Results clearly demonstrate inherent compromises
- Strong consistency comes with coordination overhead
- Distributed transactions slower than single-node operations
- Network latency impacts cross-region operations
- Trade-off between consistency, availability, and performance

## Slide 9: Read-After-Validated-Time (RAVT) Optimization

- Attempted performance optimization for read operations
- Performance gain turned out to be minimal
- Team decided removing it would improve system maintainability
- Demonstrates pragmatic engineering: simplicity over marginal gains
- Shows importance of measuring actual impact of optimizations

## Slide 10: Challenges and Lessons Learned

- Became source of numerous production issues over time
- Complexity of distributed systems requires careful design choices
- Sometimes simpler solutions are more robust long-term
- PostgreSQL compatibility improves developer experience
- Application logic must handle transaction retries correctly

## Slide 11: Question for You

Is the issue in the application logic that cannot handle transaction retries?
