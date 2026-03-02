import os
from dotenv import load_dotenv

load_dotenv()

CONTRACT_ADDRESS = os.getenv("BLOCKCHAIN_CONTRACT_ADDRESS", "")

# Blockchain is optional — gracefully degrade if not configured
_blockchain_available = False
contract = None

try:
    if CONTRACT_ADDRESS and CONTRACT_ADDRESS != "PASTE_DEPLOYED_ADDRESS_HERE":
        from web3 import Web3

        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

        ABI = [
            {
                "inputs": [{"internalType": "bytes32", "name": "_hash", "type": "bytes32"}],
                "name": "storeHash",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "bytes32", "name": "_hash", "type": "bytes32"}],
                "name": "verifyHash",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
        ]

        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        _blockchain_available = True
        print("✅ Blockchain connected")
    else:
        print("⚠️  Blockchain not configured — running without on-chain verification")
except Exception as e:
    print(f"⚠️  Blockchain unavailable: {e} — running without on-chain verification")


def store_hash_on_chain(hash_hex: str):
    if not _blockchain_available:
        print(f"[mock] Would store hash on chain: {hash_hex[:16]}...")
        return
    account = contract.w3.eth.accounts[0]
    from web3 import Web3
    tx = contract.functions.storeHash(
        Web3.to_bytes(hexstr=hash_hex)
    ).transact({"from": account})
    contract.w3.eth.wait_for_transaction_receipt(tx)


def verify_hash_on_chain(hash_hex: str) -> bool:
    if not _blockchain_available:
        print(f"[mock] Would verify hash on chain: {hash_hex[:16]}...")
        return True  # assume valid when blockchain is not available
    from web3 import Web3
    return contract.functions.verifyHash(
        Web3.to_bytes(hexstr=hash_hex)
    ).call()