// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@gluwa/attestcoin-sdk/contracts/Attestcoin.sol";

contract AutomaVerifier {
    Attestcoin public attestcoin;
    address public owner;
    address public usdcAddress;

    constructor(address _attestcoin, address _usdcAddress) {
        attestcoin = Attestcoin(_attestcoin);
        owner = msg.sender;
        usdcAddress = _usdcAddress;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function verifyAndRelease(
        bytes32 attestationId,
        address payable recipient,
        uint256 amount
    ) external onlyOwner {
        require(
            attestcoin.verifyAttestation(attestationId),
            "Attestation not verified"
        );
        IERC20(usdcAddress).transfer(recipient, amount);
    }
}