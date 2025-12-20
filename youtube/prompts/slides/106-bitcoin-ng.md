Generate 11 presentation slides based on the podcast about Bitcoin-NG (Next Generation).

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Bitcoin's Scalability Problem

- Bitcoin processes only 3-7 transactions per second
- Block propagation delay creates latency bottleneck
- Mining in China takes significant time to reach Texas nodes
- Network latency fundamentally limits throughput
- Trade-off between security and transaction processing speed

## Slide 2: Bitcoin-NG Architecture Overview

- Separates leader election from transaction processing
- Two block types: key blocks and microblocks
- Key blocks establish leadership via Proof of Work
- Microblocks contain actual transactions
- Maintains Bitcoin's security guarantees while improving throughput

## Slide 3: How Key Blocks Work

- Mined using traditional Proof of Work mechanism
- Winner becomes temporary leader for the epoch
- Leader gains exclusive right to create microblocks
- Leadership continues until next key block is mined
- Preserves decentralized mining competition

## Slide 4: Microblock Generation and Propagation

- Leader creates microblocks with pending transactions
- Microblocks propagate faster than traditional Bitcoin blocks
- No Proof of Work required for microblocks
- Leader can generate microblocks at high frequency
- Achieves 100x throughput improvement over Bitcoin

## Slide 5: Preventing Leader Abuse

- Poison transaction mechanism prevents double-spending
- If leader misbehaves, subsequent miner can publish proof
- Misbehaving leader loses all mining rewards
- Economic incentive keeps leaders honest
- Maintains Byzantine fault tolerance properties

## Slide 6: Leader Incentive Structure

- Leader receives fees from microblock transactions
- 60% of key block reward goes to current leader
- 40% goes to next key block miner
- Reward distribution ensures mining continues
- Balances short-term transaction fees with long-term security

## Slide 7: Fork Resolution and Confirmation

- Multiple confirmation levels based on block depth
- Weak confirmation: transaction in microblock
- Strong confirmation: buried under subsequent key block
- Fork resolution follows longest chain rule
- Maintains Bitcoin's eventual consistency model

## Slide 8: Real-World Performance Results

- Tested on actual Bitcoin network topology
- Achieved 100x throughput increase
- Maintained similar latency to Bitcoin
- Preserved decentralization properties
- Demonstrated practical feasibility

## Slide 9: Security Trade-offs

- Temporary centralization during leader epoch
- Leader has power until next key block mined
- Poison transactions provide economic deterrent
- Democratic character preserved through PoW mining
- Question of acceptable compromise for scalability

## Slide 10: Alternative Approaches

- DeepCoin attempts both scalability and fast confirmation
- Various blockchain architectures explore different trade-offs
- Bitcoin-NG focuses on throughput without changing consensus
- Comparison with sharding and layer-2 solutions
- Evolution of blockchain scalability research

## Slide 11: Question for You

Is temporary, rotating leadership an acceptable compromise for massive scalability gains?
