Generate 11 presentation slides based on the podcast about HDFS (Hadoop Distributed File System).

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to HDFS

- Hadoop Distributed File System designed for Big Data storage
- Built to handle massive datasets across commodity hardware clusters
- Developed as part of Apache Hadoop ecosystem
- Optimized for throughput over latency
- Addresses challenges of storing petabyte-scale data

## Slide 2: Architecture Overview

- Master-slave architecture with centralized coordination
- NameNode acts as master metadata server
- DataNodes store actual data blocks across cluster
- Single namespace managed by NameNode
- Designed for write-once, read-many workloads

## Slide 3: Block-Based Storage Model

- Files split into fixed-size blocks (typically 64MB or 128MB)
- Large blocks reduce metadata overhead
- Blocks distributed across multiple DataNodes
- Each block treated as independent file on DataNode
- Block size optimized for sequential access patterns

## Slide 4: Replication Strategy

- Default replication factor: 3 copies per block
- First replica placed on client's node (if possible)
- Second replica on different rack for fault tolerance
- Third replica on same rack as second
- Rack-aware placement balances reliability and network cost
- Configurable replication factor per file or directory

## Slide 5: Read Operations

- Client requests file metadata from NameNode
- NameNode returns list of DataNodes holding blocks
- Client reads directly from DataNodes (no NameNode bottleneck)
- Proximity-based DataNode selection minimizes network traffic
- Checksum verification ensures data integrity
- Direct client-to-DataNode communication maximizes throughput

## Slide 6: Write Operations

- Client requests block allocation from NameNode
- NameNode selects target DataNodes based on rack policy
- Client creates write pipeline through DataNodes
- Data flows through pipeline with acknowledgments
- NameNode metadata updated after successful write
- Pipeline approach reduces NameNode load during writes

## Slide 7: NameNode: The Metadata Server

- Stores entire filesystem namespace in RAM
- File tree structure, permissions, block locations
- Transaction log (EditLog) for durability
- FSImage snapshot for recovery
- Single point of coordination (and potential failure)
- RAM capacity limits filesystem scale

## Slide 8: Failure Handling

- DataNode heartbeats detect failures
- Automatic re-replication when blocks under-replicated
- Rack failure handled through cross-rack replication
- Checksum verification detects corrupt blocks
- NameNode failure requires manual recovery
- Secondary NameNode creates periodic checkpoints (not hot standby)

## Slide 9: Design Trade-offs

- Optimized for large files and sequential access
- Not suitable for low-latency random reads
- Write-once model simplifies consistency
- Large block sizes reduce small file efficiency
- Centralized NameNode limits horizontal scaling
- High throughput prioritized over POSIX compliance

## Slide 10: Evolution and Impact

- Foundation for Hadoop ecosystem growth
- Influenced cloud object storage designs (S3, GCS)
- Later versions added NameNode HA and federation
- Demonstrated viability of commodity hardware clusters
- Enabled cost-effective petabyte-scale storage
- Key enabler for Big Data analytics revolution

## Slide 11: Question for You

How would you modify HDFS architecture to support real-time low-latency workloads while preserving its high-throughput characteristics?
