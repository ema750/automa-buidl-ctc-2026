#!/usr/bin/env python3
"""
Script per monitorare eventi di Transfer del contratto USDC su Base Sepolia.
Invia alert via Telegram quando un evento viene rilevato.
"""

import os
import json
import time
from web3 import Web3
from dotenv import load_dotenv
import requests

# Carica variabili d'ambiente
load_dotenv()

# Configurazione
PROVIDER_URL = os.getenv("PROVIDER_URL", "https://sepolia.base.org")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
USDC_CONTRACT_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"

# ABI minimale per l'evento Transfer
USDC_ABI = """
[
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "name": "from", "type": "address"},
            {"indexed": true, "name": "to", "type": "address"},
            {"indexed": false, "name": "value", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    }
]
"""

def send_telegram_alert(message: str):
    """Invia un alert via Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Errore nell'invio dell'alert: {response.text}")


def monitor_transfers():
    """Monitora gli eventi di Transfer del contratto USDC."""
    w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
    if not w3.is_connected():
        print("Errore: impossibile connettersi a Base Sepolia")
        return

    contract = w3.eth.contract(address=USDC_CONTRACT_ADDRESS, abi=json.loads(USDC_ABI))
    last_block = w3.eth.block_number
    print(f"Monitoraggio avviato. Ultimo blocco: {last_block}")

    while True:
        try:
            current_block = w3.eth.block_number
            if current_block > last_block:
                events = contract.events.Transfer.get_logs(fromBlock=last_block + 1, toBlock=current_block)
                for event in events:
                    tx_hash = event.transactionHash.hex()
                    from_addr = event.args["from"]
                    to_addr = event.args["to"]
                    value = event.args["value"] / 10**6  # USDC ha 6 decimali
                    
                    message = (
                        f"🚨 *Nuovo Transfer USDC rilevato* 🚨\n"
                        f"Da: `{from_addr}`\n"
                        f"A: `{to_addr}`\n"
                        f"Valore: `{value} USDC`\n"
                        f"[Vedi su BaseScan](https://sepolia.basescan.org/tx/{tx_hash})"
                    )
                    send_telegram_alert(message)
                last_block = current_block
            time.sleep(10)  # Attendi 10 secondi prima del prossimo controllo
        except Exception as e:
            print(f"Errore durante il monitoraggio: {e}")
            time.sleep(30)


if __name__ == "__main__":
    monitor_transfers()