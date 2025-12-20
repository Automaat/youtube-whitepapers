Generate 11 presentation slides based on the podcast about Cassandra: A Decentralized Structured Storage System.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Facebook Inbox Search Challenge

- Facebook needed to search messages across 100+ million users in real-time
- Traditional databases couldn't scale to handle exponential user growth
- Required distributed system with high write throughput and availability
- Solution: Cassandra - combining Dynamo's availability with Bigtable's data model
- System had to operate across multiple data centers globally

## Slide 2: Why Existing Solutions Failed

- Bigtable: centralized master node created single point of failure
- Dynamo: key-value model too simple for complex search queries
- Traditional RDBMS: couldn't handle write-heavy workload at Facebook's scale
- HBase: similar centralization problems to Bigtable
- Need: decentralized, always-available system with structured data support

## Slide 3: Cassandra Data Model - Structured Key-Value

- Column families group related data (like tables in SQL)
- Super columns allow nested structures within column families
- Flexible schema: columns can be added dynamically per row
- Column names can encode metadata (timestamps, categories)
- Supports both simple and complex query patterns

## Slide 4: Ring Architecture - Consistent Hashing

- Nodes arranged in ring topology using consistent hashing
- Each node responsible for range of hash values
- No master node - fully decentralized coordination
- Adding/removing nodes only affects immediate neighbors
- Virtual nodes distribute load evenly across physical machines

## Slide 5: Replication Strategy

- Configurable replication factor (N copies of data)
- First replica at hash owner, next N-1 at clockwise neighbors
- Rack-aware and datacenter-aware replication options
- Prevents data loss from hardware failures or datacenter outages
- Read and write operations can specify consistency requirements

## Slide 6: Tunable Consistency

- Quorum-based consistency: R + W > N guarantees latest data
- Applications choose tradeoff between latency and consistency
- ANY: fastest write, lowest durability (coordinator caches write)
- ONE: single node confirms, very fast
- QUORUM: majority confirms, balanced approach
- ALL: all replicas confirm, strongest consistency but highest latency

## Slide 7: Write Path - MemTable and SSTables

- Writes first logged to commit log for durability
- Then written to in-memory MemTable structure
- When MemTable full, flushed to disk as immutable SSTable
- Multiple SSTables compacted periodically to reduce read amplification
- Bloom filters speed up queries by avoiding unnecessary disk reads

## Slide 8: Read Path and Compaction

- Reads check MemTable first, then SSTables from newest to oldest
- Bloom filters quickly eliminate SSTables that don't contain key
- Read repair reconciles inconsistencies across replicas
- Compaction merges multiple SSTables, removing deleted/outdated data
- Background anti-entropy ensures replicas converge over time

## Slide 9: Facebook Inbox Search Performance

- Handles 50+ writes per second per user during peak hours
- Search across entire message history completes in under 100ms
- System scales linearly by adding more nodes to ring
- Zero downtime during node failures or maintenance
- Processes billions of operations daily across global infrastructure

## Slide 10: Lessons and Trade-offs

- Eventual consistency model requires application-level awareness
- No joins or complex queries - denormalization necessary
- Storage overhead from replication and compaction
- Operations complexity: monitoring, tuning compaction, managing repairs
- Success inspired ecosystem of Cassandra-based systems (DataStax, ScyllaDB)

## Slide 11: Question for You

Which fundamental assumption in database design should we start questioning anew?
