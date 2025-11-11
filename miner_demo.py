import hashlib
import json
import time
from typing import Any, List

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

class Block:
    """
    A minimal block:
      - index:       height in the chain (0 = genesis)
      - timestamp:   unix time when created
      - data:        any JSON-serializable payload (e.g., transactions)
      - previous_hash: hash of the previous block
      - nonce:       number miners vary to satisfy difficulty
      - hash:        this block's header hash (after mining)
    """
    def __init__(self, index: int, data: Any, previous_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()  # initial (unmined) hash

    def header_string(self) -> str:
        # Sort keys to make hashing stable
        data_json = json.dumps(self.data, sort_keys=True, separators=(",", ":"))
        return f"{self.index}|{self.timestamp}|{self.previous_hash}|{data_json}|{self.nonce}"

    def compute_hash(self) -> str:
        return sha256_hex(self.header_string())

    def mine(self, difficulty: int) -> None:
        """Proof-of-Work: find nonce so hash has N leading zeros."""
        assert difficulty >= 0
        target_prefix = "0" * difficulty
        # Try nonces until the hash satisfies the target
        while True:
            self.hash = self.compute_hash()
            if self.hash.startswith(target_prefix):
                return
            self.nonce += 1

class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.chain: List[Block] = [self._create_genesis()]

    def _create_genesis(self) -> Block:
        # The first block; previous_hash is a fixed constant
        genesis = Block(index=0, data={"msg": "Genesis Block"}, previous_hash="0" * 64)
        # For demos we mine genesis too (optional)
        genesis.mine(self.difficulty)
        return genesis

    @property
    def tip(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: Any) -> Block:
        """Create, mine, and append a new block with the given data."""
        new_block = Block(index=self.tip.index + 1, data=data, previous_hash=self.tip.hash)
        start = time.time()
        new_block.mine(self.difficulty)
        elapsed = time.time() - start
        self.chain.append(new_block)
        print(f"✅ Mined block #{new_block.index} in {elapsed:.3f}s  hash={new_block.hash[:16]}…  nonce={new_block.nonce}")
        return new_block

    def is_valid(self) -> bool:
        """Full chain validation: links, hashes, and difficulty."""
        target_prefix = "0" * self.difficulty
        for i, block in enumerate(self.chain):
            # Recompute hash from the block's stored fields
            recalculated = block.compute_hash()
            if block.hash != recalculated:
                print(f"❌ Block {i} hash mismatch")
                return False
            if not block.hash.startswith(target_prefix):
                print(f"❌ Block {i} fails difficulty target")
                return False
            if i == 0:
                # Genesis: previous_hash must be 64 zeros
                if block.previous_hash != "0" * 64:
                    print("❌ Genesis previous_hash incorrect")
                    return False
            else:
                prev = self.chain[i - 1]
                if block.previous_hash != prev.hash:
                    print(f"❌ Block {i} previous_hash does not match block {i-1}")
                    return False
        return True

    def pretty_print(self) -> None:
        for b in self.chain:
            print("\n" + "-" * 70)
            print(f"Block #{b.index}")
            print(f"  time:          {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(b.timestamp))}")
            print(f"  prev_hash:     {b.previous_hash}")
            print(f"  nonce:         {b.nonce}")
            print(f"  hash:          {b.hash}")
            print(f"  data:          {json.dumps(b.data, indent=2, sort_keys=True)}")
        print("\n" + "-" * 70)

def interactive_demo() -> None:
    print("🚀 Mini Blockchain Demo (Interactive Mode)")
    print("-------------------------------------------")

    chain = Blockchain(difficulty=4)
    print(f"✅ Blockchain initialized with Genesis Block (difficulty={chain.difficulty})\n")

    while True:
        print("\nMenu:")
        print("1. Add new block")
        print("2. View blockchain")
        print("3. Validate chain")
        print("4. Tamper with a block")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            sender = input("Enter sender name: ")
            receiver = input("Enter receiver name: ")
            amount = input("Enter amount: ")

            data = {"from": sender, "to": receiver, "amount": float(amount)}
            print("⛏️  Mining new block...")
            chain.add_block(data)

        elif choice == "2":
            chain.pretty_print()

        elif choice == "3":
            print("\n🔍 Checking blockchain validity...")
            valid = chain.is_valid()
            if valid:
                print("✅ The blockchain is valid.")
            else:
                print("❌ Blockchain integrity has been broken!")

        elif choice == "4":
            try:
                index = int(input("Enter block index to tamper (e.g. 1): "))
                key = input("Enter field to modify (e.g. amount/from/to): ").strip()
                new_value = input("Enter new value: ").strip()

                if 0 <= index < len(chain.chain):
                    block = chain.chain[index]
                    if key in block.data:
                        block.data[key] = new_value
                        print(f"⚠️  Block #{index} modified! Re-run validation to check results.")
                    else:
                        print("❌ Invalid field name.")
                else:
                    print("❌ Invalid block index.")
            except ValueError:
                print("❌ Please enter a valid number.")

        elif choice == "5":
            print("\n👋 Exiting... Thank you for exploring the mini blockchain!")
            break

        else:
            print("❌ Invalid option. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    interactive_demo()
