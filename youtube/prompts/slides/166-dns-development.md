Generate 11 presentation slides based on the podcast about the Development of the Domain Name System by Paul Mockapetris and Kevin Dunlap (1988).

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Internet's First Phone Book Crisis
- Early internet used single centralized text file called `host.txt`
- One person at SRI-NIC manually maintained addresses for entire network
- System worked perfectly for dozens of machines in the 1980s
- Catastrophic failure as network scaled to thousands of workstations
- Central bottleneck contradicted internet's inherently distributed nature
- Local universities and companies wanted autonomy over their own names

## Slide 2: Why Not Just Copy Existing Solutions?
- Advanced systems already existed like Xerox's Grapevine
- Grapevine relied on intensive data replication across all nodes
- Tightly coupled to specific Xerox architecture
- DNS designers chose caching over replication for efficiency
- DARPA internet needed universal solution for heterogeneous systems
- Required something more flexible and architecture-independent

## Slide 3: Four Fundamental Design Goals
- Distributed management: end central dictator model completely
- Unlimited scalability: no hard-coded limits on growth
- Extensibility: ability to add new information types in future
- Acceptable performance: system must be fast enough for users
- These goals shaped architecture that survives 40+ years later

## Slide 4: Two-Part Architecture Revolution
- Nameservers: distributed database repositories holding zone information
- Resolvers: client-side programs that query nameservers intelligently
- True innovation was variable depth hierarchy organizing data
- Tree structure mirrors postal address system (country→city→street)
- Zone delegation mechanism enables distributed control
- Each organization manages autonomous database fragment

## Slide 5: Caching and Time-to-Live (TTL)
- Resolvers store answers in local memory cache
- Like local mailman remembering frequently requested addresses
- TTL value determines how long to remember each answer
- Zone administrators set TTL based on data stability
- Prevents overwhelming servers with repeated identical queries
- Critical for performance in unreliable network conditions

## Slide 6: Brutal Reality of 1980s Network Performance
- Designers assumed reasonably functional network infrastructure
- Reality: massive packet loss and unimaginable delays
- Servers prepared answers in <100ms but responses took 500ms-60 seconds
- 60 seconds to translate name to address (vs 3 seconds today)
- Aggressive caching became survival requirement, not optimization
- UDP datagrams chosen over TCP to reduce connection overhead

## Slide 7: The Negative Query Tsunami
- Designers expected most queries for existing valid names
- Reality: 20-60% of root server traffic queried non-existent domains
- Caused by legacy software and helpful "search lists" feature
- Single typo generated avalanche of invalid queries
- Innocent helpful feature accidentally DDoS attacked root servers
- Solution: negative caching (remember that something doesn't exist)

## Slide 8: Brilliant Optimizations That Worked
- Variable depth hierarchy proved perfect for organizations of any size
- Enabled wrapping other naming systems inside DNS structure
- Additional Section Processing: predict client's next query
- Example: MX record query includes IP addresses preemptively
- Saved entire communication round-trip for related queries
- Reduced total DNS network traffic by approximately 50%

## Slide 9: Painful Human Lessons Learned
- Distributed control ≠ distributed knowledge or competence
- Like giving power plant keys without operating manual
- Documentation explained multi-day TTL for stable servers
- Simple example used 1-hour TTL for clarity
- Everyone copied the example, ignored the explanation text
- Brutal truth: people only read examples, not documentation

## Slide 10: Social Challenges vs Technical Capabilities
- Adding new record types technically trivial in DNS software
- Practically extremely difficult due to political consensus requirements
- Must convince thousands of diverse stakeholders on exact meaning
- Example: MX records for email required massive coordination effort
- Should have required administrators to demonstrate working redundancy
- Trusted paper assurances too much instead of verifying configurations

## Slide 11: Question for You
If a next-generation global identity system with completely different philosophy attempted to wrap DNS inside itself (reversing history), which of these brilliant 1980s design principles would survive the test, and which would need to be reinvented?
