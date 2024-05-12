import hashlib
import json
from time import time


class Block:
    def __init__(self, **kwargs):
        self.index = kwargs.get("index")
        self.timestamp = kwargs.get("timestamp")
        self.data = kwargs.get("data")
        self.previous_hash = kwargs.get("previous_hash")
        self.hash = kwargs.get("hash", self.calculate_hash())

    def calculate_hash(self):
        return hashlib.sha256(
            str(self.index).encode()
            + str(self.timestamp).encode()
            + json.dumps(self.data).encode()
            + self.previous_hash.encode()
        ).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = self.load_blockchain()  # Load blockchain from file
        if not self.chain:
            self.chain = [self.create_genesis_block()]
            self.save_blockchain()

    def create_genesis_block(self):
        return Block(0, time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        self.save_blockchain()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def print_blocks(self):
        for block in self.chain:
            print(f"Block Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print()

    def save_blockchain(self):
        with open("blockchain.json", "w") as f:
            json.dump([vars(block) for block in self.chain], f)

    def load_blockchain(self):
        try:
            with open("blockchain.json", "r") as f:
                chain_data = json.load(f)
                return [Block(**block_data) for block_data in chain_data]
        except (IOError, json.JSONDecodeError):
            return None


blockchain = Blockchain()
print("Initial blockchain:")
blockchain.print_blocks()


def addNewTransaction(data):
    blockchain.add_block(
        Block(
            index=len(blockchain.chain),
            timestamp=time(),
            data=data,
            previous_hash=blockchain.get_latest_block().hash,
        )
    )


# Print blockchain after adding blocks
print("\nBlockchain after adding blocks:")
# addNewTransaction("Sample transaction data")
blockchain.print_blocks()
