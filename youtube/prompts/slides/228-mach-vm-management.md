Generate 11 presentation slides based on the podcast about Machine-Independent Virtual Memory Management for Paged Uniprocessor and Multiprocessor Architectures.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Mach VM Architecture Revolution
- Radical separation of machine-dependent and machine-independent code
- Only ~650 lines of VAX-specific code out of 14,000 total lines
- Portable across diverse hardware: VAX, IBM RT PC, Sun 3, Intel 80386
- Achieved through abstraction layers: address maps, memory objects, and pagers

## Slide 2: The Problem with Traditional VM Systems
- Previous systems tightly coupled VM management with hardware specifics
- Each new architecture required complete rewrite of memory management
- VM operations like copy-on-write spread across multiple system modules
- Hardware details (TLB, MMU) mixed with high-level memory policies
- Porting VM systems took months or years of engineering effort

## Slide 3: Mach's Three-Layer Architecture
- Physical layer: pmap module handles hardware-specific operations
- Logical layer: machine-independent VM management with address maps
- External pagers: user-space memory management for specialized needs
- Clear separation enables 3-week ports to new architectures
- Pmap module encapsulates all MMU, TLB, and page table operations

## Slide 4: Virtual Memory as Objects
- Memory regions represented as memory objects with data and operations
- Address maps organize virtual address space as non-overlapping entries
- Each address map entry points to specific memory object regions
- Copy-on-write, shared memory, and inheritance handled uniformly
- Shadow objects implement copy-on-write without complex bookkeeping

## Slide 5: The Genius of Shadow Objects
- Created automatically during copy-on-write operations
- Forms chains to original memory objects for unmodified pages
- Eliminates need for reference counting or complex data structures
- Supports efficient fork() operations and memory sharing
- Transparent to applications - works with any memory object type

## Slide 6: External Pager Interface
- User-space processes can implement custom memory management
- Communicates with kernel via message-passing protocol
- Enables distributed shared memory, persistent objects, databases
- Kernel requests pages via memory_object_data_request messages
- Pagers respond with memory_object_data_provided containing page data

## Slide 7: The Pmap Interface Magic
- Just 16 functions define entire hardware abstraction layer
- Core operations: pmap_enter, pmap_remove, pmap_protect, pmap_page_protect
- Handles physical-to-virtual mappings and TLB management
- Machine-independent code never touches page tables directly
- Enables optimizations like superpages and clustered TLB operations

## Slide 8: Performance Through Lazy Evaluation
- Page tables built only when needed (lazy allocation)
- TLB entries loaded on-demand during page faults
- Copy operations don't copy data - just manipulate mappings
- Virtual-to-physical translations cached for efficiency
- Batch operations reduce context switches and TLB flushes

## Slide 9: Real-World Impact and Legacy
- Influenced modern systems: Windows NT, OSF/1, MacOS X
- Proved microkernel VM could match monolithic kernel performance
- Enabled research in distributed shared memory systems
- Demonstrated clean separation of policy and mechanism
- Made VM portability a practical reality, not just theory

## Slide 10: Challenges and Trade-offs
- Message passing overhead for external pagers
- Complexity of shadow object chains in deep fork hierarchies
- Balancing abstraction with hardware-specific optimizations
- Trust and security issues with user-space pagers
- Performance tuning requires understanding multiple layers

## Slide 11: Question for You
Where does the optimal boundary lie between kernel security and performance versus the flexibility and development simplicity provided by user space?