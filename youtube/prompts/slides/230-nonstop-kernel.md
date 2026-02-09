Generate 11 presentation slides based on the podcast about NonStop Kernel.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to NonStop Systems
- Tandem Computers pioneered fault-tolerant computing in 1976
- NonStop kernel architecture designed for zero downtime operations
- Critical for banking, telecommunications, and transaction processing
- Hardware and software redundancy built into every component
- System continues operating even during component failures

## Slide 2: Process Pairs Architecture
- Each critical process has a backup process on different CPU
- Primary process sends checkpoint messages to backup
- Backup process monitors primary via heartbeat signals
- Takeover occurs within seconds of primary failure
- Process state preserved across failures without data loss

## Slide 3: Guardian Operating System Design
- Message-based operating system with no shared memory
- All inter-process communication through messages
- Processes isolated in separate address spaces
- Every system resource accessed via message passing
- Hardware enforced protection boundaries between processes

## Slide 4: Expand Networking Layer
- Transparent network communication across nodes
- Process pairs can span different systems
- Network failures handled automatically
- Load balancing across multiple network paths
- Geographic distribution for disaster recovery

## Slide 5: TMF Transaction Management
- Two-phase commit protocol for distributed transactions
- ACID properties guaranteed across system failures
- Transaction state preserved in audit trails
- Automatic transaction rollback on failure
- Support for long-running business transactions

## Slide 6: Pathway Application Framework
- Server class concept for automatic process management
- Dynamic process creation based on load
- Automatic restart of failed server processes
- Request routing and load distribution
- Built-in monitoring and statistics collection

## Slide 7: Software Fault Tolerance Mechanisms
- I'm Alive messages between process pairs
- Checkpoint data sent at critical points
- Sequence numbers for message ordering
- Automatic rollback to last consistent state
- Error isolation prevents cascade failures

## Slide 8: Hardware Architecture
- Multiple independent CPUs with no shared components
- Dual-ported disks accessible from multiple controllers
- Redundant power supplies and cooling systems
- Hot-swappable components for maintenance
- Error-correcting memory with scrubbing

## Slide 9: Performance and Scalability
- Linear scalability up to 16 processors initially
- Later systems scaled to hundreds of processors
- Sub-second failover times achieved
- 99.999% availability in production systems
- Benchmark performance competitive with non-fault-tolerant systems

## Slide 10: Legacy and Modern Applications
- Evolution to HP NonStop and HPE NonStop platforms
- Stock exchanges rely on NonStop for trading systems
- Payment processors handle billions of transactions
- Telecommunications switches built on NonStop
- Modern cloud services adopting similar architectural principles

## Slide 11: Question for You
How would you model a cyberattack on an electrical power grid?