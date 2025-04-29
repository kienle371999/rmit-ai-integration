from web3 import Web3
from dotenv import load_dotenv
import os

# Load variables from .env file into the environment
load_dotenv()

class Service:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('NODE_PROVIDER')))
        self.account = self.w3.eth.account.from_key(os.getenv('SECRET_KEY'))
        contract_address = Web3.to_checksum_address(os.getenv('CONTRACT_ADDRESS'))
        contract_abi = [
            {
                "type": "constructor",
                "inputs": [],
                "stateMutability": "nonpayable"
            },
            {
                "type": "function",
                "name": "getModels",
                "inputs": [],
                "outputs": [
                {
                    "name": "",
                    "type": "tuple[]",
                    "internalType": "struct MLModels.Model[]",
                    "components": [
                    {
                        "name": "flowDuration",
                        "type": "uint256",
                        "internalType": "uint256"
                    },
                    {
                        "name": "forwardPackets",
                        "type": "uint256",
                        "internalType": "uint256"
                    },
                    {
                        "name": "backwardPackets",
                        "type": "uint256",
                        "internalType": "uint256"
                    },
                    {
                        "name": "trueLabel",
                        "type": "uint8",
                        "internalType": "uint8"
                    },
                    {
                        "name": "prediction",
                        "type": "uint8",
                        "internalType": "uint8"
                    },
                    {
                        "name": "status",
                        "type": "bool",
                        "internalType": "bool"
                    }
                    ]
                }
                ],
                "stateMutability": "view"
            },
            {
                "type": "function",
                "name": "moderator",
                "inputs": [],
                "outputs": [
                {
                    "name": "",
                    "type": "address",
                    "internalType": "address"
                }
                ],
                "stateMutability": "view"
            },
            {
                "type": "function",
                "name": "pushModel",
                "inputs": [
                {
                    "name": "flowDuration",
                    "type": "uint256",
                    "internalType": "uint256"
                },
                {
                    "name": "forwardPackets",
                    "type": "uint256",
                    "internalType": "uint256"
                },
                {
                    "name": "backwardPackets",
                    "type": "uint256",
                    "internalType": "uint256"
                },
                {
                    "name": "trueLabel",
                    "type": "uint8",
                    "internalType": "uint8"
                },
                {
                    "name": "prediction",
                    "type": "uint8",
                    "internalType": "uint8"
                },
                {
                    "name": "status",
                    "type": "bool",
                    "internalType": "bool"
                }
                ],
                "outputs": [],
                "stateMutability": "nonpayable"
            }
        ]
        self.contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
    
    def push_model_output(self, data):
        flow_duration = int(data['flowDuration'])
        forward_packets = int(data['forwardPackets'])
        backward_packets = int(data['backwardPackets'])
        true_label = int(data['trueLabel'])
        prediction = int(data['prediction'])
        status = bool(data['status'])

        tx = self.contract.functions.pushModel(
            flow_duration,
            forward_packets,
            backward_packets,
            true_label,
            prediction,
            status
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 300000,
            'gasPrice': self.w3.eth.gas_price,
            'chainId': 11155111 # Sepolia ID
        })
        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.transactionHash.hex()
    
    def get_models(self):
        models = self.contract.functions.getModels().call()
        json_models = []

        for model in models:
            json_model = {
                'flowDuration': model[0],
                'forwardPackets': model[1],
                'backwardPackets': model[2],
                'trueLabel': model[3],
                'prediction': model[4],
                'status': model[5]
            }
            json_models.append(json_model)

        return json_models
    
