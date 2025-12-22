Generate 11 presentation slides based on the podcast about Oyente: Making Smart Contracts Smarter.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Introduction to Oyente

- First automated analysis tool for Ethereum smart contracts
- Symbolic execution-based vulnerability scanner
- Detects four major security bug classes in Solidity code
- Published by research team analyzing 19,366 real contracts
- Response to billions lost in smart contract exploits

## Slide 2: The Vulnerability Problem

- Traditional security tools don't work for blockchain contracts
- Immutable code - bugs cannot be patched after deployment
- Four critical vulnerability types targeted by Oyente
- Real-world incidents: DAO hack, Parity wallet freeze
- Need for automated detection before deployment

## Slide 3: Four Vulnerability Classes

- Transaction-ordering dependence (TOD): race conditions in transactions
- Timestamp dependence: relying on block timestamps for critical logic
- Mishandled exceptions: silently failing external calls
- Reentrancy: recursive call attacks (DAO hack vulnerability)

## Slide 4: Symbolic Execution Engine

- Uses symbolic variables instead of concrete values
- Explores all possible execution paths through contract
- Generates constraints for each path condition
- Leverages Z3 SMT solver for constraint satisfaction
- Identifies paths leading to vulnerable states

## Slide 5: Control Flow Graph Analysis

- Decompiles EVM bytecode into control flow graph (CFG)
- Maps every possible execution path and branch
- Tracks state changes and external calls
- Enables path-by-path vulnerability detection
- Works directly on compiled bytecode, not source code

## Slide 6: Evaluation Results

- Scanned 19,366 Ethereum contracts from blockchain
- 8,833 contracts flagged with potential vulnerabilities
- 99% analysis completion rate
- Average analysis time: 11.6 seconds per contract
- Validated findings against known exploits

## Slide 7: The Greedy Attack Pattern

- Transaction-ordering attacks exploiting miner control
- Miners can reorder transactions within blocks
- Attacker profits by front-running user transactions
- Affects 1,524 contracts in dataset
- Defense: minimize reliance on transaction ordering

## Slide 8: Parity Wallet Case Study

- Multi-signature wallet with self-destruct vulnerability
- Inherited kill function from parent library contract
- Attacker triggered suicide call, freezing all wallets
- 513,000 ETH permanently locked (~$150M at the time)
- Demonstrates inheritance-based vulnerability propagation

## Slide 9: Timestamp Manipulation Risks

- Contracts using block.timestamp for critical logic
- Miners can manipulate timestamps within ~900 second window
- Used for random number generation, time-based unlocks
- Alternative: use block numbers instead of timestamps
- Found in 1,029 analyzed contracts

## Slide 10: Impact and Future Work

- Oyente established foundation for smart contract security tools
- Subsequent tools: Mythril, Slither, Manticore built on similar principles
- Symbolic execution remains core technique in contract auditing
- Highlighted need for formal verification in blockchain
- Influenced secure coding practices in Solidity development

## Slide 11: Question for You

What security practices should be mandatory before deploying smart contracts managing significant value on blockchain platforms?
