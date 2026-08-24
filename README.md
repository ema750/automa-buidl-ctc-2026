# AUTOMA BUIDL CTC 2026 Fall Submission

## Autonomous Agent with Cross-Chain Verification via Attestcoin Protocol

### **Project Overview**
AUTOMA is an autonomous agent running on **Base** that executes actions **only after verifying cross-chain facts** (e.g., payments, deliveries, sensor data) via **Attestcoin Protocol** on **Creditcoin**. This submission targets the **AI** and **DeFi** tracks of BUIDL CTC 2026 Fall.

### **Key Features**
- **Cross-Chain Verification**: Uses Attestcoin Protocol to verify facts from Ethereum, Base, and other chains.
- **Autonomous Execution**: Releases funds or executes actions on Base after verification.
- **Use Cases**:
  - **DeFi**: Conditional payments (e.g., "Release funds on Base only if payment is verified on Ethereum").
  - **AI**: Autonomous agents that act on verified data (e.g., "Execute trade only if sensor data is attested").

---

## **Architecture**

```
[Ethereum/Polygon]       [Creditcoin]               [Base]
      |                       |                           |
      |-- Payment/Event --> Attestcoin Protocol --> AutomaVerifier.sol --> Action
```

1. **Attestcoin Protocol** (Creditcoin):
   - Generates attestations for events on other chains (e.g., Ethereum payments).
2. **AutomaVerifier.sol** (Base):
   - Verifies attestations and executes actions (e.g., transfers USDC).
3. **Monitor Script** (Python):
   - Watches for new attestations and triggers `AutomaVerifier`.

---

## **Setup & Deployment**

### Prerequisites
- `yarn` and `foundry` installed.
- Wallet with:
  - **Creditcoin Testnet CTC** (for Attestcoin interactions).
  - **Base ETH** (for gas).
  - **USDC on Base** (for transfers).

### Steps
1. **Deploy `AutomaVerifier.sol` on Base**:
   ```bash
   forge create --rpc-url https://mainnet.base.org \
     --private-key $PRIVATE_KEY \
     contracts/AutomaVerifier.sol:AutomaVerifier \
     --constructor-args $ATTESTCOIN_ADDRESS $USDC_ADDRESS
   ```

2. **Run the Monitor Script**:
   ```bash
   pip install web3 attestcoin-sdk
   python scripts/monitor_attestations.py
   ```

---

## **Example Workflow**
1. **User pays 100 USDC on Ethereum**.
2. **Attestcoin Protocol** generates an attestation on Creditcoin.
3. **AUTOMA** detects the attestation and calls `AutomaVerifier.verifyAndRelease()`.
4. **Funds are released on Base** to the recipient.

---

## **Submission Details**
- **Hackathon**: BUIDL CTC 2026 Fall.
- **Tracks**: AI, DeFi.
- **Repository**: [https://github.com/ema750/automa-buidl-ctc-2026](https://github.com/ema750/automa-buidl-ctc-2026).
- **Demo Video**: [YouTube Link] (to be added).

---

## **License**
MIT