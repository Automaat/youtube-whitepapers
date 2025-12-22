Generate 11 presentation slides based on the podcast about CRYSTALS-Kyber.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Post-Quantum Cryptography

- Current encryption (RSA, Diffie-Hellman) vulnerable to quantum computers using Shor's algorithm
- Quantum computers can break classical public-key cryptography in polynomial time
- Need for quantum-resistant algorithms before large-scale quantum computers emerge
- CRYSTALS-Kyber: NIST-selected lattice-based key encapsulation mechanism (KEM)

## Slide 2: The Quantum Threat to Current Cryptography

- Shor's algorithm enables factorization and discrete logarithm solutions in polynomial time
- Traditional key exchange protocols (TLS, SSH) at risk from quantum attacks
- "Harvest now, decrypt later" threat: adversaries storing encrypted data for future decryption
- Urgent need for transition to post-quantum cryptography standards

## Slide 3: Learning With Errors (LWE) Problem

- Mathematical foundation: deliberately noisy linear equations over finite fields
- Computational hardness: solving noisy linear systems is NP-hard
- Lattice-based cryptography: rich mathematical structure enabling efficient operations
- Quantum resistance: no known efficient quantum algorithm for LWE problems

## Slide 4: How Kyber Key Encapsulation Works

- Alice generates public key from LWE instance with intentional noise
- Bob encapsulates shared secret by adding his own noise layer
- Both parties derive same key despite noise through controlled error margins
- IND-CCA2 security: indistinguishability under adaptive chosen-ciphertext attacks

## Slide 5: Polynomial Ring Structure in Kyber

- Operations in quotient ring R_q = Z_q[X]/(X^256 + 1)
- Degree-256 polynomials with coefficients modulo q = 3329
- Number-Theoretic Transform (NTT) for efficient polynomial multiplication
- Structured lattices enable compact keys and fast operations

## Slide 6: Performance and Efficiency

- Public key: ~800-1184 bytes (security levels 512-1024)
- Ciphertext: ~768-1568 bytes
- Shared secret: 32 bytes
- Key generation: microseconds on modern hardware
- Optimized implementations achieve thousands of operations per second

## Slide 7: NTT Optimization for Polynomial Multiplication

- Number-Theoretic Transform: fast polynomial multiplication in O(n log n)
- Barrett reduction: efficient modular arithmetic without division
- Constant-time implementation: prevents timing side-channel attacks
- Hardware-friendly: vectorization on ARM NEON and x86 AVX2

## Slide 8: Real-World Deployment and Standards

- NIST PQC standardization: selected as primary KEM algorithm (2022)
- TLS 1.3 integration: hybrid mode combining Kyber with classical ECDH
- Backward compatibility: coexists with existing cryptographic infrastructure
- Industry adoption: Google Chrome, Cloudflare, AWS already implementing

## Slide 9: Security Analysis and Proven Properties

- IND-CCA2 security proof in random oracle model
- Reduction to Module-LWE hardness assumption
- Side-channel resistance: constant-time operations, masking techniques
- Conservative parameter selection: withstands known lattice attacks (BKZ, sieve algorithms)

## Slide 10: Kyber Evolution and Future

- Predecessor: NewHope algorithm (simpler but larger keys)
- ML-KEM (Module Lattice KEM): NIST standardized version of Kyber
- Ongoing research: smaller keys, faster implementations, formal verification
- Long-term vision: complete migration from classical to post-quantum cryptography

## Slide 11: Question for You

How should organizations balance the urgency of transitioning to post-quantum cryptography against the constantly evolving threat landscape?
