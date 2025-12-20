Generate 11 presentation slides based on the podcast about Random Oracles.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Random Oracles

- Bridging theory and practice in cryptographic security proofs
- One-way functions: easy to compute forward, hard to reverse
- Hash functions like SHA-256 as practical implementations
- The challenge: proving security of real-world cryptographic protocols

## Slide 2: The Random Oracle Model

- Idealized hash function that returns truly random outputs
- Queries to the oracle produce uniformly random responses
- Same input always returns same output (deterministic property)
- Theoretical tool for security proofs, not real implementations

## Slide 3: Reconciling Theory and Practice

- Theory requires perfect randomness for proofs
- Practice uses deterministic hash functions (SHA-256, SHA-3)
- Random oracle methodology: prove security in idealized model
- Replace oracle with real hash function in implementation

## Slide 4: Three-Step Security Proof Process

- Step 1: Design cryptographic protocol using random oracle
- Step 2: Prove security under random oracle assumption
- Step 3: Replace oracle with practical hash function (e.g., SHA-256)
- Hope that security properties transfer to real implementation

## Slide 5: Why Practitioners Use Random Oracles

- Provides strong security guarantees in proofs
- Enables analysis of complex protocols (RSA-OAEP, signatures)
- Industry standard for protocols like RSA encryption
- Practical hash functions approximate oracle behavior well

## Slide 6: Non-Malleability Property

- Random oracle ensures non-malleability in protocols
- Attacker cannot modify ciphertext without detection
- Critical for preventing manipulation attacks
- SHA-based schemes inherit this property in practice

## Slide 7: Bellare-Rogaway Analysis

- Showed protocols secure under random oracle assumption
- If adversary cannot break random oracle version, real version is secure
- Groundbreaking work legitimizing random oracle methodology
- Foundation for modern cryptographic protocol design

## Slide 8: Attack Preparation Limitations

- Adversary cannot pre-compute attacks without oracle access
- Random oracle prevents offline brute-force preparation
- Real hash functions share this property practically
- Key difference between theory and implementation

## Slide 9: Merkle-Damgård Vulnerabilities

- SHA-1 and SHA-2 use Merkle-Damgård construction
- Vulnerable to length extension attacks
- Can compute H(m || m') from H(m) without knowing m
- Demonstrates gap between random oracle ideal and reality

## Slide 10: SHA-3 and Modern Solutions

- SHA-3 uses sponge construction (not Merkle-Damgård)
- HMAC-based extraction (HKDF) fixes length extension issues
- Define new function HODX using HMAC to patch vulnerabilities
- Modern designs closer to random oracle behavior

## Slide 11: Question for You

So maybe practitioners were right all along, they just couldn't prove it?
