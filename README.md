Mini Blockchain – Proof of Work (Python)

A minimal blockchain prototype built in Python to demonstrate how blocks are mined and linked through cryptographic hashes using the Proof of Work mechanism.

🚀 Features
Genesis block creation (index 0, previous hash = all zeros)
SHA-256 hashing of each block’s header
Proof-of-Work mining (configurable difficulty)
Blockchain validation (detects tampering instantly)
Interactive CLI to add, view, and modify blocks

🧱 Block Structure
Each block stores:
index | timestamp | data | previous_hash | nonce | hash

⚙️ Run the Project
python3 miner_demo.py

Then follow the interactive menu:

1. Add new block
2. View blockchain
3. Validate chain
4. Tamper with a block
5. Exit

Example Output
✅ Mined block #1 in 0.187s  hash=0000fc27…  nonce=50875
🔍 Checking blockchain validity...
❌ Block 1 hash mismatch
❌ Blockchain integrity has been broken!

🧠 Concepts Demonstrated
Block creation and chaining
Proof of Work mining
SHA-256 hashing
Immutability and validation
Tamper detection in blockchain systems

🧰 Technologies
Python 3 · hashlib · json · time
