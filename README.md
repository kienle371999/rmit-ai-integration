# Integration of Etherum testnet and models

The phase 2 aims to integrate Ethereum testnet and machine learning models. The project is funded by RMIT research grants 🌳

## Install forge

```bash
curl -L https://foundry.paradigm.xyz | bash
```

## Deployment

```bash
forge create --rpc-url <your_rpc_url> --private-key <your_private_key> src/MLModels.sol:MLModels
```
