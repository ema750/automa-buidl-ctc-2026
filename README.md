# AUTOMA — BUIDL CTC 2026 Fall

Agente AI autonomo che guadagna USDC su Base: riceve compiti, li esegue e
incassa pagamenti rilasciati **solo dopo verifica cross-chain** tramite il
protocollo Attestcoin di Creditcoin.

## Architettura

```
Creditcoin (Attestcoin)          Base
┌─────────────────────┐   verifica   ┌──────────────────┐
│ createAttestation() │ ──────────►  │ AutomaVerifier    │
│ (lavoro completato) │              │ verifyAndRelease()│──► USDC al lavoratore
└─────────────────────┘              └──────────────────┘
```

- **AutomaVerifier.sol**: contratto principale — verifica l'attestazione
  e rilascia USDC una sola volta per attestazione (anti-replay).
- **MockAttestcoin**: simulazione del protocollo Creditcoin per la demo su
  testnet (in produzione il verdetto arriva dal protocollo reale).
- **MockUSDC**: token di test ERC20 con 6 decimali.

## Demo rapida su Base Sepolia

```bash
pip install web3 py-solc-x

# 1. Genera wallet + deploya i contratti (chiede ETH test da faucet)
python scripts/1_deploy.py

# 2. Flusso completo: attestazione -> rilascio -> anti-replay
python scripts/monitor_attestations.py
```

`1_deploy.py` al primo avvio genera un wallet e stampa i faucet consigliati
(chain.link, Alchemy, BwareLabs). Dopo aver finanziato l'indirizzo, riesegui:
deploya MockUSDC, MockAttestcoin, AutomaVerifier e scrive `deployed.json`
con tutti gli indirizzi verificabili su sepolia.basescan.org.

`monitor_attestations.py` esegue la demo end-to-end: crea l'attestazione,
rilascia 25 USDC al lavoratore e dimostra che lo stesso attestationId non
può essere riutilizzato.

## Team

AUTOMA (agente autonomo) & ema750 (creatore)
