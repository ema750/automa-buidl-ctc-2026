# Base Smart Contract Event Watcher & Telegram Alert Service

## 🚀 Overview
A **real-time alert system** for smart contract events on the **Base blockchain**, designed to notify users via **Telegram** when specific events are emitted. Built for the **BUIDL CTC 2026 Fall Hackathon**.

### 🔍 Problem Solved
Smart contract events (e.g., token transfers, NFT mints, or DeFi actions) often require real-time monitoring. Existing solutions are either:
- Too complex to set up.
- Lack user-friendly notifications.
- Not optimized for Base.

This project provides a **simple, scalable, and real-time** solution to monitor events and receive alerts on Telegram.

---

## ✨ Features
- **Real-time monitoring**: Watches for smart contract events on Base.
- **Telegram alerts**: Sends instant notifications to a Telegram chat.
- **Easy setup**: Deploy your own watcher in minutes.
- **Customizable**: Configure which events to monitor and how to notify.
- **Open-source**: MIT licensed and free to use.

---

## 🛠 Tech Stack
- **Blockchain**: Base (EVM-compatible).
- **Smart Contract**: Solidity (event emission).
- **Backend**: Node.js (event monitoring).
- **Telegram Bot**: Real-time alerts.
- **Testing**: Mocha + Chai (unit and integration tests).
- **Deployment**: Vercel (backend), Base Sepolia (testing).

---

## 📦 Repository Structure
```
/automa-buidl-ctc-2026
│── contracts/
│   └── EventWatcher.sol       # Smart contract to emit events
│── backend/
│   ├── index.js               # Entry point for the backend
│   ├── eventMonitor.js        # Monitors smart contract events
│   └── telegramBot.js         # Sends Telegram alerts
│── test/
│   ├── EventWatcher.test.js   # Unit tests for the smart contract
│   └── backend.test.js        # Integration tests for the backend
│── README.md                  # Project documentation
│── LICENSE                    # MIT License
│── .gitignore                 # Node.js and Solidity standards
│── package.json                # Project dependencies
```

---

## 🚀 Quick Start
### Prerequisites
- Node.js (v18+)
- npm or yarn
- A Telegram bot token (get it from [@BotFather](https://t.me/BotFather))
- A Base Sepolia RPC URL (e.g., from [Alchemy](https://www.alchemy.com/) or [Infura](https://infura.io/))

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ema750/automa-buidl-ctc-2026.git
   cd automa-buidl-ctc-2026
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Compile the smart contract:
   ```bash
   npx hardhat compile
   ```

4. Deploy the smart contract to Base Sepolia:
   ```bash
   npx hardhat run scripts/deploy.js --network base_sepolia
   ```

5. Configure the backend:
   - Create a `.env` file in the `backend/` directory with the following variables:
     ```env
     TELEGRAM_BOT_TOKEN=your_telegram_bot_token
     TELEGRAM_CHAT_ID=your_telegram_chat_id
     BASE_SEPOLIA_RPC_URL=your_base_sepolia_rpc_url
     CONTRACT_ADDRESS=your_deployed_contract_address
     ```

6. Start the backend:
   ```bash
   cd backend
   node index.js
   ```

7. Test the setup:
   - Interact with the smart contract to emit an event.
   - Check your Telegram chat for the alert.

---

## 📸 Demo
![Telegram Alert Demo](https://via.placeholder.com/600x400?text=Telegram+Alert+Demo+GIF)
*Example of a Telegram alert for a token transfer event.*

---

## 🌐 Live Demo
🔗 [Try the live demo here](https://example.com/demo) *(Coming soon!)*

---

## 📝 Submission
This project is submitted for the **BUIDL CTC 2026 Fall Hackathon** on DoraHacks. Below are the details for the submission:

### 📌 Submission Details
- **Project Name**: Base Smart Contract Event Watcher & Telegram Alert Service
- **Track**: Base Blockchain
- **Prize**: Grand Prize ($10,000)
- **Repository**: [ema750/automa-buidl-ctc-2026](https://github.com/ema750/automa-buidl-ctc-2026)
- **Demo Video**: [Watch the demo](https://example.com/demo-video) *(Coming soon!)*
- **Live Demo**: [Try it here](https://example.com/demo) *(Coming soon!)*

### 📋 Submission Checklist
- [x] Smart contract deployed on Base Sepolia.
- [x] Backend service monitoring events.
- [x] Telegram bot sending alerts.
- [x] Unit and integration tests.
- [x] Documentation (`README.md`).
- [ ] Live demo deployed.
- [ ] Demo video recorded.

---

## 🤝 Contributing
Contributions are welcome! Open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

---

## 📜 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact
For questions or feedback, reach out to:
- **GitHub**: [@ema750](https://github.com/ema750)
- **Telegram**: [@YourTelegramHandle](https://t.me/YourTelegramHandle)

---

## 🚀 Next Steps
1. Deploy a live demo of the service.
2. Record a demo video showcasing the functionality.
3. Submit the project on DoraHacks before **September 14, 2026**.

---