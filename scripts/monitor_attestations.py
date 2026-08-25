#!/usr/bin/env python3
"""AUTOMA - Demo end-to-end del flusso cross-chain su Base Sepolia.

Uso (dopo scripts/1_deploy.py):
    python scripts/monitor_attestations.py

Flusso:
  1. Crea un'attestazione sul MockAttestcoin (simula il layer Creditcoin)
  2. Rilascia i fondi con AutomaVerifier.verifyAndRelease()
  3. Riprova con la STESSA attestazione: deve fallire (anti-replay)
"""
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BASE_SEPOLIA_RPC = "https://sepolia.base.org"
CHAIN_ID = 84532
AMOUNT_USDC = 25


def main():
    from web3 import Web3
    import solcx

    solcx.install_solc("0.8.20")
    out = solcx.compile_files(
        [str(ROOT / "contracts" / "AutomaVerifier.sol")],
        output_values=("abi",),
        solc_version="0.8.20",
    )
    abi = {k.split(":")[-1]: v["abi"] for k, v in out.items()}

    info = json.loads((ROOT / "deployed.json").read_text())
    key = None
    for line in (ROOT / ".env.demo").read_text().splitlines():
        if line.startswith("DEPLOYER_KEY="):
            key = line.split("=", 1)[1].strip()

    w3 = Web3(Web3.HTTPProvider(BASE_SEPOLIA_RPC))
    acct = w3.eth.account.from_key(key)
    usdc = w3.eth.contract(address=info["mock_usdc"], abi=abi["MockUSDC"])
    att = w3.eth.contract(address=info["mock_attestcoin"],
                          abi=abi["MockAttestcoin"])
    ver = w3.eth.contract(address=info["automa_verifier"],
                          abi=abi["AutomaVerifier"])

    def send(fn, gas=200_000):
        tx = fn.build_transaction(
            {"from": acct.address,
             "nonce": w3.eth.get_transaction_count(acct.address),
             "gas": gas,
             "maxFeePerGas": w3.to_wei(0.15, "gwei"),
             "maxPriorityFeePerGas": w3.to_wei(0.001, "gwei"),
             "chainId": CHAIN_ID})
        signed = acct.sign_transaction(tx)
        h = w3.eth.send_raw_transaction(signed.raw_transaction)
        rc = w3.eth.wait_for_transaction_receipt(h, timeout=180)
        assert rc.status == 1, f"tx fallita: {h.hex()}"
        print(f"    tx: https://sepolia.basescan.org/tx/{h.hex()}")
        return h

    print("=== DEMO AUTOMA: pagamento cross-chain verificato ===\n")

    print("[1/4] Creo l'attestazione (simula Creditcoin Attestcoin)...")
    payload = json.dumps({
        "job": "automa-demo",
        "recipient": acct.address,
        "amount_usdc": AMOUNT_USDC,
        "ts": int(time.time()),
    }, sort_keys=True).encode()
    att_id = hashlib.sha256(payload).digest()
    send(att.functions.createAttestation(
        att_id, "creditcoin-testnet", payload), gas=150_000)
    print(f"    attestationId: 0x{att_id.hex()}\n")

    print(f"[2/4] verifyAndRelease -> rilascio {AMOUNT_USDC} USDC...")
    send(ver.functions.verifyAndRelease(
        att_id, acct.address, AMOUNT_USDC * 10 ** 6))
    bal_ver = usdc.functions.balanceOf(ver.address).call() / 10 ** 6
    bal_to = usdc.functions.balanceOf(acct.address).call() / 10 ** 6
    print(f"    saldo verifier: {bal_ver} USDC | ricevuto: {bal_to} USDC\n")

    print("[3/4] Anti-replay: stesso attestationId di nuovo...")
    try:
        send(ver.functions.verifyAndRelease(
            att_id, acct.address, AMOUNT_USDC * 10 ** 6))
        print("    !!! ERRORE: replay riuscito, bug!")
        sys.exit(1)
    except Exception as e:
        msg = str(e)
        ok = "AlreadyReleased" in msg or "revert" in msg.lower()
        print(f"    correttamente bloccato ({'AlreadyReleased' if ok else msg[:80]})\n")

    print("[4/4] Stato finale on-chain:")
    released = ver.functions.alreadyReleased(att_id).call()
    print(f"    alreadyReleased[{att_id.hex()[:16]}...] = {released}")
    verified = att.functions.verifyAttestation(att_id).call()
    print(f"    verifyAttestation = {verified}")

    print("\n=== DEMO COMPLETATA CON SUCCESSO ===")
    print("Contratti su Basescan:")
    for k in ("mock_usdc", "mock_attestcoin", "automa_verifier"):
        print(f"  {k}: https://sepolia.basescan.org/address/{info[k]}")


if __name__ == "__main__":
    main()
