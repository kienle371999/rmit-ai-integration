# Integration of Etherum testnet and models

The last phase aims to integrate Ethereum testnet and machine learning models. The project is funded by RMIT research grants 🌳

## Install forge

```bash
curl -L https://foundry.paradigm.xyz | bash
```

## Deployment

```bash
forge create --rpc-url <your_rpc_url> --private-key <your_private_key> src/MLModels.sol:MLModels
```

## Build server

```bash
flask --app app.py run --host=0.0.0.0 --port=8000
```
