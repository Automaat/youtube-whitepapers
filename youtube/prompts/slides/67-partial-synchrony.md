Generate 11 presentation slides based on the podcast about "Paxos Made Moderately Complex" by Robbert van Renesse and Deniz Altinbuken.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Distributed Consensus Challenge

- How can multiple computers connected via unreliable network agree on a single truth?
- Example: banking transaction ordering across replicated databases
- Messages arrive delayed, out-of-order, or servers disappear from network
- Core challenge: building reliable systems in unreliable environments
- Foundation for Google Chubby, Apache ZooKeeper, etcd, Google Spanner

## Slide 2: Partial Synchrony Model

- Asynchronous model: no time bounds, FLP impossibility theorem (consensus impossible)
- Synchronous model: guaranteed message delivery time (unrealistic for internet)
- Partial synchrony: realistic middle ground - network eventually stabilizes
- System operates asynchronously but eventually becomes synchronous
- Enables practical consensus protocols like Paxos to guarantee both safety and liveness

## Slide 3: Paxos Protocol Architecture

- Three core roles: Leaders, Acceptors, Replicas
- Leaders: propose commands and coordinate voting (can have multiple, but one active)
- Acceptors: vote on proposals and maintain protocol's persistent memory (need 2F+1 for F failures)
- Replicas: execute State Machine Replication (RSM), apply decided commands
- Quorum-based approach: majority agreement ensures consistency across failures
- Single node can play multiple roles simultaneously

## Slide 4: Ballots vs Proposals

- Proposal: the actual command/operation to be agreed upon
- Ballot: formal voting session initiated by leader with unique, monotonically increasing number
- Ballot number acts as version control for voting rounds
- Prevents old, delayed messages from interfering with current decisions
- Each slot (position in command sequence) can have multiple ballot attempts
- Higher ballot numbers can override lower ones during voting

## Slide 5: Phase 1 - Prepare & Promise

- Leader sends P1A message with ballot number B to acceptors
- Asks: "Will you promise not to accept proposals from ballots lower than B?"
- Acceptors respond with P1B containing their promise and highest previously accepted proposal
- Leader learns what was potentially decided in earlier ballots
- If leader gets majority promises, proceeds to Phase 2
- This phase establishes ordering and prevents conflicts

## Slide 6: Phase 2 - Accept & Accepted

- Leader sends P2A message with chosen command to acceptors
- If learned about previous acceptance in Phase 1, must propose that same command
- If no previous acceptance, can propose new command
- Acceptors vote by sending P2B if ballot hasn't been superseded
- When majority accepts, decision is made (but not yet known to all)
- Replicas learn decisions and execute commands in slot order

## Slide 7: Multi-Paxos Optimization

- Basic Paxos: run full protocol for every single command (expensive)
- Multi-Paxos: stable leader skips Phase 1 for subsequent commands
- Reduces 4 message round trips to 2 round trips per command
- Leader pre-establishes authority, then streams commands
- Dramatic latency improvement for sequential operations
- Requires stable leader election mechanism

## Slide 8: Leader Election & Dueling Leaders

- Scout process: new leader runs Phase 1 to establish authority
- Commander process: established leader runs Phase 2 for commands
- Problem: dueling leaders can create livelock (mutual blocking)
- Example: Leader A starts ballot 100, Leader B starts 101, A retaliates with 102
- Solution: randomized timeouts prevent synchronization of conflicts
- Eventually one leader succeeds and maintains stability

## Slide 9: Practical Implementation Optimizations

- State reduction: acceptors only remember highest ballot per slot (not full history)
- Garbage collection: delete decided slot data after all replicas learn decision
- No-op optimization: read-only operations bypass Paxos entirely
- Batching: combine multiple commands into single Paxos instance
- Pipelining: start next ballot before previous completes
- Memory and performance critical for real-world deployments

## Slide 10: Beyond Basic Paxos

- Mencius: multi-leader variant for improved throughput
- EPaxos (Egalitarian Paxos): all nodes can lead, eliminates single bottleneck
- Fast Paxos: reduces latency to 2 round trips in optimal case
- Raft: more understandable alternative with similar guarantees
- Vertical Paxos: dynamic reconfiguration of acceptor sets
- Trade-offs between latency, throughput, complexity, and fault tolerance

## Slide 11: Question for You

Jak osiągnąć konsensus w środowisku, w którym nie możemy ufać części uczestników?

(How to achieve consensus in an environment where we cannot trust some participants?)
