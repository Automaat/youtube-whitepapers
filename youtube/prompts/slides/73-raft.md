Generate 11 presentation slides based on the podcast about the Raft consensus algorithm.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Paxos: The Consensus King with Fatal Flaws

- Paxos dominated distributed consensus for years as the standard algorithm
- First major problem: notoriously difficult to understand - even experienced researchers struggled
- Second critical issue: only solves "single decree" consensus, not practical multi-decision systems
- Implementations required ad-hoc extensions, creating unproven custom protocols
- Real human cost: complexity barrier prevented building reliable distributed systems

## Slide 2: Raft's Revolutionary Goal: Understandability First

- Primary design objective: make consensus understandable, not just correct
- Two powerful techniques: decomposition and state space reduction
- Split monolithic consensus into three independent subproblems
- Leader election - choose single coordinator
- Log replication - distribute state changes
- Safety - guarantee correctness properties
- Reduce non-determinism through enforced structure and constraints

## Slide 3: Strong Leader Principle

- All client operations flow through single elected leader
- Only leader can append new entries to replicated log
- Leader replicates entries to follower servers
- Eliminates write conflicts and coordination chaos
- Trade-off: leader is potential bottleneck, but simplifies system dramatically
- Assumes "leader died" failures more common than "leader zombie" scenarios

## Slide 4: Terms: Logical Clocks for Distributed Time

- Time divided into numbered sequential periods called terms
- Each term begins with leader election
- Successful election: one leader governs for remainder of term
- Failed election: term ends immediately, new term begins with new election
- Term number acts as logical timestamp on every message
- Enables servers to detect stale information and maintain temporal order

## Slide 5: Three Server States

- Leader: active coordinator, handles all client requests, replicates log
- Follower: passive replica, only responds to leader commands
- Candidate: temporary state during leader election process
- Normal operation: exactly one leader, all others are followers
- Candidate state appears briefly when leader fails and elections begin

## Slide 6: Leader Election Mechanism

- Followers monitor leader through periodic heartbeats
- Each follower sets randomized election timeout from configured range
- Timeout expires without heartbeat → follower becomes candidate
- Candidate increments term, votes for self, requests votes from all servers
- Must collect majority votes to become leader
- Randomized timeouts prevent split votes - first candidate almost always wins
- Elegant solution: add randomness to eliminate coordination catastrophe

## Slide 7: Log Replication and Append Entries

- Leader receives client commands, appends to own log
- Sends AppendEntries RPC to all followers with new entries
- Each AppendEntries includes info about preceding log entry (index + term)
- Follower accepts only if it has matching preceding entry at same position
- Rejection indicates divergent histories - leader walks backward to find common point
- Log Matching Property: ensures consistency through incremental verification

## Slide 8: Safety Guarantees and Commit Rules

- Entry is committed when safely replicated on majority of servers
- Leader tracks highest committed index, includes in AppendEntries
- Followers learn commit status and apply entries to state machine
- Leader Election Restriction: candidate can only win if log is at least as up-to-date
- Voters reject candidates with outdated logs (compare term + index)
- Prevents committed entries from being lost during leader transitions

## Slide 9: Cluster Membership Changes

- Dynamic reconfiguration without shutting down entire system
- Two-phase approach using joint consensus configuration
- Phase 1: activate joint consensus (old + new servers both require majority)
- Phase 2: transition to new configuration alone after joint config committed
- Guarantees single unambiguous majority exists throughout entire change process
- Prevents split-brain scenarios during membership transitions

## Slide 10: Performance and Timing Requirements

- Performance comparable to complex Paxos variants in typical scenarios
- Commit requires one communication round with cluster majority - optimal
- Critical timing inequality: broadcast time ≪ election timeout ≪ MTBF
- Broadcast time: average RPC round-trip time to all servers
- Election timeout: randomized timeout before starting election
- MTBF: mean time between failures for single server
- When timing holds: cluster remains stable, available, rarely has unnecessary elections

## Slide 11: Question for You

Czy w naszej branży, która często goni za każdą milisekundą optymalizacji, powinniśmy częściej zadawać sobie pytania o koszt złożoności? Czy prostota, która umożliwia budowanie solidniejszych, łatwiejszych w utrzymaniu i po prostu bardziej ludzkich systemów, nie jest ostatecznie najwyższą i najbardziej pożądaną formą wydajności?
