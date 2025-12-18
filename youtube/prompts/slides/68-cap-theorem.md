Generate 11 presentation slides based on the podcast about CAP Theorem.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: CAP Theorem - The Fundamental Tradeoff

- Consistency, Availability, Partition Tolerance - only 2 of 3 achievable simultaneously
- Network partitions are inevitable in distributed systems, making partition tolerance non-negotiable
- Forces choice between consistency (C) or availability (A) during network failures
- Published by Eric Brewer, became a foundational principle in distributed systems design

## Slide 2: Consistency (C) - One Source of Truth

- Every read returns the most recent write, guaranteed
- All nodes see identical data at the same moment globally
- Users in Warsaw, New York, and Tokyo see the exact same state
- Like a single magical bulletin board - everyone sees identical information instantly

## Slide 3: Availability (A) - Always Responding

- System always responds to requests, never returns errors
- Every request receives a response, even without guarantee of most recent data
- Like having local copies of data - always accessible but potentially stale
- Prioritizes service continuity over data freshness

## Slide 4: Partition Tolerance (P) - Surviving Network Failures

- System continues operating despite communication breakdown between nodes
- Handles severed undersea cables, router failures, network splits
- Both partitioned sections continue functioning independently
- Not optional in real-world distributed systems - failures are inevitable, not possible

## Slide 5: CP Systems - Consistency Over Availability

- When network partitions occur, system refuses operations to prevent inconsistency
- Returns "temporarily unavailable" errors rather than risk serving stale data
- Example: Flight reservation system blocks bookings during network split to prevent double-booking
- Better to reject requests than provide incorrect information

## Slide 6: AP Systems - Availability Over Consistency

- Continues accepting operations during network partitions, risking temporary inconsistencies
- Both regions operate independently, potential for conflicting updates
- Relies on Eventual Consistency - conflicts resolved after partition heals
- Cost of handling rare conflicts lower than unavailability for thousands of users

## Slide 7: Real-World Examples - Banking vs Social Media

- **CP Systems:** Banking, stock trading, air traffic control - correctness is critical
- **AP Systems:** Facebook, Instagram, e-commerce - availability paramount
- Banks: prefer temporary downtime over incorrect account balances
- Social media: second delay in showing likes acceptable, 15-minute outage catastrophic
- Same e-commerce site may use AP for browsing, CP for payment processing

## Slide 8: ACID vs BASE - Two Philosophies

- **ACID:** Traditional databases - absolute consistency guarantees
- **BASE:** Distributed systems approach for AP systems
- **Basically Available:** system always operational
- **Soft state:** accept that system state changes over time
- **Eventually consistent:** guarantee synchronization happens eventually, not immediately

## Slide 9: Beyond Binary Choice - Spectrum of Tradeoffs

- Real systems balance between consistency and availability, not purely binary
- Different operations within same system have different guarantees
- E-commerce: product browsing uses AP model, payment checkout uses CP model
- Tradeoff exists even without failures - during normal operation

## Slide 10: PACELC - Evolution of CAP

- Extends CAP theorem with behavior during normal operation (no partition)
- **If Partition:** choose between Availability and Consistency (CAP)
- **Else (no partition):** choose between Latency and Consistency
- Fast response with potentially stale data vs slower response with guaranteed consistency
- Shows tradeoffs are omnipresent, not just during failures

## Slide 11: Question for You

Która z tych kompromisów - absolutna poprawność czy nieprzerwane działanie - jest tak naprawdę ważniejszy w usługach, od których jesteśmy coraz bardziej zależni?
