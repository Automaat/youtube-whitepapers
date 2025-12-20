Generate 11 presentation slides based on the podcast about Amazon Aurora.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Aurora - Cloud-Native Database Architecture

- Separation of storage and compute layers in MySQL architecture
- Traditional MySQL uses local storage with synchronous replication
- Aurora moves storage to distributed service layer
- Reduces write amplification from page-level replication
- Designed specifically for AWS cloud infrastructure

## Slide 2: Traditional MySQL Limitations

- Coupled storage and compute creates scaling bottlenecks
- Write amplification: single change triggers multiple operations
- Binary log, double-write buffer, and redo log overhead
- Each replica maintains full copy of data
- High network traffic during replication and failover

## Slide 3: Log-Structured Storage with LSN

- Only redo log records cross the network (not entire pages)
- Log Sequence Number (LSN) tracks write ordering
- Storage nodes reconstruct pages from log segments
- Eliminates binary log and double-write buffer
- 4/6 quorum write model for durability

## Slide 4: Service-Oriented Architecture

- Storage as independent distributed service
- Compute layer only sends log records to storage
- Storage nodes handle page materialization asynchronously
- Decouples database engine from storage management
- Enables independent scaling of compute and storage

## Slide 5: Protection Groups and Quorum Writes

- Data replicated across 3 Availability Zones
- 6 copies total: 2 copies per AZ
- Write quorum: 4 out of 6 copies acknowledge
- Read quorum: 3 out of 6 copies respond
- Protection Group spans 10 GB segment across 6 nodes

## Slide 6: Cross-Region Replication Architecture

- Read replicas can span multiple AWS regions
- Asynchronous log shipping to remote regions
- Low lag replication (<1 second typical)
- Enables global read scaling and disaster recovery
- VDL (Virtual Database Log) coordinates replay

## Slide 7: Fast Crash Recovery

- Traditional MySQL recovery scans entire redo log
- Aurora parallelizes recovery across storage nodes
- Storage nodes independently replay log segments
- Recovery time independent of database size
- Continuous background log application reduces downtime

## Slide 8: Write Performance at Scale

- Significantly reduced network traffic (only redo logs)
- Write throughput improves with storage scaling
- Eliminates page shipping to replicas
- Asynchronous storage operations reduce latency
- 35x less network I/O compared to MySQL

## Slide 9: Performance Results

- Sustained 100,000+ writes per second on r3.8xlarge
- 5x throughput improvement over MySQL with same hardware
- Sub-second failover times with minimal data loss
- Storage auto-scales to 64 TB without downtime
- Consistent performance regardless of database size

## Slide 10: Lessons Learned from Production

- Correlated failures require careful quorum design
- LSN-based recovery simpler than page-based approaches
- Separation of concerns improves operational flexibility
- Cloud-native design enables features impossible with traditional architecture
- Cost optimization through reduced replication overhead

## Slide 11: Question for You

Will we see a similar revolution in other database systems?
