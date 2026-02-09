Generate 11 presentation slides based on the podcast about The Working Set Model for Program Behavior by Peter J. Denning.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Memory Management Crisis of 1968
- Virtual memory systems were new but struggling with performance
- Thrashing occurred when too many programs competed for limited physical memory
- Systems spent more time paging than executing useful work
- Page replacement algorithms (FIFO, LRU) failed to prevent system-wide slowdowns
- Denning recognized need for predictive rather than reactive memory management

## Slide 2: Understanding Virtual Memory Fundamentals
- Physical memory (RAM) is the limited workspace, like a kitchen counter
- Virtual memory creates illusion of unlimited memory using disk storage
- Pages are fixed-size blocks of memory that can be swapped between RAM and disk
- Page faults occur when program accesses data not currently in physical memory
- Operating system must decide which pages to keep in memory and which to evict

## Slide 3: The Observer's Insight - Locality of Reference
- Programs don't access memory randomly - they exhibit patterns
- Temporal locality: recently accessed pages likely to be accessed again soon
- Spatial locality: pages near recently accessed pages likely to be needed
- Programs work in phases, each with its own memory access pattern
- Key observation: at any time, a program actively uses only a small subset of its pages

## Slide 4: Traditional Page Replacement Failures
- FIFO (First In, First Out): removes oldest page regardless of usage patterns
- LRU (Least Recently Used): better but still reactive, not predictive
- Both algorithms treat all page faults equally, missing program behavior patterns
- No consideration of how many pages a program actually needs to run efficiently
- System-wide thrashing occurs when combined working sets exceed physical memory

## Slide 5: The Working Set Definition
- Working Set W(t,τ): set of pages referenced in time interval [t-τ, t]
- Parameter τ (TAU) defines the observation window size
- Captures the "active memory footprint" of a program at any moment
- Size varies dynamically as program moves through execution phases
- Revolutionary idea: allocate memory based on predicted future needs, not past faults

## Slide 6: Mathematical Foundation and Properties
- Working set size |W(t,τ)| changes over time with program behavior
- Monotonic property: W(t,τ₁) ⊆ W(t,τ₂) when τ₁ ≤ τ₂
- Convergence: as τ increases, working set approaches total program pages
- Phase transitions visible as rapid changes in working set composition
- Statistical stability: working set size relatively constant within program phases

## Slide 7: Implementation Strategy
- Track page references using hardware reference bits or software counters
- Periodically sample and update each process's working set estimate
- Two key parameters per process: working set size and update frequency
- Allocate exactly the pages in current working set, no more, no less
- Suspend processes when total working sets exceed available memory

## Slide 8: The Balance Set Policy
- System maintains "balance set" - collection of active processes
- Admission control: new process enters only if its working set fits
- Memory pressure response: suspend process with largest working set
- Prevents thrashing by ensuring each active process has sufficient memory
- Dynamic adjustment: processes suspended/resumed based on memory availability

## Slide 9: Performance Impact and Benefits
- Dramatic reduction in page fault rates when working set satisfied
- System throughput increases by preventing thrashing
- Better CPU utilization through reduced paging overhead
- Fair memory allocation based on actual program needs
- Predictable performance through proactive memory management

## Slide 10: Modern Legacy and Applications
- Windows uses working set trimming for memory management
- Linux memory pressure algorithms influenced by working set concepts
- Database buffer pools implement working set principles
- Cloud container memory limits based on working set monitoring
- Machine learning systems apply similar concepts for GPU memory management

## Slide 11: Question for You
What other complex systems beyond computing - from logistics networks to traffic management to financial markets - could be managed more effectively by observing their dynamic working set of recent activity rather than using static rules?