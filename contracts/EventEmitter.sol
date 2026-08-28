// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EventEmitter {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Mint(address indexed to, uint256 amount);
    event AlertTriggered(string message, uint256 timestamp);

    function emitTestEvents() external {
        emit Transfer(msg.sender, address(0), 100);
        emit Mint(msg.sender, 1000);
        emit AlertTriggered("Test alert from EventEmitter", block.timestamp);
    }
}