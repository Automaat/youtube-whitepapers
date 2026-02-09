Generate 11 presentation slides based on the podcast about RFC 8200 - Internet Protocol Version 6 Specification.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: IPv6 Specification Overview
- RFC 8200 standardizes Internet Protocol version 6
- Addresses IPv4 address exhaustion with 128-bit addresses
- Simplifies header structure compared to IPv4
- Removes unnecessary complexity from IPv4 design
- Core protocol for modern internet infrastructure
- Published by IETF as Internet Standard

## Slide 2: Design Philosophy - Fix IPv4 Mistakes
- IPv4 philosophy: "handle everything at network layer"
- IPv6 shifts complexity to end hosts (end-to-end principle)
- Routers perform minimal processing for better performance
- Remove features that proved problematic in practice
- Cleaner separation of concerns between layers
- Focus on essential routing functionality only

## Slide 3: Simplified Header Structure
- Fixed 40-byte header (vs variable-length IPv4)
- Removed header checksum for performance
- No fragmentation at intermediate routers
- Extension headers replace IPv4 options
- Streamlined processing pipeline
- Faster forwarding in network devices

## Slide 4: Fragmentation Handling
- Path MTU Discovery required for fragmentation
- Only source host can fragment packets
- Routers send ICMPv6 "Packet Too Big" messages
- Minimum MTU of 1280 bytes guaranteed
- Eliminates router fragmentation overhead
- Host responsible for finding optimal packet size

## Slide 5: Flow Label Field
- 20-bit field for traffic flow identification
- Enables quality of service (QoS) handling
- Routers can identify packet streams efficiently
- Useful for real-time traffic prioritization
- Host sets flow label, routers use it
- Alternative to examining transport headers

## Slide 6: Extension Headers Architecture
- Next Header field chains multiple headers
- Routing, fragmentation, authentication headers
- Hop-by-Hop Options for all routers
- Destination Options for end host only
- Processed in strict order
- Flexible extensibility mechanism

## Slide 7: Hop Limit vs Time To Live
- Replaces IPv4's TTL field
- Strictly hop-based (not time-based)
- Decremented by 1 at each router
- Packet discarded when reaching zero
- ICMPv6 "Time Exceeded" message sent
- Prevents infinite routing loops

## Slide 8: Traffic Class Field
- 8-bit field for differentiated services
- Enables network traffic prioritization
- Compatible with DiffServ architecture
- Routers may use for queue management
- Supports real-time application needs
- Textbook example of end-to-end design

## Slide 9: Jumbograms and Payload Length
- Standard payload length: 16-bit field (64KB)
- Jumbogram extension: packets up to 4GB
- Hop-by-Hop Options header for jumbo payloads
- Useful for high-performance computing
- Requires network path support
- Not commonly used in practice

## Slide 10: Security and Attack Mitigation
- Removed source routing (known attack vector)
- Extension headers processed in order
- ICMPv6 rate limiting prevents amplification
- Path MTU Discovery potential vulnerability
- Hop-by-Hop options security concerns
- Community attempts to limit certain features

## Slide 11: Question for You
Why does the engineering community now try to limit the use of features they originally designed into IPv6?
