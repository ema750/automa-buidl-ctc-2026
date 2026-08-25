#!/usr/bin/env python3
"""AUTOMA - Deploy della suite demo su Base Sepolia.

Uso:
    python scripts/1_deploy.py

Prima esecuzione: genera un wallet di test, lo salva in .env.demo e stampa
le istruzioni per il faucet. Esecuzioni successive: deploya i contratti e
scrive gli indirizzi in deployed.json.
"""
import json
import os
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BASE_SEPOLIA_RPC = "https://sepolia.base.org"
CHAIN_ID = 84532
FAUCETS = [
    "https://faucets.chain.link/base-sepolia",
    "https://www.alchemy.com/faucets/base-sepolia",
    "https://bwarelabs.com/faucets/base-sepolia",
]

ABI = {}


def compile_contracts():
    import solcx

    solcx.install_solc("0.8.20")
    out = solcx.compile_files(
        [str(ROOT / "contracts" / "AutomaVerifier.sol")],
        output_values=("abi", "bin"),
        solc_version="0.8.20",
        optimize=True,
        optimize_runs=200,
    )
    for k in list(out):
        ABI[k.split(":")[-1]] = {
            "abi": out[k]["abi"],
            "bin": bytes.fromhex(out[k]["bin"]),
        }


def load_or_create_key():
    env_file = ROOT / ".env.demo"
    key = None
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("DEPLOYER_KEY="):
                key = line.split("=", 1)[1].strip()
    if not key:
        key = "0x" + secrets.token_hex(32)
        env_file.write_text(f"DEPLOYER_KEY={key}\n")
        env_file.chmod(0o600)
        from web3 import Web3

        acct = _account(key)
        print("=" * 60)
        print("NUOVO WALLET DI TEST GENERATO")
        print(f"Indirizzo: {acct.address}")
        print(f"(chiave salvata in {env_file.name})")
        print()
        print("Prossimo passo: prendi ETH di test gratis da UNO dei faucet:")
        for f in FAUCETS:
            print(f"  - {f}")
        print(f"Incolla l'indirizzo {acct.address} nel faucet.")
        print("Poi rilancia questo script.")
        print("=" * 60)
        sys.exit(0)
    return key


def _account(key):
    from eth_account import Account

    return Account.from_key(key)


def main():
    from web3 import Web3

    compile_contracts()
    w3 = Web3(Web3.HTTPProvider(BASE_SEPOLIA_RPC))
    assert w3.is_connected(), "RPC Base Sepolia non raggiungibile"
    print(f"Connesso a Base Sepolia (chain {w3.eth.chain_id})")

    acct = _account(load_or_create_key())
    bal = w3.from_wei(w3.eth.get_balance(acct.address), "ether")
    print(f"Wallet: {acct.address} | ETH test: {bal}")
    if bal < 0.0005:
        print("\nSaldo insufficiente per il gas.")
        for f in FAUCETS:
            print(f"Faucet: {f} -> incolla {acct.address}")
        sys.exit(1)

    def deploy(name, *args):
        c = w3.eth.contract(abi=ABI[name]["abi"], bytecode=ABI[name]["bin"])
        tx = c.constructor(*args).build_transaction(
            {"from": acct.address,
             "nonce": w3.eth.get_transaction_count(acct.address),
             "gas": 3_500_000,
             "maxFeePerGas": w3.to_wei(0.15, "gwei"),
             "maxPriorityFeePerGas": w3.to_wei(0.001, "gwei"),
             "chainId": CHAIN_ID})
        signed = acct.sign_transaction(tx)
        h = w3.eth.send_raw_transaction(signed.raw_transaction)
        rc = w3.eth.wait_for_transaction_receipt(h, timeout=180)
        print(f"  {name}: {rc.contractAddress}")
        print(f"    tx: https://sepolia.basescan.org/tx/{h.hex()}")
        assert rc.status == 1, f"deploy {name} fallito"
        return w3.eth.contract(address=rc.contractAddress, abi=ABI[name]["abi"])

    print("\n[1/4] Deploy MockUSDC...")
    usdc = deploy("MockUSDC", 1_000_000 * 10 ** 6)
    print("[2/4] Deploy MockAttestcoin...")
    att = deploy("MockAttestcoin")
    print("[3/4] Deploy AutomaVerifier...")
    ver = deploy("AutomaVerifier", att.address, usdc.address)
    print("[4/4] Fondo il verifier con 500 USDC di test...")
    tx = usdc.functions.transfer(ver.address, 500 * 10 ** 6).build_transaction(
        {"from": acct.address,
         "nonce": w3.eth.get_transaction_count(acct.address),
         "gas": 120_000,
         "maxFeePerGas": w3.to_wei(0.15, "gwei"),
         "maxPriorityFeePerGas": w3.to_wei(0.001, "gwei"),
         "chainId": CHAIN_ID})
    signed = acct.sign_transaction(tx)
    h = w3.eth.send_raw_transaction(signed.raw_transaction)
    w3.eth.wait_for_transaction_receipt(h, timeout=180)
    print(f"    tx: https://sepolia.basescan.org/tx/{h.hex()}")

    info = {
        "network": "base-sepolia",
        "mock_usdc": usdc.address,
        "mock_attestcoin": att.address,
        "automa_verifier": ver.address,
        "deployer": acct.address,
    }
    (ROOT / "deployed.json").write_text(json.dumps(info, indent=2))
    print("\nDEPLOY COMPLETATO:")
    print(json.dumps(info, indent=2))
    print("\nVerifica su Basescan:")
    for k in ("mock_usdc", "mock_attestcoin", "automa_verifier"):
        print(f"  {k}: https://sepolia.basescan.org/address/{info[k]}")


if __name__ == "__main__":
    main()
