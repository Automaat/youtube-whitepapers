Generate 11 presentation slides based on the podcast about "On the Security of Public Key Protocols" by Danny Dolev and Andrew C. Yao.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Foundational Security Paper (1981)

- Public key cryptography was new - security relied on intuition, not formal proofs
- Danny Dolev and Andrew Yao asked: what if the protocol itself has flaws?
- Strongest encryption means nothing if an attacker can manipulate the conversation
- Introduced mathematical rigor to protocol security analysis
- Created the "active saboteur" adversary model - still used today

## Slide 2: Public Key Encryption Basics

- Each user has a key pair: public key (anyone can know) and private key (secret)
- To send secret message: encrypt with recipient's public key
- Only recipient can decrypt using their private key
- Protects against passive eavesdroppers listening on the network
- But active attackers can do much more than just listen

## Slide 3: The Active Saboteur Model

- Adversary is a legitimate network user with three superpowers:
- Can intercept any message in the network
- Can initiate conversations with any participant
- Can impersonate others and inject messages mid-conversation
- Doesn't break encryption by brute force - manipulates the protocol itself
- Forces participants to unwittingly help decrypt their own messages

## Slide 4: Example 2 vs Example 3 - The Paradox

- Example 2 (secure): A sends E_B(M, A) - message M with sender name, encrypted for B
- Example 3 (broken): A sends E_B(E_A(M), A) - double encryption, looks safer
- Intuition says double encryption = more secure
- Reality: adding complexity created a new vulnerability
- Demonstrates why formal verification is essential

## Slide 5: The Oracle Attack on Example 3

- Adversary Z intercepts E_B(E_A(M), A) from A to B
- Extracts inner encrypted part: E_A(M)
- Sends it to A pretending to be legitimate request: "Please process this"
- A decrypts E_A(M) with her private key and responds per protocol
- Z repeats this trick, collecting responses until full message M is recovered
- A becomes an unwitting "decryption oracle" attacking herself

## Slide 6: Cascade Protocols - Algebraic Model

- Simplest formal model: operations are only encryption and decryption sequences
- Like layers of an onion: E_X(D_Y(E_Z(M)))
- Question: can adversary find operation sequence that removes all protections?
- Theorem 1 provides two simple security conditions
- First: every message must be encrypted on the outside
- Second: "Balancing Property" - if you decrypt with D_A, immediately re-encrypt with E_A

## Slide 7: The Balancing Property Defense

- Prevents the decryption oracle attack from Example 3
- Rule: never decrypt something and send it back in plaintext
- If you unlock with your private key, lock it again with your public key
- Forces protocol designers to think about every decrypt operation
- Simple algebraic condition with profound security implications

## Slide 8: Name-Stamp Protocols - Adding Identity

- Cascade model too simple for real protocols - need identity verification
- Allows attaching sender name to messages
- Receiver can verify if sender matches expected identity
- Much closer to real-world communication protocols
- But complexity increases for both protocols and adversary capabilities

## Slide 9: The Verification Algorithm - Theorem 3

- Proves that security verification is decidable for name-stamp protocols
- Algorithm runs in polynomial time: O(N^8) where N is protocol complexity
- O(N^8) sounds slow but is the magic boundary between feasible and infeasible
- Security becomes computable, verifiable property - not faith in designer
- Can write a program that gives definitive yes/no answer for any protocol

## Slide 10: Legacy and Impact

- Founded entire school of thought: symbolic security analysis
- Tools used today for banking, messaging apps, TLS (securing the internet)
- Modern protocol analyzers stand on Dolev-Yao foundations
- Showed complexity ≠ security
- Formal methods became standard practice in cryptographic protocol design

## Slide 11: Question for You

Are protocols designed to defend against a clever human spy ready for attack by a persistent but infinitely patient machine?
