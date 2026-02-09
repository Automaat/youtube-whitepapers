Generate 11 presentation slides based on the podcast about On-the-Fly Garbage Collection.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Challenge of Concurrent Garbage Collection
- Traditional garbage collection requires stopping all application threads (stop-the-world)
- Early systems had dedicated garbage collectors that worked at night or on separate machines
- Real-time systems need continuous operation without pauses
- The paper introduces a solution for garbage collection that runs concurrently with the application

## Slide 2: The Mutator-Collector Problem
- The mutator (application) continuously modifies the memory graph
- The collector needs to identify and reclaim unreachable objects
- Traditional marking algorithms fail when pointers change during collection
- Race conditions can cause live objects to be incorrectly marked as garbage

## Slide 3: Key Innovation: Minimal Synchronization
- Uses only weak synchronization primitives (no locks or critical sections)
- Relies on atomic read and write operations for single memory words
- Avoids stopping the mutator threads entirely
- Enables true concurrent execution of collection and application

## Slide 4: The Marking Algorithm Challenge
- Standard DFS marking traverses the object graph to find reachable objects
- Mutator can redirect pointers during traversal, causing collector to miss objects
- Example: collector marks A, mutator changes A→B to A→C and B→C, collector misses C
- Need invariants to ensure no reachable objects are missed

## Slide 5: Three-Color Abstraction
- White: unvisited objects (potentially garbage)
- Gray: visited but not fully processed (frontier)
- Black: fully processed objects (confirmed reachable)
- Invariant: no black object can directly point to a white object
- Collector moves objects from white through gray to black

## Slide 6: Maintaining the Tricolor Invariant
- Mutator cooperation required when creating new pointers
- Two approaches: prevent black→white pointers or track gray→white pointers
- Write barriers intercept pointer updates to maintain invariant
- Different strategies trade off between mutator overhead and collector complexity

## Slide 7: The Dijkstra-Scholten-Steele Algorithm
- Uses a write barrier to shade objects gray when pointers are created
- If mutator stores pointer to white object in black object, shade target gray
- Ensures collector will revisit modified parts of object graph
- Provides strong correctness guarantees with acceptable performance overhead

## Slide 8: Memory Consistency and Atomicity
- Single-word atomic reads and writes are sufficient
- No need for expensive synchronization primitives
- Algorithm works correctly even with weak memory models
- Careful ordering of operations prevents race conditions

## Slide 9: Performance Implications
- Write barrier adds overhead to every pointer assignment
- Typical overhead: 10-20% slowdown of mutator
- Eliminates long pause times (milliseconds vs seconds)
- Trade-off: slightly slower overall execution for predictable response times

## Slide 10: Real-World Impact and Applications
- Influenced modern concurrent collectors in Java, .NET, and Go
- Critical for real-time systems, interactive applications, and large-scale services
- Enabled garbage collection in systems that couldn't tolerate pauses
- Foundation for incremental and generational collection techniques

## Slide 11: Question for You
Do we quietly rely on similar subtle synchronization invariants in our concurrent systems, hoping that an equally embarrassing bug won't blow up at the most unexpected moment?