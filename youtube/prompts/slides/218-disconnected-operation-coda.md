Generate 11 presentation slides based on the podcast about Disconnected Operation in the Coda File System.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Problem of Disconnected Operation
- Early 1990s: Mobile computing meant bulky laptops and fragile network connections
- Traditional distributed file systems required constant server connectivity
- Network disconnection meant complete work stoppage - "game over" for productivity
- Coda's radical shift: treating disconnection as a normal operating mode, not a failure

## Slide 2: Coda's Two-Pillar Architecture
- First pillar: Server Replication for high availability
- AVSG (Accessible Volume Storage Group) maintains replicated data across multiple servers
- System remains operational as long as one server in AVSG is accessible
- Second pillar: Disconnected Operation when all servers become unreachable

## Slide 3: Venus - The Intelligent Client
- Venus transitions from simple client to local file system manager during disconnection
- Operates in three distinct modes: Hoarding, Emulation, and Reintegration
- Maintains complete file system semantics during disconnection
- Acts as a transparent layer between applications and the distributed file system

## Slide 4: Hoarding Mode - Proactive Caching
- Venus proactively caches files before disconnection based on user priorities
- Users define critical files and directories in the Hoard Database (HDB)
- System balances user preferences with recent usage patterns (LRU)
- Automatic periodic walks ensure cache freshness every 10 minutes

## Slide 5: The Optimistic Concurrency Bet
- Empirical data from AFS showed concurrent write-write conflicts at only 0.75%
- Most file access patterns were sequential, not simultaneous
- Coda made a calculated risk: assume conflicts won't happen
- The reward: full productivity during disconnection outweighed minimal conflict risk

## Slide 6: Emulation Mode - Working Offline
- Venus serves all file operations from local cache during disconnection
- Creates "pseudo-fids" (fake file identifiers) for new files
- Maintains complete log of all operations in the CML (Client Modification Log)
- Applications continue working unaware of the disconnection

## Slide 7: Client Modification Log (CML)
- Records every file operation performed during disconnection
- Optimized to minimize size: cancels out redundant operations
- Stores operations, not data - actual files remain in cache
- Critical for conflict detection and resolution during reintegration

## Slide 8: Reintegration - Reconnecting to the Network
- Venus replays the entire CML to the server upon reconnection
- Store IDs ensure atomic transaction-like behavior
- Server validates each operation against current state
- Successful replay merges all offline work seamlessly

## Slide 9: Conflict Resolution Strategies
- Automatic resolution for directory conflicts (e.g., concurrent file creation)
- File conflicts require manual intervention through repair tools
- System preserves both versions when conflicts occur
- Repair session allows users to choose or merge conflicting versions

## Slide 10: Impact and Modern Relevance
- Coda pioneered optimistic replication, influencing Git, Dropbox, and Google Docs
- Demonstrated that disconnected operation was not just possible but practical
- Paradox: Modern cloud-first apps often have worse offline support than 1990s Coda
- The vision of seamless offline work remains partially unfulfilled 30+ years later

## Slide 11: Question for You
Are our modern cloud-first applications, which become useless without constant high-speed connectivity, actually a step backward in availability compared to the vision that Coda outlined over 30 years ago?