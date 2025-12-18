Generate 11 presentation slides based on the podcast about "Paxos Made Simple" by Leslie Lamport.

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

- Distributed consensus: agreement among untrusting computers in chaotic environment
- Three safety requirements from Lamport:
  - Only proposed values can be chosen (no invented values)
  - Exactly one value must be chosen (never split decisions)
  - No false victory announcements before actual decision
- Foundation for internet, global databases, cloud services that work despite server failures

## Slide 2: Paxos Roles - Proposers, Acceptors, Learners

- Proposer: initiates proposals, tries to convince the system
- Acceptor: committee member, listens and accepts/rejects proposals
- Learner: wants to know the final decision
- Single server can play all three roles simultaneously
- Decision requires majority of acceptors
- Role separation is a mental model for analysis

## Slide 3: System Assumptions

- Asynchronous network: messages arrive in any order with delays
- Messages can be lost or duplicated
- Processes can fail and restart at any time
- Non-Byzantine model: no malicious lying
- No single point of failure (multiple acceptors required)
- Challenge: how to choose one value in this chaos?

## Slide 4: The Problem with Simple Approaches

- Single acceptor = single point of failure (system stops if it crashes)
- Rule P1: "accept first proposal received" leads to deadlock
  - Half accepts A, half accepts B - no majority
  - If acceptor crashes, can't reconstruct if decision was made
- Acceptors must be able to change their mind (accept multiple proposals)
- But how to avoid total chaos if everyone keeps changing minds?

## Slide 5: Proposal Ordering - The First Breakthrough

- Each proposal gets unique, increasing number (not just value)
- Proposal = pair: (number, value)
- Acceptor can accept new proposal only if number is higher than previously accepted
- Introduces discipline: can change mind, but only for newer ideas
- Still doesn't prevent two conflicting decisions at different numbers
- Need stronger guarantee...

## Slide 6: Rule P2 - The Iron Law

- P2: If decision about value V was made, every future agreed proposal must also have value V
- Once decided, decision is final and irrevocable
- System has "no going back" principle
- Rest of algorithm enforces this one powerful rule
- Question: How does new proposer after failure know what was decided elsewhere?
- No central registry to consult!

## Slide 7: Phase 1 - Prepare (Reconnaissance and Blocking)

- Before sending value, proposer reserves right to make proposal
- Chooses new unique number N, sends to majority: "Promise to ignore lower numbers?"
- Critical question: "What was highest-numbered proposal you already accepted?"
- Acceptor responds if N is higher than last promise:
  - "I promise. Last thing I accepted was proposal M with value V"
  - Or just "I promise" if accepted nothing
- This is like reserving speaking time at podium

## Slide 8: Phase 2 - Accept (The Proposal with Inherited History)

- Proposer waits for promises from majority
- If any acceptor reported previously accepted value:
  - MUST abandon own idea
  - MUST use value from response with highest number
- If no previous values reported: free to propose original value
- Sends to all who promised: "Please accept proposal (N, V)"
- Acceptor accepts unless it promised higher number in meantime
- Inheritance mechanism guarantees consistency

## Slide 9: Liveness Problem - Live-lock

- Safety guaranteed, but what about progress?
- Classic problem: P1 finishes prepare with number 10
  - Before accept, P2 finishes prepare with 11
  - P1 blocked, restarts with 12, blocking P2
  - Digital duel: "After you" "No, after you" - infinite loop
- Solution: elect distinguished leader proposer
- Only leader initiates proposals for a time
- Leader election itself is consensus problem (FLP result)
- But: Paxos safety preserved even with multiple leaders thinking they rule!

## Slide 10: Replicated State Machine - Practical Application

- One agreed value = fundamental building block for massive systems
- Replicated state machine: multiple database server copies with identical state
- Use Paxos to agree on each operation in sequence
- Create log: position 1, 2, 3... each decided by Paxos instance
- Leader collects client requests, proposes in consecutive rounds
- If leader crashes: new leader reads log, continues from last agreed position
- Gap filling with no-op (no-operation) commands to maintain log continuity

## Slide 11: Question for You

Z czym polega ta przepaść między teoretyczną prostotą idei, a piekielną złożonością jej praktycznego wdrożenia? Jakie inne proste koncepcje w nauce czy technologii, które można wyjaśnić w pięć minut, kryją w sobie ogromną, ukrytą złożoność, gdy próbujemy je urzeczywistnić?
