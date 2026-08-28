// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EventEmitter {
    event Deposit(address indexed user, uint256 amount);

    function deposit() external payable {
        emit Deposit(msg.sender, msg.value);
    }
}
