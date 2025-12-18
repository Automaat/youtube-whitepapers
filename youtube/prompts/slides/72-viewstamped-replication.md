Generate 11 presentation slides based on the podcast about Viewstamped Replication.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction & Problem Statement

- Critical systems that cannot stop: cloud file systems, ticket booking, bank databases
- Core challenge: what happens when a server fails?
- Goal: transparency - system continues without anyone noticing
- Solution: State Machine Replication with coordinated operation ordering

## Slide 2: State Machine Replication & Notary Analogy

- Three notaries maintaining identical ledgers
- State Machine Replication: replicas process same operations in same order
- Challenge: guaranteeing identical operation order across all replicas
- Leader-based approach: one replica (primary) coordinates all others

## Slide 3: Views & Primary Election

- Views (widoki): periods where specific replica acts as primary
- View Change mechanism triggers when primary fails
- Sequential views ensure system never stops
- Leadership transition maintains consistency during failures

## Slide 4: Quorum Mathematics (2F+1)

- Tolerating F failures requires 2F+1 replicas (3 replicas for F=1)
- Quorum = F+1 replicas (majority must agree)
- Quorum intersection property prevents split-brain scenarios
- Mathematical guarantee: any two quorums share at least one member

## Slide 5: Normal Operation Protocol

- Client sends request to primary
- Primary assigns operation number, sends PREPARE to backups
- Backups log operation, respond with PREPARE-OK
- Primary waits for F confirmations (quorum), commits, responds to client
- Commit point: when quorum acknowledges the operation

## Slide 6: View Change Protocol

- Timeout triggers when primary goes silent
- Three-phase process for leadership transition:
- START-VIEW-CHANGE: backups detect failure
- DO-VIEW-CHANGE: candidates share their logs
- START-VIEW: new primary announces takeover with complete log
- Ensures no committed operations are lost during transition

## Slide 7: VR Revisited - No Disk Writes

- Revolutionary change: eliminates disk writes during normal operation
- Relies on replicated RAM across independent machines
- Assumes independent failures (low probability of F+1 simultaneous crashes)
- Massive performance improvement over disk-based protocols

## Slide 8: Reconfiguration & Witnesses

- Dynamic reconfiguration: add/remove servers without downtime
- Change from F=1 to F=2 (3 to 5 servers) without service window
- Witnesses: lightweight replicas participating in quorum without full state
- Epoch-based configuration changes ensure consistency
- Reduces storage and computation costs

## Slide 9: Performance Optimizations

- Batching: group multiple small requests into one batch
- Fast-reads: read operations bypass primary, go to quorum directly
- Reduces leader load and latency dramatically
- Complete, practical recipe for building fault-tolerant systems

## Slide 10: Comparison with Paxos & Raft

- VR = complete replication protocol vs Paxos = abstract consensus algorithm
- More valuable to engineers: ready-to-implement solution
- Inspired Byzantine fault-tolerant protocols (PBFT)
- Real-world impact: ideas live in distributed systems around us

## Slide 11: Question for You

Wracając do naszej analogii z notariuszami, co by się stało, gdyby jeden z nich nie tylko zachorował, ale zaczął celowo wpisywać fałszywe transakcje do swojej księgi? Które z fundamentalnych założeń tego protokołu, jak quorum czy wybór lidera, musiałyby ulec zmianie, aby chronić system przed kimś, kto aktywnie próbuje go oszukać?
