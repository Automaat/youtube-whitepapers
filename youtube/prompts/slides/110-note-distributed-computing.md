Generate 11 presentation slides based on the podcast about "A Note on Distributed Computing".

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Unified Objects Fallacy

- The vision: local and remote objects should be used identically via unified programming model
- Central promise: distributed systems become as simple as single-process applications
- Major players: CORBA, Java RMI, DCOM - all built on this assumption
- The reality: this abstraction fundamentally breaks down in distributed environments

## Slide 2: Latency - The First Breaking Point

- Local call latency: nanoseconds (memory access)
- Remote call latency: milliseconds to seconds (network traversal)
- 4-5 orders of magnitude difference makes them fundamentally different operations
- Cannot hide network delays - application architecture must account for this

## Slide 3: Partial Failure - Networks Are Unreliable

- Local systems: process crashes or works
- Distributed systems: indefinite waiting, timeout uncertainty, partial responses
- Cannot distinguish between slow response, network failure, or remote crash
- Applications freeze waiting for responses that may never arrive

## Slide 4: Memory Access Semantics Break Down

- Local objects: pass by reference, direct memory pointers
- Remote objects: must serialize, deep copy entire object graphs
- Shared memory assumptions fail - modifications aren't automatically synchronized
- Performance implications: serialization overhead dwarfs actual computation

## Slide 5: Indistinguishable Failures

- From client perspective: network timeout looks identical to server crash
- No way to determine actual failure cause without additional infrastructure
- Traditional error handling patterns don't apply
- Requires fundamentally different failure handling strategies

## Slide 6: Concurrency Complexity Multiplies

- Local concurrency: threads, locks, shared memory within single address space
- Distributed concurrency: network partitions, clock skew, ordering ambiguities
- Race conditions become distributed coordination problems
- Debugging becomes orders of magnitude harder across process boundaries

## Slide 7: Real-World Casualties - Sun's Experience

- Sun Microsystems learned these lessons painfully through NFS implementation
- Early NFS versions tried to hide distribution - resulted in poor reliability
- Applications hung indefinitely on network issues
- Led to fundamental rethinking of distributed system APIs

## Slide 8: The "Server Disappeared" Error Pattern

- New error category: server was available, then vanished mid-operation
- Doesn't exist in local programming - processes don't partially disappear
- Requires explicit handling in application logic
- Cannot be abstracted away by infrastructure

## Slide 9: Objects Are Not Distributed - Proof by Counter-Example

- Paper demonstrates unified object model is mathematically impossible
- Different failure modes require different interfaces
- Latency differences demand different calling patterns
- Abstraction leaks at every level

## Slide 10: Separate Interfaces for Local vs Remote

- Local code: simple, direct method calls with familiar error handling
- Remote code: explicit network awareness, timeout handling, retry logic, partial failure management
- Accept the difference rather than hide it
- Design APIs that acknowledge and embrace distributed nature

## Slide 11: Question for You

And do we proudly call our patches for problems "Resilience Patterns"?
