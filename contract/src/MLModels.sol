// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract MLModels {
    struct Model {
        uint256 timestamp;
        uint8 threatLevel;
        string ipAddress;
    }

    // The moderator is the person deploying the contract
    address public immutable moderator;

    // Array to store models
    Model[] private models;

    constructor() {
        moderator = msg.sender;
    }

    // Add a new model (only callable by moderator)
    function pushModel(
        uint256 timestamp,
        uint8 threatLevel,
        string memory ipAddress
    ) external {
        require(
            msg.sender == moderator,
            "Only the moderator can call this function"
        );

        models.push(
            Model({
                timestamp: timestamp,
                threatLevel: threatLevel,
                ipAddress: ipAddress
            })
        );
    }

    // Retrieve all models
    function getModels() external view returns (Model[] memory) {
        return models;
    }
}
