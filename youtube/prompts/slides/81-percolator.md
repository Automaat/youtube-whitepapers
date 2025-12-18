Generate 11 presentation slides based on the podcast about Google's Percolator: Large-scale Incremental Processing Using Distributed Transactions.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Challenge of Incremental Web Indexing

- Google's web index needed continuous updates as new content appeared
- Batch processing with MapReduce required reprocessing entire datasets
- Fresh results were critical for search quality and user experience
- Need for incremental processing system at massive scale (billions of documents)

## Slide 2: Why MapReduce Wasn't Enough

- MapReduce excelled at batch processing but lacked incremental capabilities
- Rebuilding entire index from scratch was resource-intensive and slow
- No built-in support for transactions or consistency guarantees
- Gap between batch processing framework and real-time update requirements

## Slide 3: Percolator's Architecture Overview

- Built on top of BigTable for distributed storage layer
- Added transaction support with snapshot isolation
- Observer framework for incremental computation triggers
- Combined scalability of BigTable with ACID transaction guarantees

## Slide 4: Transaction Model and Snapshot Isolation

- Two-phase commit protocol for distributed transactions
- Snapshot isolation providing consistent read views
- Timestamps stored in BigTable for version management
- Lock columns for coordinating concurrent modifications

## Slide 5: The Observer Framework

- Observers trigger on data changes rather than scanning all data
- Notifications propagate through dependency chains
- Enables incremental computation across document collection
- Dramatically reduces processing overhead compared to batch recomputation

## Slide 6: Two-Phase Commit Implementation

- Pre-write phase: acquire locks and prepare changes
- Commit phase: write final values and release locks
- Primary lock mechanism coordinates distributed transaction
- Cleanup process handles failed transactions and orphaned locks

## Slide 7: Notification and Scanning Mechanism

- Workers scan for dirty cells requiring processing
- Notifications stored alongside data in BigTable
- Parallel scanning across multiple workers for throughput
- Already-processed regions skipped efficiently

## Slide 8: Performance Characteristics and Results

- Document processing throughput measured in documents per second
- Latency from document crawl to index availability
- Resource utilization compared to batch MapReduce approach
- Scalability demonstrated across Google's web corpus

## Slide 9: Real-World Impact at Google Scale

- Enabled continuous index updates for Google Search
- Fundamental trade-off: lower latency vs higher resource costs
- Proved incremental processing viable at massive scale
- Foundation for real-time data processing systems

## Slide 10: Legacy and Influence on Modern Systems

- Inspired transaction support in distributed databases
- Observer pattern adopted in stream processing frameworks
- Demonstrated combining transactions with scalable storage
- Influenced systems like Spanner, Cloud Bigtable, and other distributed databases

## Slide 11: Question for You

What part of the system could be further optimized?
