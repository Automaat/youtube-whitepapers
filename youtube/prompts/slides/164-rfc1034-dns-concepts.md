Generate 11 presentation slides based on the podcast about RFC 1034: Domain Names - Concepts and Facilities.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Scalability Crisis of Early Internet

- Pre-DNS internet used centralized HOSTS.TXT file maintained by SRI-NIC
- Every hostname-to-IP mapping required manual file distribution across all machines
- Growing network created vicious cycle: more servers meant larger files and more frequent updates
- Single point of failure with no autonomy for local network administrators
- System fundamentally couldn't scale beyond a few hundred hosts

## Slide 2: Hierarchical Namespace Architecture

- Tree structure with root at top, branching down through top-level domains (TLDs)
- Domain hierarchy mirrors organizational structure: com, edu, gov, country codes
- Each level delegates authority to next level (decentralization by design)
- Labels separated by dots, read right-to-left for resolution (www.example.com → com → example → www)
- Enables distributed administration while maintaining global consistency

## Slide 3: Recursive vs Iterative Resolution

- Resolver initiates query by contacting local name server
- Recursive mode: server takes full responsibility, returns final answer or error
- Iterative mode: server returns referrals to next authoritative server down the chain
- Resolution path starts at root, follows referrals through TLD to authoritative server
- Client receives complete answer regardless of how many servers were consulted

## Slide 4: Design Philosophy and Flexibility

- Multiple protocol classes beyond Internet (IN): Chaos (CH), Hesiod (HS) for future networks
- System designed for networks that didn't exist yet in 1987
- Separation of namespace from implementation details (names vs addresses)
- Extensible record types allow new functionality without protocol changes
- Focus on long-term scalability over immediate convenience

## Slide 5: CNAME Records and Aliasing

- Canonical Name (CNAME) records create aliases pointing to true hostname
- One machine can have multiple names for different services or purposes
- CNAME resolution follows chain until reaching A record with actual IP address
- Enables service migration and load balancing without changing client configurations
- Critical for flexibility in distributed systems architecture

## Slide 6: Resource Records and Time-to-Live (TTL)

- Every DNS record includes TTL value specifying cache lifetime in seconds
- Record types: A (address), NS (name server), MX (mail exchange), SOA (start of authority)
- SOA record contains zone metadata: serial number, refresh interval, retry, expire
- TTL balances consistency vs performance: short TTL = fresh data, high load
- Cached records reduce query load by orders of magnitude

## Slide 7: Zone Transfers and Authority

- Zone = contiguous portion of namespace managed by single authority
- Primary name server holds master copy, secondary servers maintain replicas
- Zone transfer (AXFR) copies entire zone from primary to secondary
- Delegation records (NS) mark boundaries where authority transfers to child zones
- Authoritative answer flag indicates response came from zone owner, not cache

## Slide 8: Consistency Model and Update Propagation

- Serial number in SOA record tracks zone version (must increment with each change)
- Secondary servers poll primary based on SOA refresh interval (typically hours)
- If serial increased, secondary initiates zone transfer to get updates
- Retry interval determines how long secondary waits after failed refresh
- Expire interval sets maximum time secondary serves stale data before giving up

## Slide 9: Caching Strategy and Negative Responses

- Caching is mandatory for resolvers, optional for servers
- Negative caching: storing non-existence answers (NXDOMAIN) with TTL
- Cache reduces average query path from multiple hops to zero (cache hit)
- Stale data risk bounded by TTL duration
- Performance vs consistency tradeoff tunable per-zone via TTL policy

## Slide 10: Evolution Through Extensions

- Original RFC 1034/1035 designed for extensibility from start
- DNSSEC adds cryptographic signatures for authenticity and integrity
- IPv6 support via AAAA records without protocol changes
- Internationalized domain names (IDN) using Punycode encoding
- 40+ years of growth from thousands to billions of domains without architectural redesign

## Slide 11: Question for You

Are we building today's fundamental systems with the same foresight for decentralization and scalability from the start, learning from DNS lessons? Or are we once again creating centralized bottlenecks for convenience that will become tomorrow's scaling crisis?
