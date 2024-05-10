import datetime
import hashlib
import random

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(str(self.index).encode() + 
                               str(self.timestamp).encode() + 
                               str(self.data).encode() + 
                               str(self.previous_hash).encode()).hexdigest()

def generate_random_block(previous_block):
    index = previous_block.index + 1
    timestamp = datetime.datetime.now()
    data = f"Random data for block {index}"
    previous_hash = previous_block.hash
    return Block(index, timestamp, data, previous_hash)

def print_blockchain(blocks):
    for block in blocks:
        # print(f"Index: {block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print("-" * 50)

def main():
    # Create genesis block
    genesis_block = Block(0, datetime.datetime.now(), "Genesis Block", "0")
    blockchain = [genesis_block]

    # Generate 9 additional random blocks
    for _ in range(3):
        new_block = generate_random_block(blockchain[-1])
        blockchain.append(new_block)

    # Print the blockchain
    print_blockchain(blockchain)

def addNewBlock(blockcount):
    block_no = random.randint(1200, 3400)
    genesis_block = Block(block_no, datetime.datetime.now(), "Genesis Block", "0")
    blockchain = [genesis_block]

    # Generate 9 additional random blocks
    for _ in range(3):
        new_block = generate_random_block(blockchain[-1])
        blockchain.append(new_block)

    # Print the blockchain
    print_blockchain(blockchain)
    

if __name__ == "__main__":
    main()
