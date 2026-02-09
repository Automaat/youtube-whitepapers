Generate 11 presentation slides based on the podcast about the Fast File System for UNIX.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Performance Crisis of Early UNIX File Systems
- Original UNIX file system from 1974: 512-byte blocks, sequential inode allocation
- VAX 11/750 performance: only 3-5% of theoretical disk throughput utilized
- Main bottleneck: excessive seek operations due to fragmented data layout
- Critical need for redesign as systems scaled to larger disks and more users

## Slide 2: The Problem with 512-Byte Blocks
- 512-byte blocks required constant disk head movement for any substantial file
- 2048-byte blocks improved throughput to 30% but wasted significant disk space
- Small files (< 2KB) comprised majority of files in typical UNIX systems
- Trade-off between performance and storage efficiency seemed insurmountable

## Slide 3: The Breakthrough: Cylinder Groups
- Disk divided into cylinder groups - localized regions with own metadata copies
- Each cylinder group contains: superblock copy, inode bitmap, block bitmap, inodes, and data blocks
- Strategy: keep related data physically close on disk to minimize seek time
- Typical size: 16 cylinders per group for optimal locality

## Slide 4: Smart Allocation Strategies
- Files in same directory allocated within same cylinder group when possible
- Inodes for directory entries placed near the directory's own inode
- Large files distributed across multiple cylinder groups to prevent monopolization
- Redirect threshold: after 48KB in one group, continue in another group

## Slide 5: The Fragment Solution for Small Files
- Blocks divided into fragments (typically 1024 bytes from 8192-byte blocks)
- Small files use fragments, avoiding 87% waste from full block allocation
- Fragments from different files can share same block, maximizing efficiency
- Fragment coalescing: automatic merging when files grow beyond fragment size

## Slide 6: Performance Optimizations in FFS
- Disk access reduced from 6-7 operations per file creation to just 2
- Sequential read performance: near 100% of disk bandwidth achieved
- Write performance: 50% of disk bandwidth (limited by rotational delay)
- 10x improvement over original UNIX file system in real-world usage

## Slide 7: CPU Overhead and Bitmap Management
- Bitmap operations for free space tracking: initially 40% CPU overhead
- Problem: scanning bitmaps for free blocks consumed significant processor time
- Solution: optimized assembly routines reduced overhead to just 11%
- Lesson: even elegant algorithms need low-level optimization for production systems

## Slide 8: Large File Optimization Challenges
- Large files scattered across cylinder groups caused fragmentation over time
- Solution: reserve 10% of disk space to maintain allocation flexibility
- Dynamic reallocation: system moves files when better placement becomes available
- Trade-off: slightly reduced usable capacity for sustained performance

## Slide 9: System Call Innovations
- Atomic rename() operation: eliminated window for corruption during file moves
- Long file names: increased from 14 to 255 characters maximum
- Symbolic links: references to files by pathname rather than inode
- Advisory file locking: cooperative mechanism for multi-process coordination

## Slide 10: Real-World Impact and Legacy
- Adopted as standard in 4.2BSD UNIX release (1984)
- Performance gains enabled UNIX adoption in commercial environments
- Design principles influenced: ext2/3/4, NTFS, HFS+, and ZFS
- Key insight: locality of reference more important than raw algorithm efficiency

## Slide 11: Question for You
Which performance optimizations that we admire today are actually preparing the ground for revealing completely different bottlenecks we don't yet know about?