Generate 11 presentation slides based on the podcast about RFC 4271: A Border Gateway Protocol 4 (BGP-4).

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: BGP-4 Introduction and Evolution
- BGP is the core routing protocol enabling global Internet connectivity
- RFC 4271 is the revised specification consolidating years of operational experience
- Replaced earlier BGP versions with improved mechanisms and clarifications
- Protocol operates between Autonomous Systems (AS) to exchange routing information
- Uses TCP port 179 for reliable, connection-oriented communication
- Foundation for Internet-scale routing and policy-based path selection

## Slide 2: Inter-AS Communication Fundamentals
- BGP enables data exchange between different autonomous systems
- Each AS has independent routing policies and administrative control
- Protocol handles path vector routing rather than distance vector
- Routers advertise reachability information for network prefixes
- IBGP (Internal BGP) used within AS, EBGP (External BGP) between AS
- Supports complex routing policies based on business relationships

## Slide 3: BGP Message Types and Protocol Operation
- OPEN message: initiates BGP session with capability negotiation
- UPDATE message: advertises new routes or withdraws unreachable routes
- KEEPALIVE message: maintains session and confirms OPEN acceptance
- NOTIFICATION message: reports errors and closes BGP connection
- All messages use TCP for reliable, ordered delivery
- State machine governs session establishment and maintenance

## Slide 4: Error Handling and Notification Mechanisms
- NOTIFICATION messages include error code and subcode for diagnostics
- Common errors: message header errors, OPEN message errors, UPDATE errors
- Protocol mandates connection closure after sending NOTIFICATION
- Finite state machine ensures proper error recovery
- Diagnostic data included in NOTIFICATION for troubleshooting
- Robust error handling critical for Internet stability

## Slide 5: Path Attributes and Route Information
- UPDATE messages carry path attributes describing route characteristics
- Well-known mandatory: ORIGIN, AS_PATH, NEXT_HOP
- Well-known discretionary: LOCAL_PREF, ATOMIC_AGGREGATE
- Optional transitive and non-transitive attributes for extended functionality
- Attributes enable sophisticated policy-based routing decisions
- BGP-4's extensible attribute system allowed Internet to scale effectively

## Slide 6: Decision Process - Attribute Priority
- LOCAL_PREF attribute: influences outbound traffic within AS
- Higher LOCAL_PREF values indicate more preferred routes
- Used for implementing routing policies within autonomous system
- AS_PATH length: shorter paths generally preferred
- ORIGIN: IGP preferred over EGP, EGP over INCOMPLETE
- MED (Multi-Exit Discriminator): influences inbound traffic between ASes

## Slide 7: Route Selection Algorithm
- BGP uses multi-step decision process for best path selection
- Continuous negotiation and evaluation of available routes
- Step-by-step comparison: LOCAL_PREF, AS_PATH length, ORIGIN, MED
- Tie-breaking rules ensure deterministic path selection
- Routers maintain routing information base (RIB) with all learned routes
- Only best path advertised to neighbors after selection

## Slide 8: Advanced Tie-Breaking Criteria
- If MED values equal, prefer EBGP-learned routes over IBGP
- Next preference: route with lowest IGP cost to NEXT_HOP
- Longer AS_PATH in some cases (policy-dependent routing)
- Router ID comparison as final tie-breaker
- Route aggregation and summarization impact path selection
- Complex scenarios require understanding full decision algorithm

## Slide 9: Policy Implementation and Route Filtering
- BGP enables granular control over route advertisement and acceptance
- Import/export policies filter routes based on attributes
- Prefer specific routes over aggregates when tie-breaking
- AS_PATH prepending used to influence path selection
- Community attributes enable route tagging and policy signaling
- BGP policies reflect business relationships and traffic engineering goals

## Slide 10: Internet Routing Dynamics
- Global Internet routing constantly evolves with policy changes
- BGP convergence time affects network stability
- Route flap damping prevents instability from propagating
- International routing diplomacy encoded in BGP configurations
- Protocol must balance scalability, policy flexibility, and stability
- RFC 4271 codified best practices from decades of operational experience

## Slide 11: Question for You
What should we do about it?
