Generate 11 presentation slides based on the podcast about Disco: Running Commodity Operating Systems on Scalable Multiprocessors.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Challenge of Scalable Multiprocessors
- Stanford's Flash project addressed hardware costs reaching millions of dollars
- CC-NUMA (Cache Coherent Non-Uniform Memory Access) machines introduced new complexity
- Traditional operating systems required extensive modifications for multi-processor support
- The paradox: powerful hardware existed but software couldn't effectively utilize it
- Need for a solution that preserves existing OS investments while scaling to new architectures

## Slide 2: The Economics of Operating System Modification
- Porting an OS to multiprocessor systems took years of development time
- Required deep expertise in both OS internals and parallel programming
- Millions of lines of code needed modification for proper NUMA awareness
- Cost-benefit analysis often favored running unmodified single-processor systems
- Industry needed a way to leverage existing commodity operating systems

## Slide 3: Understanding CC-NUMA Architecture
- Each processor has local memory with fast access times
- Accessing remote memory through interconnect adds significant latency
- Hardware maintains cache coherence across all processors automatically
- Memory access times vary by location (Non-Uniform Memory Access)
- Up to 64 processors could be connected in Stanford's Flash machine

## Slide 4: The Disco Virtual Machine Monitor Solution
- Thin virtualization layer between hardware and operating systems
- Multiple unmodified operating systems run simultaneously as guests
- Each OS believes it has exclusive hardware access
- Disco handles resource multiplexing and NUMA optimization transparently
- Minimal overhead: less than 16,000 lines of code

## Slide 5: Virtual CPU (VCPU) Management
- Virtual CPUs act as the processor's scheduler notebook
- Maps virtual processors to physical cores dynamically
- Maintains processor state including registers and TLB entries
- Enables transparent migration between physical processors
- Direct execution model: guest code runs natively when possible

## Slide 6: Memory Virtualization Techniques
- Two-level address translation: virtual → physical → machine addresses
- TLB (Translation Lookaside Buffer) managed cooperatively with guests
- Copy-on-write sharing for common pages across VMs
- NUMA-aware memory allocation to minimize remote accesses
- Dynamic page migration based on access patterns

## Slide 7: CPU and Memory Scheduling Innovations
- Affinity scheduling keeps VCPUs near their memory
- Load balancing across NUMA nodes prevents hotspots
- Cache-aware scheduling minimizes cache pollution
- Idle loop detection prevents wasted CPU cycles
- Transparent page replication for frequently accessed read-only pages

## Slide 8: Solving the Memory Overhead Problem
- Global buffer cache eliminates redundant data copies
- Transparent page sharing between identical OS instances
- Zero-copy networking through remapped pages
- Memory ballooning for dynamic resource adjustment
- Compression and deduplication for memory-constrained scenarios

## Slide 9: Performance Optimization Layers
- User space applications run unmodified
- Kernel space operates with minimal virtualization overhead
- Disco's thin monitor layer adds typically 3-5% overhead
- Hardware abstraction layer provides uniform interface
- Direct device access for performance-critical operations

## Slide 10: Impact and Legacy
- Enabled running unmodified IRIX on multiprocessor systems immediately
- Influenced VMware's founding and commercial virtualization
- Demonstrated viability of virtualization for resource management
- Paved the way for modern cloud computing infrastructure
- Showed that old problems (virtualization) could solve new challenges (NUMA)

## Slide 11: Question for You
How should this influence the design of new computer architectures?