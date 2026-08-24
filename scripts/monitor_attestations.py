#!/usr/bin/env python3
"""
AUTOMA Monitor Script for Attestcoin Protocol

Monitors new attestations on Creditcoin and triggers AutomaVerifier on Base.
"""

from web3 import Web3
from web3.middleware import geth_poa_middleware
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CREDITCOIN_RPC = os.getenv("CREDITCOIN_RPC", "https://rpc.creditcoin.network")
BASE_RPC = os.getenv("BASE_RPC", "https://mainnet.base.org")
ATTESTCOIN_ADDRESS = os.getenv("ATTESTCOIN_ADDRESS")
AUTOMA_VERIFIER_ADDRESS = os.getenv("AUTOMA_VERIFIER_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Validate environment
if not ATTESTCOIN_ADDRESS or not AUTOMA_VERIFIER_ADDRESS:
    raise Exception("Contract addresses not configured")
if not PRIVATE_KEY or len(PRIVATE_KEY) != 64:
    raise Exception("Invalid private key")

# ABI for Attestcoin (simplified)
ATTESTCOIN_ABI = """
[
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "name": "attestationId", "type": "bytes32"},
            {"indexed": false, "name": "sourceChain", "type": "string"},
            {"indexed": false, "name": "data", "type": "bytes"}
        ],
        "name": "AttestationVerified",
        "type": "event"
    }
]
"""

# ABI for AutomaVerifier (simplified)
AUTOMA_VERIFIER_ABI = """
[
    {
        "inputs": [
            {"name": "attestationId", "type": "bytes32"},
            {"name": "recipient", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "verifyAndRelease",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
"""

# Initialize Web3
w3_creditcoin = Web3(Web3.HTTPProvider(CREDITCOIN_RPC))
w3_base = Web3(Web3.HTTPProvider(BASE_RPC))

# Add PoA middleware for Creditcoin (if needed)
w3_creditcoin.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check connections
if not w3_creditcoin.is_connected():
    raise Exception("Failed to connect to Creditcoin RPC")
if not w3_base.is_connected():
    raise Exception("Failed to connect to Base RPC")

# Initialize contracts
attestcoin = w3_creditcoin.eth.contract(
    address=ATTESTCOIN_ADDRESS,
    abi=ATTESTCOIN_ABI
)
automa_verifier = w3_base.eth.contract(
    address=AUTOMA_VERIFIER_ADDRESS,
    abi=AUTOMA_VERIFIER_ABI
)

# Wallet account
account = w3_base.eth.account.from_key(PRIVATE_KEY)

def load_last_block():
    """Load last processed block from file."""
    try:
        with open("last_block.txt", "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return w3_creditcoin.eth.block_number

def save_last_block(block_number):
    """Save last processed block to file."""
    with open("last_block.txt", "w") as f:
        f.write(str(block_number))

def monitor_attestations():
    """Monitor new attestations on Creditcoin and trigger AutomaVerifier."""
    print("Monitoring attestations on Creditcoin...")
    
    last_block = load_last_block()
    while True:
        try:
            current_block = w3_creditcoin.eth.block_number
            if current_block > last_block:
                # Fetch new events
                events = attestcoin.events.AttestationVerified.get_logs(
                    from_block=last_block + 1,
                    to_block=current_block
                )
                for event in events:
                    attestation_id = event.args.attestationId
                    recipient = "0x" + event.args.data.hex()[-40:]  # Extract recipient from attestation data
                    print(f"New attestation detected: {attestation_id.hex()}")
                    print(f"Recipient extracted: {recipient}")
                    call_automa_verifier(attestation_id, recipient)
                last_block = current_block
                save_last_block(last_block)
            time.sleep(15)  # Poll every 15 seconds
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(30)

def call_automa_verifier(attestation_id, recipient):
    """Call AutomaVerifier.verifyAndRelease on Base."""
    try:
        # Example: Release 1 USDC (6 decimals)
        amount = 1000000  # 1 USDC
        
        tx = automa_verifier.functions.verifyAndRelease(
            attestation_id,
            recipient,
            amount
        ).build_transaction({
            "from": account.address,
            "gas": 200000,
            "gasPrice": w3_base.eth.gas_price,
            "nonce": w3_base.eth.get_transaction_count(account.address)
        })
        
        signed_tx = account.sign_transaction(tx)
        tx_hash = w3_base.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Transaction sent: {tx_hash.hex()}")
        
        # Wait for receipt
        receipt = w3_base.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("Transaction successful!")
        else:
            print("Transaction failed!")
    except Exception as e:
        print(f"Error calling AutomaVerifier: {e}")

if __name__ == "__main__":
    monitor_attestations()