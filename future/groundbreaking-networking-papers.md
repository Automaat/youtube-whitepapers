# 📡 Groundbreaking Networking Papers & Standards

**Date:** 2025-12-16
**Tags:** #research #networking #protocols #internet #standards
**Focus:** Chronological survey of foundational networking papers, RFCs, and standards

---

## 🎯 Overview

This document catalogs 60+ groundbreaking papers, RFCs, and standards that shaped computer networking from the 1960s to present day. Organized chronologically to show the evolution of networking technology.

---

## 📜 1960s - The Dawn of Networking

### 1. Queueing Theory for Packet Networks (1961-1964)

- **Author:** Leonard Kleinrock
- **Work:** PhD Thesis at MIT → Book "Communication Nets" (1964)
- **Impact:** 🔥 Mathematical foundation for packet switching; queueing theory models for network data flow
- **Connection:** [[Information Theory]], [[ARPANET]]

### 2. On Distributed Communications (1964)

- **Author:** Paul Baran
- **Publication:** RAND Corporation (11 volumes)
- **Impact:** 🔥 Proposed packet switching for robust military communications; introduced concept of distributed networks surviving nuclear attacks
- **Note:** Initially classified; rediscovered at ARPA later
- **Connection:** [[Cold War Technology]], [[ARPANET]]

### 3. Packet Switching Concept (1965-1966)

- **Author:** Donald Davies
- **Institution:** UK National Physical Laboratory
- **Impact:** 🔥 Coined term "packet switching"; independent invention from Baran; proposed 1965 design similar to later networks
- **Connection:** [[ARPANET]], [[Paul Baran]]

### 4. Towards a Cooperative Network of Time-Shared Computers (1966)

- **Authors:** Thomas Marill, Lawrence G. Roberts
- **Impact:** Early paper describing issues in forming computer networks
- **Connection:** [[ARPANET]]

---

## 📜 1970s - ARPANET & Protocol Foundations

### 5. RFC 1 - Host Software (1969)

- **Author:** Steve Crocker
- **Date:** April 7, 1969
- **Impact:** 🔥 First RFC ever; invented the RFC system for internet standards
- **Connection:** [[IETF]], [[Internet Governance]]

### 6. ARPANET IMP Documentation (1969-1970)

- **Institution:** BBN (Bolt, Beranek and Newman)
- **Impact:** First packet-switched network connecting 4 nodes (UCLA, SRI, UCSB, Utah)
- **Connection:** [[TCP/IP]], [[Packet Switching]]

### 7. A Protocol for Packet Network Intercommunication (1974)

- **Authors:** Vinton Cerf, Robert Kahn
- **Publication:** IEEE Transactions on Communications, May 1974
- **Impact:** 🔥🔥🔥 THE foundational TCP paper; introduced internetworking concepts; basis for TCP/IP
- **Link:** [IEEE](https://ieeemilestones.ethw.org/Milestone-Proposal:Transmission_Control_Protocol_(TCP)_and_the_Architecture_of_the_Internet,_1974)
- **Connection:** [[TCP/IP]], [[Internet Architecture]]

### 8. RFC 675 - Specification of Internet TCP (1974)

- **Author:** Vinton Cerf et al.
- **Date:** December 1974
- **Impact:** First detailed TCP specification
- **Connection:** [[TCP/IP]]

### 9. Ethernet: Distributed Packet Switching for Local Computer Networks (1976)

- **Authors:** Robert Metcalfe, David Boggs
- **Publication:** Communications of the ACM, July 1976
- **Impact:** 🔥🔥🔥 Invented Ethernet; introduced CSMA/CD; enabled LANs
- **Note:** Metcalfe received 2023 Turing Award for this work
- **Connection:** [[LAN]], [[IEEE 802.3]]

### 10. Time, Clocks, and the Ordering of Events in a Distributed System (1978)

- **Author:** Leslie Lamport
- **Publication:** Communications of the ACM, July 1978
- **Impact:** 🔥🔥 Logical clocks concept; foundational for distributed systems; Dijkstra Prize 2000
- **Connection:** [[Distributed Systems]], [[Consensus Protocols]]

---

## 📜 1980s - TCP/IP Standardization Era

### 11. RFC 791 - Internet Protocol (IP) (1981)

- **Author:** Jon Postel (editor)
- **Date:** September 1981
- **Impact:** 🔥🔥🔥 Defined IPv4; foundation of all internet communication
- **Link:** [RFC 791](https://datatracker.ietf.org/doc/html/rfc791)
- **Connection:** [[IPv4]], [[Routing]]

### 12. RFC 792 - Internet Control Message Protocol (ICMP) (1981)

- **Author:** Jon Postel
- **Impact:** 🔥 Defined ICMP; enables ping, traceroute; network diagnostics
- **Connection:** [[Network Diagnostics]], [[IPv4]]

### 13. RFC 793 - Transmission Control Protocol (TCP) (1981)

- **Author:** Jon Postel (editor)
- **Date:** September 1981
- **Impact:** 🔥🔥🔥 Official TCP standard; reliable transport; still used today
- **Link:** [RFC 793](https://datatracker.ietf.org/doc/html/rfc793)
- **Connection:** [[TCP/IP]], [[Congestion Control]]

### 14. RFC 826 - Address Resolution Protocol (ARP) (1982)

- **Author:** David Plummer
- **Impact:** 🔥 Maps IP to MAC addresses; essential for LAN communication
- **Connection:** [[Ethernet]], [[IPv4]]

### 15. RFC 821 - Simple Mail Transfer Protocol (SMTP) (1982)

- **Author:** Jonathan B. Postel
- **Date:** August 1982
- **Impact:** 🔥🔥 Standard for email transport; still foundation of email today
- **Link:** [RFC 821](https://datatracker.ietf.org/doc/html/rfc821)
- **Connection:** [[Email]], [[Application Protocols]]

### 16. RFC 822 - Standard for Internet Message Format (1982)

- **Author:** David Crocker
- **Impact:** 🔥 Defined email message format; headers, body structure
- **Connection:** [[Email]], [[SMTP]]

### 17. End-to-End Arguments in System Design (1984)

- **Authors:** J.H. Saltzer, D.P. Reed, D.D. Clark
- **Publication:** ACM TOCS, Vol. 2, No. 4, November 1984
- **Impact:** 🔥🔥🔥 Seminal design principle; functions belong at endpoints; shaped internet architecture philosophy
- **Link:** [MIT PDF](https://web.mit.edu/saltzer/www/publications/endtoend/endtoend.pdf)
- **Connection:** [[Internet Architecture]], [[Protocol Design]]

### 18. IEEE 802.3 - Ethernet Standard (1983)

- **Institution:** IEEE
- **Impact:** 🔥🔥 Standardized Ethernet; enabled interoperability
- **Connection:** [[LAN]], [[Ethernet]]

### 19. IEEE 802.5 - Token Ring (1984-1989)

- **Institution:** IBM/IEEE
- **Impact:** Alternative to Ethernet; popular in 1980s-90s enterprise networks
- **Connection:** [[LAN]], [[Legacy Networks]]

### 20. RFC 959 - File Transfer Protocol (FTP) (1985)

- **Authors:** J. Postel, J. Reynolds
- **Date:** October 1985
- **Impact:** 🔥 Canonical FTP specification; file transfer standard
- **Link:** [RFC 959](https://datatracker.ietf.org/doc/html/rfc959)
- **Connection:** [[Application Protocols]]

### 21. RFC 1034/1035 - Domain Name System (DNS) (1987)

- **Author:** Paul Mockapetris
- **Date:** November 1987
- **Impact:** 🔥🔥🔥 Invented DNS; hierarchical naming system; essential internet infrastructure
- **Link:** [RFC 1034](https://datatracker.ietf.org/doc/html/rfc1034), [RFC 1035](https://datatracker.ietf.org/doc/html/rfc1035)
- **Connection:** [[Internet Infrastructure]], [[Naming Systems]]

### 22. Development of the Domain Name System (1988)

- **Authors:** Paul Mockapetris, Kevin Dunlap
- **Publication:** SIGCOMM '88
- **Impact:** Academic paper describing DNS development and deployment
- **Link:** [Cornell PDF](https://www.cs.cornell.edu/courses/cs6411/2018sp/papers/mockapetris.pdf)
- **Connection:** [[DNS]]

### 23. The Design Philosophy of the DARPA Internet Protocols (1988)

- **Author:** David D. Clark
- **Publication:** SIGCOMM '88
- **Impact:** 🔥🔥🔥 Explains WHY internet protocols are designed as they are; design rationale document
- **Link:** [MIT PDF](https://web.mit.edu/6.033/www/papers/darpa.pdf)
- **Connection:** [[Internet Architecture]], [[TCP/IP]]

### 24. Congestion Avoidance and Control (1988)

- **Author:** Van Jacobson
- **Publication:** SIGCOMM '88
- **Impact:** 🔥🔥🔥 Introduced TCP congestion control algorithms; saved internet from congestion collapse
- **Connection:** [[TCP]], [[Congestion Control]]

### 25. RFC 1058 - Routing Information Protocol (RIP) (1988)

- **Author:** Charles Hedrick
- **Impact:** 🔥 First officially standardized routing protocol (unofficially used since 1970s)
- **Connection:** [[Routing]], [[Distance Vector]]

### 26. A Binary Feedback Scheme for Congestion Avoidance (1988)

- **Authors:** K.K. Ramakrishnan, Raj Jain
- **Publication:** SIGCOMM '88
- **Impact:** Congestion signaling mechanism; influenced ECN
- **Connection:** [[Congestion Control]]

### 27. Information Management: A Proposal (1989)

- **Author:** Tim Berners-Lee
- **Institution:** CERN
- **Impact:** 🔥🔥🔥 Proposed the World Wide Web; hypertext, URLs, HTTP concept
- **Connection:** [[WWW]], [[HTTP]]

### 28. Analysis and Simulation of a Fair Queueing Algorithm (1989)

- **Authors:** Alan Demers, Srinivasan Keshav, Scott Shenker
- **Publication:** SIGCOMM '89
- **Impact:** 🔥🔥 Introduced Fair Queueing (FQ); foundation for QoS
- **Connection:** [[QoS]], [[Traffic Management]]

### 29. RFC 1105 - Border Gateway Protocol (BGP) (1989)

- **Authors:** Kirk Lougheed, Yakov Rekhter
- **Date:** June 1989
- **Impact:** 🔥🔥🔥 First BGP specification; "two napkin protocol"; replaced EGP
- **Note:** Famously sketched on napkins at IETF conference
- **Connection:** [[Routing]], [[Internet Architecture]]

### 30. RFC 1131 - OSPF Specification (1989)

- **Author:** John Moy
- **Date:** October 1989
- **Impact:** 🔥🔥 Open Shortest Path First; link-state routing; replaced RIP in many deployments
- **Link:** [RFC 1131](https://datatracker.ietf.org/doc/rfc1131/)
- **Connection:** [[Routing]], [[Link-State]]

### 31. RFC 1112 - Host Extensions for IP Multicasting (1989)

- **Author:** Steve Deering
- **Impact:** 🔥 Defined IGMP; IP multicast foundation
- **Connection:** [[Multicast]], [[IGMP]]

---

## 📜 1990s - Web, Security & QoS Era

### 32. FDDI Standard (1990)

- **Institution:** ANSI X3T9.5
- **Impact:** 100 Mbps fiber optic LAN; dual ring for redundancy
- **Note:** Obsoleted by Fast Ethernet and Gigabit Ethernet
- **Connection:** [[LAN]], [[Legacy Networks]]

### 33. Multicast Routing in a Datagram Internetwork (1991)

- **Author:** Steve Deering
- **Publication:** PhD Thesis, Stanford
- **Impact:** 🔥🔥 Foundational IP multicast work; designed multicast service model
- **Connection:** [[Multicast]], [[Routing]]

### 34. On the Self-Similar Nature of Ethernet Traffic (1993)

- **Authors:** Will E. Leland, Murad S. Taqqu, Walter Willinger, Daniel V. Wilson
- **Publication:** SIGCOMM '93
- **Impact:** 🔥🔥 Proved network traffic is fractal/self-similar; challenged Poisson models; changed capacity planning
- **Connection:** [[Traffic Modeling]], [[Network Measurement]]

### 35. Random Early Detection Gateways for Congestion Avoidance (1993)

- **Authors:** Sally Floyd, Van Jacobson
- **Publication:** IEEE/ACM Transactions on Networking, August 1993
- **Impact:** 🔥🔥 Invented RED algorithm; Active Queue Management (AQM) foundation; "saved internet from collapse"
- **Link:** [Paper PDF](https://www.icir.org/floyd/papers/early.twocolumn.pdf)
- **Connection:** [[Congestion Control]], [[QoS]]

### 36. RFC 1633 - Integrated Services (IntServ) (1994)

- **Authors:** R. Braden, D. Clark, S. Shenker
- **Impact:** 🔥 First QoS architecture for IP; per-flow guarantees; RSVP resource reservation
- **Connection:** [[QoS]], [[RSVP]]

### 37. RFC 1631 - Network Address Translator (NAT) (1994)

- **Authors:** K. Egevang, P. Francis
- **Date:** May 1994
- **Impact:** 🔥🔥 Defined NAT; "short-term" solution that became permanent; extended IPv4 lifetime
- **Link:** [RFC 1631](https://www.rfc-editor.org/rfc/rfc1631)
- **Connection:** [[IPv4]], [[Address Exhaustion]]

### 38. SSL Protocol Version 2.0 (1995)

- **Institution:** Netscape
- **Impact:** 🔥 First web security protocol; enabled e-commerce (though later found insecure)
- **Connection:** [[Network Security]], [[TLS]]

### 39. SSL Protocol Version 3.0 (1996)

- **Authors:** Paul Kocher, Phil Karlton, Alan Freier
- **Impact:** 🔥🔥 Complete redesign of SSL; foundation for all TLS versions
- **Connection:** [[Network Security]], [[TLS]]

### 40. Active Networks (1996)

- **Authors:** David Tennenhouse, David Wetherall
- **Publication:** SIGCOMM CCR, 1996
- **Impact:** 🔥 Proposed programmable networks; precursor to SDN concepts
- **Connection:** [[SDN]], [[Programmable Networks]]

### 41. TCP Vegas: New Techniques for Congestion Detection and Avoidance (1995)

- **Authors:** Lawrence Brakmo, Larry Peterson
- **Publication:** IEEE JSAC
- **Impact:** 🔥 Delay-based congestion control; alternative to loss-based TCP
- **Connection:** [[TCP]], [[Congestion Control]]

### 42. RFC 1771 - BGP-4 (1995)

- **Authors:** Y. Rekhter, T. Li
- **Date:** March 1995
- **Impact:** 🔥🔥 Current BGP version; added CIDR support; route aggregation
- **Connection:** [[BGP]], [[Routing]]

### 43. RFC 1825-1829 - IPsec (1995)

- **Institution:** IETF
- **Impact:** 🔥🔥 First IPsec specifications; VPN foundation
- **Connection:** [[Network Security]], [[VPN]]

### 44. IEEE 802.11 Wireless LAN Standard (1997)

- **Institution:** IEEE
- **Impact:** 🔥🔥🔥 First WiFi standard; enabled wireless networking revolution
- **Connection:** [[Wireless]], [[WiFi]]

### 45. Anatomy of a Large-Scale Hypertext Web Search Engine (1998)

- **Authors:** Sergey Brin, Larry Page
- **Publication:** WWW Conference 1998
- **Impact:** 🔥🔥 PageRank algorithm; Google's foundation; revolutionized web search
- **Connection:** [[WWW]], [[Search Engines]]

### 46. RFC 2460 - IPv6 Specification (1998)

- **Authors:** S. Deering, R. Hinden
- **Date:** December 1998
- **Impact:** 🔥🔥 Defined IPv6; 128-bit addresses; long-term solution to address exhaustion
- **Link:** [RFC 2460](https://datatracker.ietf.org/doc/rfc2460/)
- **Connection:** [[IPv6]], [[Internet Evolution]]

### 47. RFC 2474/2475 - Differentiated Services (DiffServ) (1998)

- **Institution:** IETF
- **Impact:** 🔥 Scalable QoS architecture; per-hop behaviors; DSCP markings
- **Connection:** [[QoS]], [[Traffic Engineering]]

### 48. RFC 2246 - TLS 1.0 (1999)

- **Authors:** T. Dierks, C. Allen
- **Impact:** 🔥🔥 IETF-standardized SSL successor; foundation for secure web
- **Connection:** [[Network Security]], [[HTTPS]]

### 49. RFC 2131 - DHCP (1997)

- **Author:** R. Droms
- **Impact:** 🔥 Dynamic address assignment; essential network service
- **Connection:** [[Network Management]], [[IP Addressing]]

### 50. RFC 2616 - HTTP/1.1 (1999)

- **Authors:** Fielding et al.
- **Impact:** 🔥🔥 Definitive HTTP specification; persistent connections; chunked transfer
- **Connection:** [[WWW]], [[Application Protocols]]

---

## 📜 2000s - P2P, SDN & Modern Internet

### 51. Network Information Flow (2000)

- **Authors:** R. Ahlswede, N. Cai, S.-Y.R. Li, R.W. Yeung
- **Publication:** IEEE Trans. Inf. Theory, July 2000
- **Impact:** 🔥🔥 Founded network coding theory; max-flow min-cut for networks; "butterfly network"
- **Link:** [PDF](https://pdos.csail.mit.edu/archive/decouto/papers/ahlswede00.pdf)
- **Connection:** [[Network Coding]], [[Information Theory]]

### 52. Chord: A Scalable Peer-to-peer Lookup Service (2001)

- **Authors:** Ion Stoica et al.
- **Publication:** SIGCOMM 2001
- **Impact:** 🔥🔥 Distributed Hash Table (DHT); P2P foundation; O(log N) lookups
- **Connection:** [[P2P]], [[Distributed Systems]]

### 53. A Scalable Content-Addressable Network (CAN) (2001)

- **Authors:** Sylvia Ratnasamy et al.
- **Publication:** SIGCOMM 2001
- **Impact:** 🔥 DHT implementation; P2P infrastructure
- **Connection:** [[P2P]], [[DHT]]

### 54. Pastry: Scalable, Decentralized Object Location (2001)

- **Authors:** Antony Rowstron, Peter Druschel
- **Impact:** 🔥 DHT variant; prefix-based routing
- **Connection:** [[P2P]], [[DHT]]

### 55. RFC 3031 - MPLS Architecture (2001)

- **Authors:** E. Rosen, A. Viswanathan, R. Callon
- **Date:** January 2001
- **Impact:** 🔥🔥 Label switching for traffic engineering; VPNs; Layer 2.5 protocol
- **Link:** [RFC 3031](https://datatracker.ietf.org/doc/html/rfc3031)
- **Connection:** [[Traffic Engineering]], [[VPN]]

### 56. Kademlia: A Peer-to-peer Information System Based on XOR Metric (2002)

- **Authors:** Petar Maymounkov, David Mazières
- **Publication:** IPTPS 2002
- **Impact:** 🔥🔥 DHT with XOR distance metric; used by BitTorrent, IPFS
- **Connection:** [[P2P]], [[BitTorrent]]

### 57. A Study of Non-blocking Switching Networks (Clos Networks) (1953/2000s revival)

- **Author:** Charles Clos
- **Publication:** Bell System Technical Journal, 1953
- **Impact:** 🔥🔥 Multi-stage switching topology; revived for data center networks (Fat-tree, VL2)
- **Connection:** [[Data Center]], [[Network Topology]]

### 58. RFC 4271 - BGP-4 (Revised) (2006)

- **Authors:** Y. Rekhter, T. Li, S. Hares
- **Impact:** 🔥 Current BGP standard; refined from RFC 1771
- **Connection:** [[BGP]], [[Routing]]

### 59. RFC 4301 - IPsec Architecture (2005)

- **Authors:** S. Kent, K. Seo
- **Impact:** 🔥 Updated IPsec; "IPsec-v3"
- **Link:** [RFC 4301](https://datatracker.ietf.org/doc/html/rfc4301)
- **Connection:** [[Network Security]], [[VPN]]

### 60. OpenFlow: Enabling Innovation in Campus Networks (2008)

- **Authors:** Nick McKeown et al.
- **Publication:** ACM SIGCOMM CCR, April 2008
- **Impact:** 🔥🔥🔥 Launched SDN revolution; separation of control/data planes; Stanford Clean Slate
- **Connection:** [[SDN]], [[Network Programmability]]

### 61. A Scalable, Commodity Data Center Network Architecture (Fat-tree) (2008)

- **Authors:** Mohammad Al-Fares, Alexander Loukissas, Amin Vahdat
- **Publication:** SIGCOMM 2008
- **Impact:** 🔥🔥 Fat-tree topology for data centers; full bisection bandwidth with commodity switches
- **Connection:** [[Data Center]], [[Network Topology]]

### 62. VL2: A Scalable and Flexible Data Center Network (2009)

- **Authors:** Albert Greenberg et al. (Microsoft)
- **Publication:** SIGCOMM 2009
- **Impact:** 🔥🔥 Microsoft's data center network; Clos topology; Valiant load balancing
- **Link:** [PDF](https://web.eecs.umich.edu/~mosharaf/Readings/VL2.pdf)
- **Connection:** [[Data Center]], [[Cloud Computing]]

---

## 📜 2010s - Cloud, Mobile & Modern Protocols

### 63. The Akamai Network: A Platform for High-Performance Internet Applications (2010)

- **Authors:** Erik Nygren et al.
- **Publication:** ACM SIGOPS OSR, 2010
- **Impact:** 🔥 CDN architecture; edge computing; content delivery at scale
- **Link:** [ACM](https://dl.acm.org/doi/10.1145/1842733.1842736)
- **Connection:** [[CDN]], [[Edge Computing]]

### 64. CUBIC: A New TCP-Friendly High-Speed TCP Variant (2008)

- **Authors:** Sangtae Ha, Injong Rhee, Lisong Xu
- **Publication:** ACM SIGOPS OSR
- **Impact:** 🔥🔥 Default Linux TCP; cubic function for window growth; high bandwidth-delay product networks
- **Connection:** [[TCP]], [[Congestion Control]]

### 65. ETSI NFV White Paper (2012)

- **Institution:** ETSI ISG NFV
- **Impact:** 🔥🔥 Launched Network Functions Virtualization; software-based network functions
- **Link:** [ETSI NFV](https://portal.etsi.org/nfv/nfv_white_paper.pdf)
- **Connection:** [[NFV]], [[Virtualization]]

### 66. RFC 6550 - RPL: Routing Protocol for Low-Power Networks (2012)

- **Institution:** IETF
- **Impact:** 🔥 IoT routing protocol for constrained devices
- **Connection:** [[IoT]], [[6LoWPAN]]

### 67. RFC 7252 - CoAP: Constrained Application Protocol (2014)

- **Institution:** IETF CoRE WG
- **Impact:** 🔥 HTTP-like protocol for IoT; REST for constrained devices
- **Connection:** [[IoT]], [[Embedded Systems]]

### 68. Jupiter Rising: A Decade of Clos Topologies at Google (2015)

- **Authors:** Arjun Singh et al.
- **Publication:** SIGCOMM 2015
- **Impact:** 🔥🔥 Google's data center network evolution; centralized control at hyperscale
- **Connection:** [[Data Center]], [[Google]]

### 69. BBR: Congestion-Based Congestion Control (2016)

- **Authors:** Neal Cardwell et al. (Google)
- **Publication:** ACM Queue, 2016
- **Impact:** 🔥🔥 Model-based TCP; estimates bandwidth and RTT; deployed at Google/YouTube
- **Link:** [Semantic Scholar](https://www.semanticscholar.org/paper/BBR:-Congestion-Based-Congestion-Control-Cardwell-Cheng/46a3ac9ce82ed02eafb9616fabd102d50b1792bc)
- **Connection:** [[TCP]], [[Congestion Control]]

### 70. The QUIC Transport Protocol: Design and Internet-Scale Deployment (2017)

- **Authors:** Adam Langley et al. (Google)
- **Publication:** SIGCOMM 2017
- **Impact:** 🔥🔥🔥 UDP-based transport; 0-RTT connections; built-in TLS; foundation of HTTP/3
- **Link:** [Google Research](https://research.google/pubs/the-quic-transport-protocol-design-and-internet-scale-deployment/)
- **Connection:** [[Transport Protocols]], [[HTTP/3]]

### 71. RFC 8446 - TLS 1.3 (2018)

- **Author:** E. Rescorla
- **Impact:** 🔥🔥 Major TLS overhaul; 1-RTT handshake; removed weak ciphers; mandatory forward secrecy
- **Connection:** [[Network Security]], [[HTTPS]]

---

## 📜 2020s - HTTP/3, 5G & Beyond

### 72. RFC 9000 - QUIC (2021)

- **Institution:** IETF QUIC WG
- **Impact:** 🔥🔥 IETF-standardized QUIC; transport protocol of HTTP/3
- **Connection:** [[Transport Protocols]], [[HTTP/3]]

### 73. RFC 9114 - HTTP/3 (2022)

- **Institution:** IETF
- **Impact:** 🔥🔥 HTTP over QUIC; eliminates head-of-line blocking; next generation web protocol
- **Connection:** [[WWW]], [[HTTP]]

### 74. 3GPP Release 15-18 - 5G Standards (2018-present)

- **Institution:** 3GPP
- **Impact:** 🔥🔥 5G NR, network slicing, URLLC, mMTC; mobile broadband evolution
- **Link:** [3GPP](https://www.3gpp.org/technologies/5g-system-overview)
- **Connection:** [[Mobile Networks]], [[5G]]

### 75. RFC 8200 - IPv6 (Internet Standard) (2017)

- **Institution:** IETF
- **Impact:** 🔥 Elevated IPv6 to Internet Standard status (supersedes RFC 2460)
- **Connection:** [[IPv6]]

---

## 🔗 Connections & Themes

### Protocol Design Principles

- [[End-to-End Arguments]] - Functions at endpoints
- [[DARPA Design Philosophy]] - Survivability, heterogeneity
- [[Layered Architecture]] - OSI, TCP/IP models

### Evolution Patterns

- **IPv4 → NAT → IPv6** - Address space evolution
- **SSL → TLS 1.0 → TLS 1.3** - Security evolution
- **TCP → QUIC → HTTP/3** - Transport evolution
- **RIP → OSPF → BGP** - Routing evolution
- **Circuit → Packet → SDN** - Switching evolution

### Key Institutions

- **DARPA/ARPA** - Original internet funding
- **BBN** - Early implementation
- **Stanford** - SDN, many protocols
- **MIT** - Theoretical foundations
- **IETF** - Standards body
- **IEEE** - Ethernet, WiFi standards
- **3GPP** - Mobile standards

---

## 📚 Sources

- [Internet Society History](https://www.internetsociety.org/internet/history-internet/)
- [ACM Digital Library](https://dl.acm.org/)
- [IETF Datatracker](https://datatracker.ietf.org/)
- [IEEE Xplore](https://ieeexplore.ieee.org/)
- [RFC Editor](https://www.rfc-editor.org/)
- [CAIDA](https://www.caida.org/)
- [3GPP](https://www.3gpp.org/)
- [ETSI](https://www.etsi.org/)

---

## ❓ Questions for Further Research

- How will post-quantum cryptography affect TLS?
- What will 6G bring beyond 5G?
- Will QUIC fully replace TCP?
- How will satellite constellations (Starlink) change internet architecture?
- What's the future of network programmability beyond SDN?

---

**Suggested location:** 3_Resources/Technology/Networking/
**Potential MOCs:** [[Networking MOC]], [[Internet History MOC]], [[Protocol Design MOC]]
**Tags:** #networking #protocols #internet #standards #research #tcp-ip #routing #security
