Generate 11 presentation slides based on the podcast about RFC 4301 - IPsec Security Architecture.

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: IPsec - Securing the Internet Protocol
- Network-layer security protocol protecting entire IP infrastructure
- Provides confidentiality, authentication, and integrity for IP packets
- Operates transparently below transport layer (TCP/UDP)
- Standardized by IETF in RFC 4301 as fundamental internet security protocol

## Slide 2: Core Security Services
- Authentication - verifying sender identity and packet integrity
- Confidentiality - encrypting payload to prevent eavesdropping
- Replay protection - defending against packet replay attacks
- Access control - enforcing security policies at network boundaries

## Slide 3: IPsec Architecture Components
- Security Policy Database (SPD) - defines which traffic requires protection
- Security Association Database (SAD) - stores active security parameters
- Peer Authorization Database (PAD) - manages trusted peer relationships
- Two main protocols: AH (Authentication Header) and ESP (Encapsulating Security Payload)

## Slide 4: Authentication Header (AH)
- Provides authentication and integrity without encryption
- Protects entire IP packet including immutable header fields
- Suitable when confidentiality not required (e.g., internal networks)
- Guarantees sender authenticity and detects tampering

## Slide 5: Encapsulating Security Payload (ESP)
- Encrypts payload while providing optional authentication
- Protects transport-layer data from inspection
- Flexible authentication modes - payload-only or full packet
- Most commonly used IPsec protocol for VPN connections

## Slide 6: Transport vs Tunnel Mode
- Transport mode - protects payload only, original IP headers visible
- Tunnel mode - encapsulates entire IP packet in new encrypted packet
- Transport mode for end-to-end host protection
- Tunnel mode for gateway-to-gateway VPN connections

## Slide 7: Security Policy Database (SPD)
- Defines rules for traffic processing: protect, bypass, or discard
- Matches traffic by selectors: IP addresses, ports, protocols
- Determines which SA to use or when to establish new one
- Critical decision point for all inbound and outbound packets

## Slide 8: Security Association (SA)
- Unidirectional connection with negotiated security parameters
- Specifies protocol (AH/ESP), mode (transport/tunnel), encryption algorithm
- Bidirectional communication requires two SAs (one per direction)
- Uniquely identified by SPI (Security Parameter Index), destination IP, and protocol

## Slide 9: IPsec as Modular Architecture
- Not a monolithic protocol but a flexible framework
- Separates policy (SPD), key management (IKE), and data protection (AH/ESP)
- Allows algorithm negotiation and cryptographic agility
- Extensible design accommodating new security mechanisms

## Slide 10: Key Management and IKE
- Internet Key Exchange (IKE) protocol establishes and maintains SAs
- Automates cryptographic key negotiation between peers
- Supports dynamic SA creation based on traffic needs
- Works with PAD to authenticate peers and verify authorization

## Slide 11: Question for You
Can you have the strongest lock in the world, but what good is it if the wall around it is made of paper?
