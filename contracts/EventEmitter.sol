// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

contract EventEmitter {
    address public owner;

    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function deposit(uint256 amount) external payable {
        emit Deposit(msg.sender, amount);
    }

    function withdraw(uint256 amount) external {
        require(amount > 0, "Amount must be positive");
        emit Withdrawal(msg.sender, amount);
    }

    // Funzione di esempio per future estensioni (es. cambio owner)
    function transferOwnership(address newOwner) external onlyOwner {
        owner = newOwner;
    }
}