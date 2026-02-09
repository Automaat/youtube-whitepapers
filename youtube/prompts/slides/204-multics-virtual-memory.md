Generate 11 presentation slides based on the podcast about Multics Virtual Memory Management.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Pre-Multics Era - Memory Management Chaos
- Early systems lacked abstraction between physical and logical memory
- Programmers manually managed memory addresses and overlays
- No memory protection between processes
- Applications required knowledge of exact memory layout
- Resource sharing was primitive and error-prone

## Slide 2: The Multics Vision - Unified Memory Model
- Single-level storage: treat disk and RAM as one continuous address space
- Programs access all resources through virtual addressing
- Supervisor (OS kernel) manages physical-to-virtual mapping
- Goal: eliminate programmer burden of memory management
- Revolutionary idea for 1960s computing

## Slide 3: Segmentation - Logical Memory Division
- Memory organized into variable-length segments
- Each segment represents logical program unit (code, data, stack)
- Segments can grow/shrink independently
- Provides natural boundary for access control
- Aligns with program structure rather than arbitrary pages

## Slide 4: Paging - Physical Memory Allocation
- Fixed-size pages (typically 1KB in Multics) for physical allocation
- Pages map to arbitrary locations in physical RAM
- Solves external fragmentation problem
- Enables efficient memory utilization
- Supervisor maintains page tables for translation

## Slide 5: Two-Level Address Translation
- Virtual address = segment number + offset within segment
- First lookup: segment descriptor table finds segment base
- Second lookup: page table translates virtual page to physical frame
- Hardware support required for acceptable performance
- Combined benefits of segmentation and paging

## Slide 6: Segment Descriptors and Access Control
- Each segment has descriptor with base address, length, permissions
- Descriptor specifies read/write/execute rights
- Bounds checking prevents buffer overruns
- Ring-based protection model (privilege levels)
- Foundation for process isolation and security

## Slide 7: Page Fault Handling and Demand Paging
- Page fault signals when requested page not in physical memory
- Supervisor loads page from disk transparently
- Illusion maintained - process unaware of physical location
- LRU and other algorithms for page replacement
- Enables working with memory larger than physical RAM

## Slide 8: Coremap - Physical Memory Tracking
- Coremap tracks which physical frames are allocated
- Maps physical pages to virtual segments
- Essential for page replacement decisions
- Maintains reference and dirty bits
- Coordinates between virtual and physical views

## Slide 9: Unified Segment Management
- Each segment has unique identifier across entire system
- Segments can be shared between processes
- Single copy of code/data segments in memory
- Reference counting for shared resources
- Simplifies inter-process communication and libraries

## Slide 10: Legacy and Influence on Modern Systems
- Unix inherited simplified version (flat paging)
- Virtual memory became standard in all major OSes
- Segmentation largely abandoned in favor of pure paging
- Ring protection model lives on in x86 architecture
- Demand paging and page replacement still fundamental concepts

## Slide 11: Question for You
Where does the optimal division of tasks between silicon and code lie today?
