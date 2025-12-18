Generate 11 presentation slides based on the podcast about "CAP Theorem Twelve Years Later: How the 'Rules' Have Changed" by Eric Brewer.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The CAP Theorem Foundation

- **C (Consistency)**: All users see identical data at any moment - every read returns the most recent write
- **A (Availability)**: System always responds to requests (read/write) without errors, 24/7 operation guarantee
- **P (Partition Tolerance)**: System continues operating despite network splits between servers
- Classic interpretation: "Choose 2 out of 3" - if network partition occurs, pick either C or A
- This binary choice shaped Internet architecture for over a decade

## Slide 2: From ACID to BASE - The NoSQL Revolution

- **ACID world** (traditional databases): Atomicity, Consistency, Isolation, Durability - strict consistency as sacred principle
- **BASE philosophy** (NoSQL movement): Basically Available, Soft state, Eventually consistent
- CAP Theorem provoked shift from strict consistency to availability-first architectures
- Systems like Amazon DynamoDB, Cassandra emerged favoring A over C
- The pendulum swung too far - oversimplification led to misunderstandings

## Slide 3: Eric Brewer's 2012 Clarification - "Wait, Hold On"

- 12 years after original theorem, Brewer published essay explaining the evolution
- **Key insight**: CAP is not a tragic "2 out of 3" binary choice
- Real systems exist on a **spectrum of shades** - from strict linearizability to eventual consistency
- Modern approach: **adjust the sliders dynamically** rather than making permanent architectural choice
- Goal: balance consistency and availability instead of sacrificing one completely

## Slide 4: Active Partition Management

- **Two operational modes**: Normal mode vs. Partition mode (emergency state)
- System must **detect partitions** (typically via timeouts when servers don't respond)
- In partition mode, system explicitly decides: prioritize C or A for this specific operation
- **After partition heals**: activate recovery mechanisms to restore full consistency
- This is engineering challenge, not just technology selection

## Slide 5: Granular Consistency - Not All Data Is Equal

- **Different consistency levels** for different data types and operations:
  - Critical operations (privacy settings, financial transactions): Route to single source of truth, sacrifice low latency
  - Non-critical reads (profile views, recommendations): Serve from local replicas, eventual consistency acceptable
- **Context matters**: Same data may require different consistency based on user action
- Netflix example: Viewing your own queue vs. someone else viewing recommendations

## Slide 6: Version Vectors - Tracking Concurrent Changes

- When partition heals, how to identify which version is correct?
- **Version vectors**: Like document version numbering when multiple people collaborate
- Each server maintains vector tracking updates from all other servers
- On merge: System compares vectors to detect conflicts
- If vectors show concurrent modifications to same object, explicit conflict resolution needed

## Slide 7: CRDTs - Conflict-Free Replicated Data Types

- **Amazon shopping cart example**: User on phone adds item A, on laptop removes item B during partition
- Traditional approach: Pick one version, lose other changes
- **CRDT strategy**: Treat cart as two separate sets - "items added" and "items removed"
- Both sets only grow (never shrink), making them mathematically mergeable
- Final cart = (union of all adds) - (union of all removes)
- Guarantees no lost additions, predictable merge behavior

## Slide 8: ATM Case Study - Compensation Strategies

- ATMs often operate in partition mode (offline from central bank system)
- **Choice**: Maximize availability - allow cash withdrawals even when disconnected
- **Risk**: Account balance may go negative during partition
- **Compensation mechanism**: When connection restored, system detects violation and applies overdraft fees
- Design question: Which invariants are unbreakable vs. which can be temporarily violated?

## Slide 9: System Invariants vs. Flexible Rules

- **Invariants**: Rules that MUST NEVER be violated under any circumstances
  - Example: Bank account cannot go negative without overdraft protection/fees
  - These define the core business logic boundaries
- **Flexible rules**: Can be temporarily bent during partitions
  - Must design explicit compensation/recovery scenarios
  - Example: Shopping cart consistency, like counts, recommendation freshness
- Engineers must deeply understand business logic to classify correctly

## Slide 10: Modern Engineering - Planning for Failure

- **False hope**: "Just pick AP technology and hope it works out" - recipe for disaster
- **Real engineering**: Design recovery and compensation mechanisms from day one
- **Eventual consistency acceptance**: What temporary inconsistencies are acceptable in our digital life?
- Building resilient, scalable systems means explicitly planning what happens when things go wrong
- True engineering starts where we plan for failure scenarios, not just happy paths

## Slide 11: Question for You

What would have to happen for a system you use to commit an error that truly, absolutely could not be compensated for in any way?
