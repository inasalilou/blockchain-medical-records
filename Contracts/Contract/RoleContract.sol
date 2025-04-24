// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract RoleContract is ReentrancyGuard {

    struct Role{
        bool isAssigned;
        uint _role;
    }
    // Mappings
    mapping(address => Role) public roles;

    function assignRole(address _user, uint _role) external nonReentrant {
        require(!roles[_user].isAssigned, "User already registered");
       // require(_role <= 2, "Role must be 0, 1, or 2"); // <-- Ajoutez cette ligne
        roles[_user] = Role({
            isAssigned: true,
            _role: _role
        });
    }

    function isUserAssigned(address _user) public view returns (bool) {
        return roles[_user].isAssigned;
    }

    function checkRole(address _user) public view returns (uint) {
        return roles[_user]._role;
    }

}