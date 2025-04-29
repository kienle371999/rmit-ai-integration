// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract MLModels {
    struct Model {
        uint256 flowDuration;
        uint256 forwardPackets;
        uint256 backwardPackets;
        uint8 trueLabel;
        uint8 prediction;
        bool status;
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
        uint256 flowDuration,
        uint256 forwardPackets,
        uint256 backwardPackets,
        uint8 trueLabel,
        uint8 prediction,
        bool status
    ) external {
        require(
            msg.sender == moderator,
            "Only the moderator can call this function"
        );

        models.push(
            Model({
                flowDuration: flowDuration,
                forwardPackets: forwardPackets,
                backwardPackets: backwardPackets,
                trueLabel: trueLabel,
                prediction: prediction,
                status: status
            })
        );
    }

    // Retrieve all models
    function getModels() external view returns (Model[] memory) {
        return models;
    }
}
