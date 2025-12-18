Generate 11 presentation slides based on the podcast about MapReduce: Simplified Data Processing on Large Clusters.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to MapReduce

- Google's 2004 paper introducing programming model for processing massive datasets
- Designed to handle terabytes of data across thousands of machines daily
- Simplifies distributed computing by abstracting parallelization and fault tolerance
- Inspired by functional programming concepts: map and reduce operations
- Revolutionary impact on big data processing and distributed systems

## Slide 2: The Core Problem

- Google processing 20+ terabytes of data daily in early 2000s
- Traditional approaches required complex distributed systems code for each task
- Engineers spent more time on infrastructure than business logic
- Needed consistent handling of: machine failures, data distribution, load balancing
- Every new data processing task reimplemented same distributed computing patterns

## Slide 3: Map Phase Explained

- Map function processes input key/value pairs to generate intermediate results
- Example: word count - each document mapped to (word, 1) pairs
- Workers process chunks of data in parallel across cluster
- Master node coordinates task assignment to available workers
- Output written to local disk partitioned by reduce task (e.g., by city, region)

## Slide 4: Reduce Phase Explained

- Reduce function aggregates all values for each intermediate key
- Example: word count - reduce sums all counts for each word
- Master assigns reduce tasks based on intermediate data locality
- Workers read partitioned data from map workers' local disks
- Final output written to distributed file system (GFS)

## Slide 5: Fault Tolerance

- Master pings workers periodically to detect failures
- Failed map tasks restarted on different machines (data on local disk lost)
- Failed reduce tasks only rerun if output not yet written to GFS
- Completed tasks don't need reruns (output already in distributed storage)
- System handles machine failures transparently without user intervention

## Slide 6: Data Locality Optimization

- Master schedules map tasks on machines already storing input data
- Reduces network bandwidth usage by processing data where it lives
- If local execution impossible, schedule on nearby machine (same rack)
- Critical for performance at Google's scale (terabytes over limited bandwidth)
- GFS replication (3 copies) increases chances of local scheduling

## Slide 7: Execution Workflow

- User program splits input into M map tasks and R reduce tasks
- Master tracks task states: idle, in-progress, completed
- Map workers produce R intermediate partitions locally
- Reduce workers notified of partition locations after map completion
- Output files written to GFS, typically used as input for another MapReduce job

## Slide 8: Real-World Applications at Google

- Distributed grep: searching patterns across massive log datasets
- URL access frequency counting for web analytics
- Reverse web-link graph: building graph of pages linking to each URL
- Document clustering and machine learning feature extraction
- All running on commodity hardware clusters (thousands of machines)

## Slide 9: Performance Characteristics

- Sorting 1TB benchmark: processes data faster than disk-to-disk copy
- Scalability: 1800 machines processing terabytes in minutes
- Bandwidth efficiency: data locality reduces network to <10% bottleneck
- Fault recovery: backup tasks for stragglers improve tail latency by 44%
- Linear scaling with cluster size for most workloads

## Slide 10: Impact and Legacy

- Changed how engineers think about large-scale data processing
- Spawned entire ecosystem: Hadoop, Spark, cloud computing platforms
- Demonstrated power of simple abstractions for complex distributed systems
- Enabled data-driven decision making at unprecedented scale
- Proof that "less is more" in distributed systems design

## Slide 11: Question for You

Does simplicity in systems design - and perhaps in life - truly mean that less is more?
