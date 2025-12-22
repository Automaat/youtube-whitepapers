Generate 11 presentation slides based on the podcast about RFC 1112: Host Extensions for IP Multicasting.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to IP Multicasting
- RFC 1112 defines host extensions for IP multicasting support
- Published in 1989 as a foundational standard for one-to-many communication
- Introduces Internet Group Management Protocol (IGMP) for group membership
- Enables efficient network resource utilization for group communication
- Revolutionary shift from traditional unicast and broadcast paradigms

## Slide 2: The Problem with Unicast and Broadcast
- Unicast: one-to-one communication requiring N separate transmissions for N recipients
- Broadcast: sends to all hosts, overwhelming networks with irrelevant traffic
- Neither scales efficiently for group communication scenarios
- Multicast solves this by sending one copy to multiple interested receivers
- Significantly reduces bandwidth consumption and network load

## Slide 3: Multicast Communication Model
- One sender transmits to a multicast group address
- Only interested receivers join the group and receive traffic
- Network infrastructure replicates packets only where needed
- Uses Class D IP addresses (224.0.0.0 to 239.255.255.255)
- Maintains efficiency regardless of group size

## Slide 4: Reserved Multicast Address Ranges
- 224.0.0.0 to 224.0.0.255 reserved for well-known services
- 224.0.0.1: all hosts on local network segment
- 224.0.0.2: all routers on local network segment
- Immediate address space reservation shows protocol's importance
- Enables automatic service discovery and network coordination

## Slide 5: Use Cases and Applications
- Multimedia streaming and video conferencing
- Real-time data distribution (stock quotes, news feeds)
- Server discovery protocols and service announcements
- Distributed database synchronization
- Multiplayer online games and collaborative applications

## Slide 6: IGMP Protocol Overview
- Internet Group Management Protocol manages multicast group membership
- Hosts use IGMP to join and leave multicast groups
- Routers query hosts to discover active group members
- Two message types: membership queries and membership reports
- Simple yet effective protocol for group coordination

## Slide 7: IGMP Message Flow
- Router periodically sends membership query to 224.0.0.1 (all hosts)
- Hosts respond with reports listing their active multicast groups
- Hosts send unsolicited reports when joining new groups
- Silent leave mechanism: hosts simply stop responding
- Minimizes network overhead while maintaining accurate membership

## Slide 8: Time To Live (TTL) Scoping
- TTL field controls multicast packet propagation distance
- TTL thresholds define administrative boundaries
- Prevents accidental wide-area multicast flooding
- Enables hierarchical scoping: local, site-wide, regional, global
- Simple mechanism for controlling multicast reach

## Slide 9: Ethernet Multicast Address Mapping
- IP multicast addresses map to Ethernet multicast MAC addresses
- Lower 23 bits of IP address map to MAC address
- Mapping: 224.x.y.z → 01:00:5E:(x&0x7F):y:z
- 32:1 address ambiguity requires higher-level filtering
- Network interface cards filter unwanted multicast traffic

## Slide 10: Design Philosophy and Impact
- Elegant, minimal solution focusing on core functionality
- Explicitly left routing protocols for future standardization
- Enabled explosive growth of Internet multimedia services
- Foundation for modern streaming, IPTV, and real-time applications
- Demonstrates power of simple, well-designed protocols

## Slide 11: Question for You
How would modern cloud-native architectures change if IP multicast was fully supported across public clouds and wide-area networks?
