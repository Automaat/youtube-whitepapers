Generate 11 presentation slides based on the podcast about BigTable.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: BigTable Introduction - Distributed Storage for Structured Data

- Sparse, distributed, persistent multi-dimensional sorted map developed at Google
- Indexed by row key, column key, and timestamp
- Designed to scale to petabytes of data across thousands of commodity servers
- Built on top of Google File System (GFS) for reliable distributed storage
- Provides high performance for both read-heavy and write-heavy workloads
- Powers major Google services: Google Search, Google Analytics, Google Earth

## Slide 2: Data Model - Sparse Multi-Dimensional Map

- Each value in map is uninterpreted array of bytes
- Row key: arbitrary string (up to 64KB, typically 10-100 bytes)
- Column key: grouped into column families (family:qualifier format)
- Timestamp: 64-bit integer representing microseconds since epoch
- Multiple versions of data can be stored per cell with different timestamps
- Sparse structure: missing data consumes no storage space

## Slide 3: Tablets - Horizontal Partitioning Strategy

- Table dynamically partitioned into tablets (unit of distribution and load balancing)
- Each tablet contains contiguous range of rows
- Tablets typically ~100-200 MB in size by default
- Large tables split across many tablets distributed across multiple tablet servers
- Tablet servers handle read/write requests for their assigned tablets
- Dynamic tablet migration for load balancing and failure recovery

## Slide 4: Storage Architecture - MemTable and SSTable

- Writes first go to commit log for durability, then to MemTable (in-memory sorted buffer)
- MemTable: sorted key-value pairs stored in memory for fast writes
- SSTable: immutable, sorted file format stored in GFS for persistent storage
- When MemTable reaches threshold, frozen and converted to SSTable
- Multiple SSTables per tablet created over time through minor compactions
- Major compaction merges SSTables and removes deleted data

## Slide 5: SSTable Format - Persistent Ordered Immutable Map

- Sequence of 64KB blocks (configurable size) stored in GFS
- Block index stored at end of SSTable for efficient lookups
- Index loaded into memory when SSTable opened
- Single disk seek required to read data (one seek for index, one for block)
- Immutability enables efficient concurrent reads without synchronization
- Bloom filters reduce disk seeks for non-existent rows

## Slide 6: Garbage Collection and Data Versioning

- System supports keeping last N versions or versions from last N days
- Garbage collection during compaction removes obsolete versions
- Deleted data marked with deletion marker (tombstone)
- Physical deletion occurs during major compaction
- Old SSTables can be safely deleted after new SSTable created
- Version management enables time-travel queries and historical data analysis

## Slide 7: Performance Optimizations - Bloom Filters and Compression

- Bloom filters: space-efficient probabilistic data structure to test set membership
- Reduces disk seeks by quickly identifying SSTables that don't contain requested row
- Compression applied to each SSTable block using configurable algorithms
- Two-level compression: custom fast compression, then BMDiff or Zippy
- Locality groups: column families grouped together for better compression ratios
- In-memory column families for frequently accessed small data

## Slide 8: Real-World Use Cases at Google Scale

- Google Analytics: stores raw click data (petabytes), user session analysis
- Google Earth: terabytes of satellite imagery indexed by geographic coordinates
- WebTable: stores crawled web pages and metadata for search indexing
- Personalized Search: stores per-user data for search history and preferences
- Google Maps: geographic data, point-of-interest information, routing data
- All systems handle massive scale with commodity hardware

## Slide 9: Lessons from Production - Building Distributed Systems

- Simple, well-understood building blocks enable complex systems
- Immutable data structures simplify concurrent access and replication
- Delay addressing problems until they become significant bottlenecks
- Start with simple designs, measure performance, then optimize
- Proper system monitoring and debugging tools are essential
- Design for failures: hardware failures are normal at scale, not exceptions

## Slide 10: BigTable vs Traditional Databases - Trade-offs

- No full relational model: no joins, no complex SQL queries
- No ACID transactions across row keys (only single-row transactions)
- Eventually consistent: not strictly consistent like traditional RDBMS
- In return: massive horizontal scalability and high throughput
- Suitable for applications that need simple read/write operations at scale
- Foundation for later NoSQL systems: HBase, Cassandra inspired by BigTable

## Slide 11: Question for You

What would be your strategy for choosing between BigTable's scalability model and traditional relational databases with rich query languages, and what acceleration would it offer?
