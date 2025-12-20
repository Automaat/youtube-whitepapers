Generate 11 presentation slides based on the podcast about Yao's "Protocols for Secure Computations" (1982).

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Millionaires' Problem

- Two wealthy individuals want to determine who is richer
- Critical constraint: neither wants to reveal their actual wealth
- Classic example of Secure Multi-Party Computation (MPC)
- Yao's 1982 paper opened an entirely new field in cryptography
- Fundamental question: can parties compute jointly using private data while only learning the final result?
- Proves that secure computation is possible for any computable function

## Slide 2: One-Way Functions & Garbled Circuits

- One-way functions: easy to compute forward, computationally infeasible to reverse (like a magic lock)
- Alice has public lock (anyone can lock) and private key (only she can unlock)
- Bob can encrypt data with Alice's public lock, only Alice can decrypt
- Foundation for garbled circuits: encrypted truth tables that hide intermediate values
- Each computation step is "garbled" so evaluator learns nothing except final output
- Enables secure evaluation of arbitrary Boolean circuits

## Slide 3: Protocol Construction Using Oblivious Transfer

- Alice creates 10 locked boxes, each containing comparison result for one wealth value
- Bob receives boxes but can only open one corresponding to his actual wealth
- Oblivious transfer: Bob learns one value, Alice doesn't know which one he opened
- Intersection of Bob's pointer and Alice's knowledge reveals the comparison
- Communication occurs such that only final result leaks, nothing more
- Mathematical formalization transforms intuition into provable security guarantees

## Slide 4: Security Model & Information Leakage

- Entire communication designed so only final comparison result leaks
- No intermediate values, wealth amounts, or computation steps are revealed
- Formal security definition: protocol is secure if it reveals no more than the output itself
- Passive adversary model: participants follow protocol but try to learn extra information
- Active adversary model: participants may deviate from protocol arbitrarily
- Information-theoretic vs computational security trade-offs

## Slide 5: Scaling to Large Input Domains

- What if millionaires have billions in wealth? Does protocol become impractical?
- Theorem 2: polynomial protocol construction for any computable function
- Data exchange proportional to circuit complexity, not input domain size
- For many practical problems with relatively simple circuits, protocol becomes realistic
- Circuit representation: any function can be expressed as Boolean gates (AND, OR, NOT)
- Polynomial-size protocols make secure computation feasible in practice

## Slide 6: Reducing Communication Complexity

- Naive approach requires exchanging massive amounts of data
- Yao showed communication is proportional to circuit size, not input size
- Garbled circuit size: O(|C|) where |C| is number of gates in circuit
- Each gate requires constant communication (encrypted truth table)
- Comparison of n-bit numbers: O(n) circuit size, not O(2^n) as naive approach
- Makes protocol practical for real-world applications with reasonable circuit sizes

## Slide 7: Extension to M-Party Computation

- Generalization from two parties to M participants
- New risk emerges: collusion between multiple parties
- What if several participants conspire to cheat the others?
- Yao proves protocols can be constructed resistant to M-1 colluding parties against one honest party
- Requires more sophisticated cryptographic primitives and proof techniques
- Threshold security: protocol remains secure as long as honest majority exists

## Slide 8: Impossibility of Perfect Exchange Protocols

- Fundamental limitation theorem: in any direct exchange protocol, one party can always cheat with probability ≥ 1/2
- There exists a moment when one party knows the other's secret, but not vice versa
- In that fraction of a second, the first party can disconnect, leaving the second with nothing
- Proves need for trusted third party or cryptographic commitment schemes for fair exchange
- Demonstrates fundamental asymmetry in two-party protocols without additional assumptions
- Motivates development of commitment schemes and zero-knowledge proofs

## Slide 9: Applications Beyond Millionaires

- Secure comparison enables secure voting systems (no vote reveals, only tallies)
- Secret auctions: determine winner without revealing losing bids
- Privacy-preserving data analysis: compute statistics on combined datasets without sharing raw data
- Medical research: analyze patient records across institutions without violating privacy
- Financial institutions: detect fraud patterns across banks without sharing customer data
- Modern applications: privacy-preserving machine learning, secure genomic computation

## Slide 10: Legacy and Modern Impact

- Yao's work laid foundation for entire field of secure multi-party computation
- Garbled circuits remain fundamental primitive in modern MPC protocols
- Contemporary systems: Sharemind, SCALE-MAMBA, cryptographic frameworks in production
- Blockchain smart contracts inspired by MPC concepts (compute on encrypted state)
- Homomorphic encryption extends ideas to arbitrary computation on encrypted data
- Most private data held by few global corporations and governments—MPC offers path to privacy-preserving insights

## Slide 11: Question for You

If you could run one arbitrary secure computation on all the private data of humanity combined—data held by corporations and governments—what function would you compute to discover something truly fundamental about our society that we don't know today?
