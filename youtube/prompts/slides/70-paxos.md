Generate 11 presentation slides based on the podcast about "The Part-Time Parliament" by Leslie Lamport (Paxos algorithm).

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Consensus Problem

- Distributed servers need to agree on shared state despite failures
- Servers can crash, lose network connectivity, or restart unexpectedly
- Must maintain consistency: no conflicting data across replicas
- Must ensure progress: system cannot halt when stable quorum exists
- The Part-Time Parliament presents this as Greek island allegory with merchants as legislators
- Paxos protocol was one of first practical solutions enabling modern cloud infrastructure

## Slide 2: The Parliament Allegory and Core Challenge

- Part-time legislators (servers) constantly entering/leaving chamber (availability issues)
- Decrees (commands) must be recorded in identical order across all ledgers (state machines)
- Example failure: Decree 37 passed twice with conflicting content
- Two fundamental properties required: consistency (no conflicting entries) and progress (decisions eventually made)
- Ledgers represent distributed database state
- Problem: achieving agreement without central coordinator

## Slide 3: The Synod - Single Value Consensus

- Synod: process for agreeing on single decree value
- Two-phase protocol based on numbered ballots with unique, increasing numbers
- Each ballot attempt has higher number than all previous attempts
- Phase 1 (Prepare): reserve right to propose with ballot number B
- Phase 2 (Accept): actually propose and vote on decree value
- Foundation for State Machine Replication pattern

## Slide 4: Phase 1 - Prepare (Reservation)

- Proposer (president) selects new ballot number B higher than any seen before
- Sends NextBallot(B) message to all legislators: "planning ballot B, any objections?"
- Legislators receiving NextBallot(B) check if B is highest they've seen
- If yes, they promise not to participate in any lower-numbered ballots
- Critically: legislators respond with LastVote info if they previously voted
- Analogy: reserving conference room while informing about previous meeting decisions

## Slide 5: Phase 2 - Accept (Voting)

- President must collect promises from majority (quorum) before proceeding
- If any quorum member previously voted, president MUST propose that same value (highest ballot number)
- This ensures consistency: once-decided values cannot be overwritten
- If no prior votes exist, president can propose their own value
- President sends BeginBallot(B, D) with decree D to all legislators
- When quorum votes, decree is officially adopted

## Slide 6: Multi-Paxos - Sequence of Decrees

- Single synod handles one decree - need sequence for full ledger
- Solution: run independent Paxos instance for each decree number
- Optimization: president can execute Phase 1 for range of future decrees (100-200)
- After reservation, each decree requires only fast Phase 2
- Gaps in sequence filled with no-op decrees (e.g., "olive day becomes national holiday")
- Enables State Machine Replication: all servers execute same commands in same order

## Slide 7: Multiple Presidents Problem

- What if two proposers compete with conflicting values for same decree?
- Numbered ballots prevent inconsistency: only one proposal can win quorum
- But can kill progress: infinite war of escalating ballot numbers
- System becomes live-locked, making no forward progress
- Practical implementations require Leader Election mechanism
- Only one active leader at a time ensures both safety and liveness

## Slide 8: Ledger Growth and Snapshots

- After years, ledgers contain thousands of decrees - inefficient to read entire history
- Solution: periodic snapshots (checkpoints) of current legal state
- Consolidated law book captures all effective decrees at point in time
- New legislators can start from latest snapshot instead of full history
- Reduces storage and speeds up recovery from failures
- Standard practice in modern distributed databases

## Slide 9: Leases - Time-Bounded Authority

- Cheese Inspector example: decree appoints Dijkstra, later replaced by Gouda
- If Dijkstra doesn't learn of replacement, two inspectors issue conflicting certificates
- Classic exclusive resource access problem in distributed systems
- Solution: leases - grant authority for limited time period (e.g., 3 months)
- Authority automatically expires unless renewed by parliament
- Guarantees eventual consistency even if message delivery fails

## Slide 10: Trust Model and Byzantine Faults

- Paxos assumes honest but forgetful participants
- Handles fail-stop failures: processes crash, messages lost, network partitions
- Does NOT handle Byzantine faults: malicious actors actively trying to deceive
- Legislators can be absent, lose messages, forget information, but never lie
- Byzantine fault tolerance requires significantly more complex protocols
- Different class of problems requiring different guarantees and higher overhead

## Slide 11: Question for You

Jak bezpiecznie zarządzać ewolucją takich systemów? Jak zmieniać zasady gry, skoro same te zmiany muszą być uzgodnione w ramach starych zasad?
