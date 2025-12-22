Generate 11 presentation slides based on the podcast about the Mirai botnet.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Mirai Botnet - IoT's Dark Army

- First major botnet targeting IoT devices exclusively
- Infected hundreds of thousands of routers, cameras, DVRs
- Launched record-breaking DDoS attacks in 2016
- Source code released publicly, spawning countless variants
- Demonstrated catastrophic security failures in IoT ecosystem

## Slide 2: Infection Strategy - Brutal Simplicity

- Scanned entire IPv4 address space for open Telnet ports (23, 2323)
- Used dictionary of 62 default username/password combinations
- Targeted manufacturers who shipped devices with hardcoded credentials
- No sophisticated exploits needed - just brute force authentication
- Infection spread exponentially once device compromised

## Slide 3: Default Credentials - The 62 Keys to Chaos

- Database of factory-default login combinations
- Manufacturers reused same credentials across product lines
- admin/admin, root/root, support/support variations
- Devices shipped with no password change enforcement
- Single credential list unlocked diverse IoT device types

## Slide 4: Self-Defense Mechanisms

- Closed Telnet ports immediately after successful infection
- Prevented competing botnets from reinfecting same device
- Terminated processes from known rival malware families
- Claimed exclusive control over compromised resources
- Created temporary monopoly on infected device population

## Slide 5: Exponential Growth - Doubling Every 76 Minutes

- Initial infection spread tracked by security researchers
- Botnet size doubled approximately every 76 minutes
- Peak estimates: 300,000 to 600,000 infected devices
- Growth only limited by available vulnerable device population
- Network scanning generated massive Internet background noise

## Slide 6: DDoS Attack Arsenal - 10 Flood Techniques

- Specialized attacks optimized for different target types
- GRE flood: devastated router infrastructure
- TCP SYN flood, ACK flood, UDP flood variations
- DNS amplification attacks leveraging open resolvers
- HTTP flood for application-layer overload
- Custom protocols tailored to maximize damage

## Slide 7: Target: Dyn DNS - Internet Disruption

- October 21, 2016 attack on Dyn DNS provider
- Peak traffic: 1.2 Tbps, largest DDoS attack recorded at the time
- Disrupted major sites: Twitter, Netflix, Reddit, GitHub, Airbnb
- Demonstrated critical infrastructure vulnerability
- Exposed single points of failure in DNS ecosystem

## Slide 8: Research Analysis - Reverse Engineering Success

- Security researchers analyzed captured Mirai samples
- Mapped command-and-control server communication protocols
- Identified telemetry data sent from infected devices
- Documented attack command structure and parameters
- Published findings enabling defensive countermeasures

## Slide 9: Attribution and Aftermath

- Source code released on HackForums in October 2016
- FBI investigation traced operators through operational security failures
- Anna-senpai persona linked to real-world identity
- Conviction led to collaboration with FBI on cybercrime investigations
- Code release spawned ecosystem of Mirai variants

## Slide 10: The IoT Security Crisis

- Market saturation with fundamentally insecure devices
- Manufacturers prioritized cost over security engineering
- No firmware update mechanisms in many devices
- Consumer awareness of IoT risks nearly nonexistent
- Regulatory frameworks lagged behind technological deployment

## Slide 11: Question for You

Are we unknowingly building an even larger and more powerful army for Mirai's successor?
