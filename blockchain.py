import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, str(datetime.now()), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, product_id, role, location, description, timestamp):
        transaction = {
            "product_id": product_id,
            "role": role,
            "location": location,
            "description": description,
            "timestamp": timestamp,
        }
        self.pending_transactions.append(transaction)

    def mine_block(self):
        if not self.pending_transactions:
            return False

        new_block = Block(
            len(self.chain),
            str(datetime.now()),
            self.pending_transactions,
            self.get_latest_block().hash,
        )
        self.chain.append(new_block)
        self.pending_transactions = []

    def get_product_history(self, product_id):
        history = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["product_id"] == product_id:
                    history.append(transaction)
        return history

    def get_all_records(self):
        all_records = []
        for block in self.chain:
            all_records.extend(block.transactions)
        return all_records
