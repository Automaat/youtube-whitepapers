Generate 11 presentation slides based on the podcast about VM/370 Time-Sharing System.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Birth of Virtual Machines
- IBM System/370 introduced revolutionary virtualization in 1972
- CP-67 (Control Program) enabled multiple virtual machines on single mainframe
- Each virtual machine appeared as complete, independent system to users
- Time-sharing allowed multiple users to work simultaneously on expensive hardware
- Virtual machines could run different operating systems concurrently

## Slide 2: Architecture of CP/CMS System
- Control Program (CP) acted as hypervisor managing virtual machines
- Cambridge Monitor System (CMS) ran as single-user OS on each VM
- Two-layer architecture separated resource management from user interface
- CP handled hardware virtualization, memory management, and I/O simulation
- CMS provided interactive computing environment for individual users
- Each VM had illusion of dedicated System/370 mainframe

## Slide 3: The Problem VM/370 Solved
- Mainframes cost millions but sat idle most of the time
- Batch processing created long wait times for developers
- Multiple incompatible operating systems needed same hardware
- Testing new OS versions required dedicated machines
- Remote access demanded expensive dedicated terminals
- Traditional time-sharing systems limited user flexibility

## Slide 4: CMS - Simplicity Over Complexity
- CMS designed as lightweight single-user operating system
- Eliminated complex scheduling and memory management
- Focused on interactive development and debugging
- Provided file system, editor, and programming tools
- Much simpler than full multi-user operating systems
- Let CP handle resource sharing between virtual machines

## Slide 5: Hardware Virtualization Techniques
- Supervisor state operations trapped and emulated by CP
- Virtual memory gave each VM illusion of full address space
- I/O instructions intercepted and redirected to virtual devices
- Timer interrupts multiplexed among virtual machines
- Privileged instructions caused traps to hypervisor
- Shadow page tables maintained for each virtual machine

## Slide 6: Virtual Machine Isolation
- Complete isolation between virtual machines
- VM crash didn't affect other users or system
- Each VM could run different OS version or configuration
- Security through hardware-enforced boundaries
- Users could experiment without system-wide impact
- Enabled safe OS development and testing environment

## Slide 7: Recursive Virtualization Innovation
- VM/370 could run inside another VM/370
- Users could create nested virtual machines
- Enabled multi-level testing environments
- Demonstrated completeness of virtualization approach
- CP could virtualize itself without modification
- Theoretical importance proved practical virtualization

## Slide 8: Performance and Resource Management
- CP-67 efficiently scheduled CPU time between VMs
- Memory paging allowed overcommitment of physical RAM
- Virtual devices multiplexed physical hardware
- Dynamic resource allocation based on demand
- Performance monitoring built into system
- Achieved 80-90% of native hardware performance

## Slide 9: Virtual Networking and Communication
- CP simulated virtual modems and communication lines
- Virtual machines could network without physical connections
- Inter-VM communication through virtual channels
- Remote access through virtual terminal connections
- Eliminated need for dedicated hardware per user
- Created foundation for modern virtual networking

## Slide 10: Legacy and Impact
- Pioneered concepts used in modern hypervisors (VMware, Xen, KVM)
- Established virtualization as fundamental computing abstraction
- Enabled cloud computing and server consolidation
- Influenced development of microkernels and containers
- IBM mainframes still use evolved VM technology today
- Demonstrated hardware can become transparent to users

## Slide 11: Question for You
Will physical hardware that powers everything become completely transparent and irrelevant to us?