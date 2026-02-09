Generate 11 presentation slides based on the podcast about Jim Gray's "Why Do Computers Stop and What Can Be Done About It?" (1985).

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The 90-Minute Mystery
- Jim Gray analyzed 2000+ failures in Tandem fault-tolerant systems (1985)
- Average system downtime: 90 minutes per failure (not just restart time)
- Detection delay: 3+ minutes before operators notice problems
- Diagnosis and recovery: majority of the time spent understanding what happened
- Key question: Why do supposedly fault-tolerant systems still fail?

## Slide 2: The Availability Formula
- Availability = MTBF / (MTBF + MTTR)
- MTBF (Mean Time Between Failures): How long until next failure
- MTTR (Mean Time To Repair): How long to recover
- Critical insight: Reducing MTTR to seconds is more impactful than extending MTBF
- Goal: Achieve 99.999% availability (5 minutes downtime per year)

## Slide 3: Hardware Redundancy Success
- Single disk MTBF: ~10,000 hours (just over 1 year)
- Mirrored disks with independent controllers: MTBF > 5,000 years
- Redundancy transforms hours into millennia of reliability
- Hardware failures accounted for only small fraction of system outages
- The real culprit wasn't hardware after all

## Slide 4: The Real Failure Distribution
- Software: 25% of all system failures
- Administration/operations: 42% (largest category)
- Hardware: Only 18% of failures
- Environment (power, cooling): 14%
- Maintenance operations: Single biggest source of outages

## Slide 5: Software Failure Patterns - Heisenbugs
- Bohrbug: Consistent, reproducible bugs (like Bohr atom model - predictable)
- Heisenbug: Intermittent bugs that disappear when investigated (like Heisenberg uncertainty)
- Most production bugs are Heisenbugs - occur only under specific timing/load
- Solution: Process restart often "fixes" Heisenbugs temporarily
- Implication: Quick restart more effective than debugging in production

## Slide 6: FailFast Module Design
- Module detects internal inconsistency → immediately stops execution
- Returns error to caller rather than continuing with corrupted state
- Enables rapid error detection and containment
- Prevents error propagation through system
- Foundation: "Fail cleanly rather than corrupt silently"

## Slide 7: Process Pairs Architecture
- Primary process handles all requests
- Backup process maintains synchronized state via checkpoints
- On primary failure, backup takes over in seconds
- Checkpoint frequency determines recovery point
- Used in all critical Tandem systems for instant failover

## Slide 8: Transactions as Recovery Mechanism
- Every operation wrapped in transaction boundaries
- System state always consistent at transaction boundaries
- After crash: roll back incomplete transactions
- Combines with process pairs for seamless recovery
- Makes complex recovery logic simple and predictable

## Slide 9: Human Error Prevention Strategies
- System should prevent dangerous operations (like formatting active disks)
- All maintenance operations must be reversible
- Automated consistency checks before critical operations
- Clear separation between development and production environments
- Design assumption: Operators will make mistakes

## Slide 10: Gray's Lasting Impact
- These principles from 1985 still foundation of modern systems
- Process pairs → Modern active-active replication
- Transactions → Distributed transactions and saga patterns
- FailFast → Circuit breakers and health checks
- Complexity remains the enemy: More abstraction layers haven't solved fundamental problems

## Slide 11: Question for You
Have we truly solved the human error and complexity problem, or have we merely buried it under layers of abstraction that are even harder to understand when something inevitably goes wrong?