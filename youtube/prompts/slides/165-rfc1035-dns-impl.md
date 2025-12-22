Generate 11 presentation slides based on the podcast about RFC 1035: Domain Names - Implementation and Specification.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: RFC 1035 - DNS Implementation Specification
- DNS as the practical implementation guide for the domain name system
- Follows RFC 1034's conceptual foundation with concrete technical details
- Published in 1987 by Paul Mockapetris at USC ISI
- Transforms the distributed hierarchical database concept into working code
- Defines resolver and name server behavior, message formats, and wire protocols

## Slide 2: The Performance Crisis That DNS Solved
- Original HOSTS.TXT system required downloading entire host list from central server
- Network bandwidth consumption grew exponentially with internet size
- Single point of failure at MIT's central repository
- DNS enabled distributed queries: ask only what you need, when you need it
- Caching mechanisms dramatically reduced redundant lookups across the network

## Slide 3: Resolver and Name Server Architecture
- Resolver: client-side component that initiates DNS queries on behalf of applications
- Name Server: responds to queries with authoritative or cached data
- Recursive resolution: resolver delegates full query resolution to name server
- Iterative resolution: name server returns referrals, resolver follows the chain
- Clear separation of concerns enables independent scaling and optimization

## Slide 4: DNS Resource Record Types and TTL
- Each entry in the global database has a Type field defining its purpose
- Time To Live (TTL): how long a record can be cached before re-querying
- A record: maps domain name to IPv4 address (the phonebook entry)
- MX record: mail exchange servers for email routing
- PTR record: reverse lookups from IP address to domain name

## Slide 5: Message Format and Wire Protocol
- Binary format with fixed header structure for efficient parsing
- Header contains query ID, flags, and section counts
- Four sections: Question, Answer, Authority, Additional
- UDP preferred for speed (port 53), TCP fallback for large responses
- Compression pointers reduce message size by eliminating repeated domain names

## Slide 6: Caching Strategy and Scalability
- Simple caching solution transformed DNS performance fundamentally
- Every resolver and name server caches responses according to TTL
- Reduces load on root servers and authoritative name servers exponentially
- Negative caching: remember that a record doesn't exist (prevents repeated failures)
- Distributed caching creates implicit content delivery network for name resolution

## Slide 7: Extension Mechanisms and Future-Proofing
- Class field allows multiple protocol families (IN for Internet, CH for Chaosnet)
- Type codes reserved for future record types beyond initial set
- QTYPE in queries can request all records or specific types
- Flexible design accommodated later additions: AAAA (IPv6), SRV, TXT, DNSSEC
- Extensibility without breaking existing implementations

## Slide 8: UDP vs TCP and Message Size Handling
- UDP maximum safe size: 512 bytes to avoid fragmentation
- If response exceeds limit, server sets truncation flag
- Truncation signals resolver to retry query over TCP connection
- TCP provides reliable delivery for large responses and zone transfers
- Trade-off: UDP speed for common queries, TCP reliability for edge cases

## Slide 9: The Key Insight: Hierarchical Delegation
- No single entity needs complete knowledge of entire namespace
- Each zone authority maintains only its portion of the tree
- Referrals guide resolvers from root to authoritative server through hierarchy
- Enables organic growth without central coordination bottlenecks
- Scales from thousands to billions of domains without architectural changes

## Slide 10: Pragmatic Design Philosophy
- RFC deliberately avoids mandating specific caching strategies
- Implementers given freedom to optimize for their use cases
- Robustness through simplicity: minimal required behavior, optional enhancements
- Emphasis on interoperability over prescriptive algorithms
- This flexibility enabled DNS to evolve for over 35 years

## Slide 11: Question for You
How does the hierarchical delegation model in DNS relate to modern security challenges like phishing and identity verification on the internet?
