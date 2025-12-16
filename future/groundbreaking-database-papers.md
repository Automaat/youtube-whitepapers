# 📚 Groundbreaking Database Papers

**Date:** 2024-12-16
**Tags:** #research #databases #papers #distributed-systems
**Focus:** Seminal & influential database whitepapers

---

## 🏛️ Foundational Papers

### Relational Model
- **"A Relational Model of Data for Large Shared Data Banks"** (1970) - E.F. Codd
  - Foundation for ALL SQL databases
  - Introduced data independence principles
  - [Original Paper](https://dl.acm.org/doi/10.1145/362384.362685)

### Transaction Recovery
- **"ARIES: A Transaction Recovery Method"** (1992) - Mohan et al.
  - Write-ahead logging (WAL)
  - Fine-granularity locking, partial rollbacks
  - Still used in most modern RDBMS

### Query Optimization
- **"Access Path Selection in a Relational DBMS"** (1979) - Selinger et al. (System R)
  - Cost-based query optimization
  - Foundation of modern query planners

### Concurrency Control
- **"On Optimistic Methods for Concurrency Control"** (1981) - Kung & Robinson
  - Alternative to locking
  - Basis for modern MVCC implementations

- **"Concurrency Control in Distributed Database Systems"** (1981) - Bernstein & Goodman
  - MVCC described in detail
  - Foundation for PostgreSQL, Oracle, MySQL InnoDB

---

## 🌐 Distributed Systems Classics

### Google's Trinity

| Paper | Year | Impact |
|-------|------|--------|
| **Google File System (GFS)** | 2003 | Append-only distributed FS, inspired HDFS |
| **MapReduce** | 2004 | Distributed computation paradigm |
| **Bigtable** | 2006 | Wide-column store, inspired HBase, Cassandra |

### Consensus & Consistency
- **"Paxos Made Simple"** (2001) - Lamport
  - Fault-tolerant distributed consensus

- **"In Search of an Understandable Consensus Algorithm" (Raft)** (2014) - Ongaro & Ousterhout
  - More understandable than Paxos
  - Used in etcd, CockroachDB, TiKV

- **"Time, Clocks, and Ordering of Events"** (1978) - Lamport
  - Fundamental to distributed databases, blockchain
  - Logical clocks concept

- **"CAP Twelve Years Later"** (2012) - Brewer
  - Retrospective on consistency/availability tradeoffs

### Key-Value Stores
- **"Chord: A Scalable Peer-to-peer Lookup Service"** (2001)
  - Consistent hashing for distributed systems

- **"Dynamo: Amazon's Highly Available Key-value Store"** (2007)
  - Eventually consistent, always-writable
  - Inspired Cassandra, Riak, Voldemort

---

## 🚀 Modern Distributed SQL (NewSQL)

### Google's Next Generation
- **"Spanner: Google's Globally Distributed Database"** (2012) ⭐
  - **SIGOPS Hall of Fame Award**
  - TrueTime API - synchronized clocks for global transactions
  - First system with externally-consistent distributed transactions
  - [Paper PDF](https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf)

- **"F1: A Distributed SQL Database That Scales"** (2013)
  - Built on Spanner
  - Replaced MySQL for Google AdWords
  - SQL + NoSQL best of both worlds

### Open Source NewSQL
- **"CockroachDB: The Resilient Geo-Distributed SQL Database"** (2020)
  - Spanner-inspired, PostgreSQL-compatible
  - Raft consensus, parallel commits optimization

- **"TiDB: A Raft-based HTAP Database"** (2020)
  - MySQL-compatible
  - Separates compute/storage (TiKV)

---

## 📊 Analytical & Columnar Systems

### Column-Oriented Revolution
- **"C-Store: A Column-oriented DBMS"** (2005) - Stonebraker et al.
  - Academic foundation for analytical DBs
  - Led to Vertica

- **"Column-Stores vs. Row-Stores: How Different Are They Really?"** (2012)
  - Definitive comparison paper

- **"Dremel: Interactive Analysis of Web-Scale Datasets"** (2010)
  - Nested columnar format
  - Massively parallel queries
  - Inspired Parquet, BigQuery, Drill

### Data-Parallel Processing
- **"Resilient Distributed Datasets (RDD)"** (2012) - Zaharia et al.
  - Foundation of Apache Spark
  - Orders of magnitude faster than MapReduce for iterative workloads

---

## 🌲 Storage Engines

### LSM-Trees
- **"The Log-Structured Merge-Tree"** (1996) - O'Neil et al.
  - Foundation for write-optimized storage
  - Used in: LevelDB, RocksDB, Cassandra, HBase, TiKV

- **"RocksDB: Evolution of Development Priorities"** (2021) - Facebook
  - Most influential embedded KV store
  - Powers TiDB, YugabyteDB, Kafka Streams, CockroachDB

### B-Trees
- **"Efficient Locking for Concurrent Operations on B-Trees"** (1981)
  - Core data structure for OLTP

- **"R*-tree: An Efficient Access Method for Points and Rectangles"** (1990)
  - Multi-dimensional spatial indexing

---

## 🤖 Vector Databases & AI (2024 Hot Topic)

### Core Papers
- **"The FAISS Library"** (2024) - Meta AI
  - Foundational ANN search library
  - Used by Pinecone, Zilliz, many VDBMSs
  - [ArXiv 2401.08281](https://arxiv.org/pdf/2401.08281)

- **"Hierarchical Navigable Small Worlds (HNSW)"** (2016) - Malkov & Yashunin
  - Graph-based approximate nearest neighbor
  - Logarithmic scaling in high dimensions
  - Supported by most commercial vector DBs

- **"Survey of Vector Database Management Systems"** (2024) - Tsinghua
  - Comprehensive survey of 20+ VDBMSs
  - [PDF](https://dbgroup.cs.tsinghua.edu.cn/ligl/papers/vldbj2024-vectordb.pdf)

---

## 📖 Meta-Resources

### Reading Lists
- **"Readings in Database Systems" (Red Book)** - Bailis, Hellerstein, Stonebraker
  - Comprehensive overview of DB research history
  - [Online version](http://www.redbook.io/)

- **"What Goes Around Comes Around"** - Stonebraker & Hellerstein
  - 35 years of data modeling history
  - 9 different eras of proposals

- **[rxin/db-readings](https://github.com/rxin/db-readings)** - GitHub
  - Curated list for understanding databases

- **[Ryan Marcus - Most Influential Papers](https://rmarcus.info/blog/2023/07/25/papers.html)**
  - PageRank-based ranking of SIGMOD/VLDB/CIDR/PODS papers

---

## 🎯 Must-Read Priority List

### If you read only 10 papers:
1. 📜 Codd's Relational Model (1970)
2. 🕐 Lamport's Time & Clocks (1978)
3. 📁 Google File System (2003)
4. 🗺️ MapReduce (2004)
5. 📊 Bigtable (2006)
6. 🔑 Dynamo (2007)
7. 📈 Dremel (2010)
8. ⚡ Spark RDDs (2012)
9. 🌍 Spanner (2012)
10. 🌲 LSM-Tree or RocksDB paper

---

## 🔗 Related Notes

- [[distributed-computing-papers]] - Raft, Paxos, consensus
- [[data-engineering-papers]] - ETL, streaming
- [[AI-infrastructure]] - Vector DBs, embeddings

---

## 📚 Sources

- [rxin/db-readings](https://github.com/rxin/db-readings)
- [Ryan Marcus - Influential Papers](https://rmarcus.info/blog/2023/07/25/papers.html)
- [Andy Pavlo - 2024 Databases Retrospective](https://www.cs.cmu.edu/~pavlo/blog/2025/01/2024-databases-retrospective.html)
- [Data Engineering Whitepapers](https://www.ssp.sh/brain/data-engineering-whitepapers/)
- [Paper Digest - SIGMOD](https://www.paperdigest.org/2025/09/most-influential-sigmod-papers-2025-09-version/)
