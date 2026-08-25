// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title Demo BUIDL CTC 2026 - AUTOMA
 * @notice Suite completa per demo su Base Sepolia:
 *         - MockUSDC: token ERC20 di test (in produzione: USDC reale)
 *         - MockAttestcoin: simulazione del protocollo Attestcoin di
 *           Creditcoin (in produzione: protocollo reale su Creditcoin)
 *         - AutomaVerifier: rilascia USDC su Base solo dopo verifica
 *           dell'attestazione cross-chain.
 */

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract MockUSDC {
    string public constant name = "USD Coin (test)";
    string public constant symbol = "USDC";
    uint8 public constant decimals = 6;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(uint256 _initialSupply) {
        totalSupply = _initialSupply;
        balanceOf[msg.sender] = _initialSupply;
        emit Transfer(address(0), msg.sender, _initialSupply);
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        require(balanceOf[msg.sender] >= amount, "saldo insufficiente");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }
}

contract MockAttestcoin {
    mapping(bytes32 => bool) public verified;

    event AttestationVerified(
        bytes32 indexed attestationId,
        string sourceChain,
        bytes data
    );

    /// @notice Simula la creazione di un'attestazione sul layer Creditcoin
    function createAttestation(
        bytes32 attestationId,
        string calldata sourceChain,
        bytes calldata data
    ) external {
        verified[attestationId] = true;
        emit AttestationVerified(attestationId, sourceChain, data);
    }

    /// @notice Verifica che un'attestazione esista ed e' valida
    function verifyAttestation(bytes32 attestationId)
        external
        view
        returns (bool)
    {
        return verified[attestationId];
    }
}

contract AutomaVerifier {
    IAttestcoin public attestcoin;
    address public owner;
    address public usdcAddress;

    mapping(bytes32 => bool) public alreadyReleased;

    event FundsReleased(
        bytes32 indexed attestationId,
        address indexed recipient,
        uint256 amount
    );

    error NotOwner();
    error AlreadyReleased();
    error AttestationNotVerified();

    constructor(address _attestcoin, address _usdc) {
        attestcoin = IAttestcoin(_attestcoin);
        usdcAddress = _usdc;
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    /// @notice Verifica l'attestazione cross-chain e rilascia i fondi
    ///         una sola volta per attestazione (protezione anti-replay).
    function verifyAndRelease(
        bytes32 attestationId,
        address recipient,
        uint256 amount
    ) external onlyOwner {
        if (alreadyReleased[attestationId]) revert AlreadyReleased();
        if (!attestcoin.verifyAttestation(attestationId)) {
            revert AttestationNotVerified();
        }
        alreadyReleased[attestationId] = true;
        emit FundsReleased(attestationId, recipient, amount);
        require(IERC20(usdcAddress).transfer(recipient, amount), "transfer fallito");
    }
}

interface IAttestcoin {
    function verifyAttestation(bytes32 attestationId)
        external
        view
        returns (bool);
}
