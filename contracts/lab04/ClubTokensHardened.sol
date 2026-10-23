// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// @title ClubTokenAHardened - Nguồn cung cố định, bảo toàn tính bất biến
contract ClubTokenAHardened is ERC20 {
    constructor() ERC20("Club Token A", "CTA") {
        _mint(msg.sender, 1_000_000 * 10 ** decimals());
    }
}

/// @title ClubTokenBHardened - Khắc phục lỗi lạm phát vô hạn với trần tổng cung cứng (Max Supply Cap)
contract ClubTokenBHardened is ERC20, Ownable {
    uint256 public constant MAX_SUPPLY = 2_000_000 * 10 ** 18;

    event TokensMinted(address indexed to, uint256 amount);

    error MaxSupplyExceeded(uint256 requested, uint256 available);
    error ZeroAddress();
    error ZeroAmount();

    constructor() ERC20("Club Token B", "CTB") Ownable(msg.sender) {
        _mint(msg.sender, 1_000_000 * 10 ** decimals());
    }

    function mint(address to, uint256 amount) external onlyOwner {
        if (to == address(0)) revert ZeroAddress();
        if (amount == 0) revert ZeroAmount();
        if (totalSupply() + amount > MAX_SUPPLY) {
            revert MaxSupplyExceeded(amount, MAX_SUPPLY - totalSupply());
        }
        _mint(to, amount);
        emit TokensMinted(to, amount);
    }
}

/// @title ClubTokenCHardened - Danh sách hạn chế minh bạch, chặn hai chiều triệt tiêu bẫy Honeypot
contract ClubTokenCHardened is ERC20, Ownable {
    mapping(address => bool) public restricted;

    event RestrictionUpdated(address indexed account, bool status);

    error SenderRestricted(address account);
    error RecipientRestricted(address account);
    error ZeroAddress();

    constructor() ERC20("Club Token C", "CTC") Ownable(msg.sender) {
        _mint(msg.sender, 1_000_000 * 10 ** decimals());
    }

    function setRestricted(address user, bool status) external onlyOwner {
        if (user == address(0)) revert ZeroAddress();
        restricted[user] = status;
        emit RestrictionUpdated(user, status);
    }

    function _update(address from, address to, uint256 value) internal override {
        // Chặn đối xứng cả 2 chiều để loại bỏ hoàn toàn bẫy Honeypot một chiều
        if (from != address(0) && restricted[from]) {
            revert SenderRestricted(from);
        }
        if (to != address(0) && restricted[to]) {
            revert RecipientRestricted(to);
        }
        super._update(from, to, value);
    }
}
