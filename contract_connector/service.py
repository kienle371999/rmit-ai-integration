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
                        "name": "timestamp",
                        "type": "uint256",
                        "internalType": "uint256"
                    },
                    {
                        "name": "threatLevel",
                        "type": "uint8",
                        "internalType": "uint8"
                    },
                    {
                        "name": "ipAddress",
                        "type": "string",
                        "internalType": "string"
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
                    "name": "timestamp",
                    "type": "uint256",
                    "internalType": "uint256"
                },
                {
                    "name": "threatLevel",
                    "type": "uint8",
                    "internalType": "uint8"
                },
                {
                    "name": "ipAddress",
                    "type": "string",
                    "internalType": "string"
                }
                ],
                "outputs": [],
                "stateMutability": "nonpayable"
            }
        ]
        self.contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)

    def push_model(self, time, threat_level, ip_address):
        tx = self.contract.functions.pushModel(time, threat_level, ip_address).build_transaction({
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
        return models