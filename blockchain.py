#some examples given in the assignment will not work bcoz as stages increases, the chnages are made within that for eg 
# first stage doesnt have transaction order of highest insentive shud come first similarly in first stage, its only 3 transactions per block 

import hashlib

class Block:
    def __init__(self, block_num, block_hash, txns, merkle_root, nonce):
        self.block_num = block_num
        self.block_hash = block_hash
        self.txns = txns
        self.merkle_root = merkle_root
        self.nonce = nonce

class Blockchain:
    def __init__(self):
        self.chain = []

    def add_block(self, block_num, block_hash, txns, merkle_root, nonce):
        self.chain.append(Block(block_num, block_hash, txns, merkle_root, nonce))

    def print_block(self):
        for block in self.chain:
            print(block.block_num)
            print(block.block_hash)
            print(block.txns)
            print(block.merkle_root)
            print(block.nonce)

class MerkleNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class MerkleTree:
    def __init__(self, transactions=None):  # This makes the transactions parameter optional. That means you can create a MerkleTree instance in two ways: With transactions and Without any transactions:
        if transactions is not None:
            self.transactions = transactions
        else:
            self.transactions = []
        self.root = None  # points to the actual root
        self.merkle_root = ''  # points to the hash of the root  root.data=merkle_root but its better to keep two diff variables
        self.build_tree(self.transactions)  # build tree function wiith transactions as input

    def _hash_the_data(self, data):
        return hashlib.sha3_256(data.encode()).hexdigest()

    def build_tree(self, transactions):
        nodes = []
        for tx in transactions:
            if tx is not None:
                nodes.append(MerkleNode(self._hash_the_data(tx)))
        if not nodes:
            self.root = None  # points to the actual root
            self.merkle_root = ''
            return
        while (len(nodes) > 1):
            if len(nodes) % 2 == 1:  # It checks if the number of nodes is odd (len(nodes) % 2 == 1).
                nodes.append(nodes[-1])  # If yes, it duplicates the last node (nodes[-1]) and appends it to the list.
            new_level = []
            for i in range(0, len(nodes), 2):
                summ = self._hash_the_data(nodes[i].data + nodes[i + 1].data)
                parent = MerkleNode(summ)
                parent.left = nodes[i]
                parent.right = nodes[i + 1]
                new_level.append(parent)
            nodes = new_level
            # why do we have new_level=[] and nodes=[]
            # Level 0: [L1, L2, L3, L4]
            # Pair (L1+L2), (L3+L4)
            # new_level = [P1, P2]
            # nodes = new_level  → Now process [P1, P2]
        self.root = nodes[0]
        self.merkle_root = self.root.data

def hash_the_data(data):
    return hashlib.sha3_256(data.encode()).hexdigest()


def sort_txns(transactions):  # stage 2
    txn = []
    for i, j in enumerate(transactions):  # sorting is more difficult with list of list thats why we convert to list of tuples
        txn.append((i, j))
    txn.sort(key=lambda x: (-x[1]["incentive"],x[1]["to"],x[0])) # x[1] is transaction and x[0] is index number  - is descending and + is ascending
    result = []  # only has transactions not the index
    for pair in txn:
        result.append(pair[1])
    return result

def find_nonce(block_hash):  # stage 4
    nonce = 0
    while True:
        data = block_hash + str(nonce)
        hashed = hash_the_data(data)
        if hashed.endswith("0"):
            return nonce
        nonce += 1


def find_miner(miners, block_num):  # stage 5
    maxx = 0
    max_miner = ""  # max_miner keeps track of the miner id who has the highest BSS score as you loop through all miners.
    for j in miners:
        bhs = j["bhsa"][block_num % 8]  # bhs = block_hash_score_array[block_number%8]
        bss = j["com_score"] * bhs  # bss[i] = com[i]*bhs
        if maxx < bss:
            maxx = bss
            max_miner = j["miner_id"]
    return max_miner

# miners: a list of dictionaries. Each dictionary represents a miner and contains:
# miner_id: a unique identifier
# com_score: some score representing miner's competence
# bhsa: a list (of length 8) containing values used in scoring

def main():
    blockchain = Blockchain()
    accounts = {}
    miner = []
    t = []
    block_reward = 0
    while True:
        print("\nMENU:")
        print("1. Enter accounts")
        print("2. Enter transactions")
        print("3. Block reward")
        print("4. Number of miners")
        print("5. Print blockchain")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if (choice=="1"):
            n = int(input("Enter the number of accounts: "))
            for i in range(n):
                acc, bal = input().split()
                accounts[acc] = int(bal)
        elif choice=="2":
            m = int(input("Enter the number of transactions: "))
            for _ in range(m):
                acc_from, acc_to, amt, inc = input().split()
                if int(inc) < 0:
                    continue  # it will exit out of for loop continue used only when there is for or while loop
                t.append({"from": acc_from, "to": acc_to, "amount": int(amt), "incentive": int(inc)})
            t = sort_txns(t)
        elif choice=="3":
            block_reward = int(input("Enter the block reward available: "))
        elif choice=="4":
            p = int(input("Enter the number of miners: "))
            for i in range(p):
                arr = input().split()
                idd = arr[0]
                com_score = int(arr[1])
                bhsa = list(map(int, arr[2:10]))
                miner.append({"miner_id": idd, "com_score": com_score, "bhsa": bhsa})
        elif choice=="5":
            count = 0  # Tracks how many valid transactions have been added to the current block.
            block_count = 0  # Tracks how many blocks have been added to the blockchain.
            prev_block_hash = "0"  # Stores the hash of the previous block
            node = []  # it holds 4 transactions and then the merkle tree is made
            array=[]
            for i in range(len(t)):
                if accounts[t[i]["from"]] > t[i]["amount"]:
                    accounts[t[i]["from"]] -= t[i]["amount"]
                    accounts[t[i]["to"]] += t[i]["amount"]
                    node.append(t[i]["from"] + t[i]["to"] + str(t[i]["amount"]) + str(t[i]["incentive"]))
                    array.append(t[i])
                    count += 1

                    if count == 4:
                        block_count += 1
                        merkle_tree = MerkleTree(node)  # create merkle tree of 4 txns
                        txn = []
                        for a in array[-4:]:
                            txn.append([a["from"], a["to"], a["amount"], a["incentive"]])
                        curr_block_hash = hash_the_data(str(prev_block_hash) + str(block_count) + merkle_tree.merkle_root)
                        nonce = find_nonce(curr_block_hash)
                        if miner:
                            bhs_miner = find_miner(miner, block_count)
                            nonce_miner = str(nonce) + " " + bhs_miner
                            accounts[bhs_miner] += block_reward
                        else:
                            bhs_miner=None
                            nonce_miner=None
                        blockchain.add_block(block_count, curr_block_hash, txn, merkle_tree.merkle_root, nonce_miner)  # there is no concept of block_num its only block_count
                        node = []
                        count = 0
                        prev_block_hash = curr_block_hash
                else:
                    continue

            if count > 0:  # case where number of transactions are between 1 and 3
                block_count += 1
                merkle_tree = MerkleTree(node)
                txn = []
                for a in array[-count:]:
                    txn.append([a["from"], a["to"], a["amount"], a["incentive"]])
                curr_block_hash = hash_the_data(str(prev_block_hash) + str(block_count) + merkle_tree.merkle_root)
                nonce = find_nonce(curr_block_hash)
                if miner:
                    bhs_miner = find_miner(miner, block_count)
                    nonce_miner = str(nonce) + " " + bhs_miner
                    accounts[bhs_miner] += block_reward
                else:
                    bhs_miner=None
                    nonce_miner=None

                blockchain.add_block(block_count, curr_block_hash, txn, merkle_tree.merkle_root,nonce_miner)  # there is no concept of block_num its only block_count
            blockchain.print_block()
        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")
if __name__ == '__main__':
    main()