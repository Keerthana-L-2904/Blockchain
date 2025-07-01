## Introduction:
- **This is a custom blockchain implementation project aimed at understanding blockchains.** 
- **It has a native cryptocurrency with miners and the transactions are stored in Merkle Tree.**
- **The blockchain is Proof of Work based on simulated miner block sealing and block reward system.**

## Components:
- **Block**: Stores hash, Merkle root, transactions, and nonce
- **Blockchain**: List-like structure maintaining the block sequence
- **MerkleTree**: Generates Merkle root from hashed transactions
- **Miner Selection**: Picks the miner with highest BSS = competence_score * BHS
- **Nonce Finder**: Computes a nonce such that the hash ends in '0' (simulates PoW)

## How it Works?
- **Create Accounts with user-defined balances.**
- **Input Transactions and filter based on balances and incentives.**
- **Group Valid Transactions (up to 4 per block)**
- **Build Merkle Tree and get Merkle Root.**
- **Generate Block Hash using previous block’s hash + Merkle root.**
- **Find Nonce such that the final hash ends in '0'.**
- **Select Miner using BSS and reward with block incentive.**
- **Append Block to blockchain and print details.**
