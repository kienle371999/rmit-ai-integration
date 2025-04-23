from flask import Flask, request, jsonify
from service import Service

app = Flask(__name__)

@app.post('/push-model')
def push_model():
    data = request.json
    timestamp = int(data['timestamp'])
    threat_level = int(data['threatLevel'])
    ip_address = data['ipAddress']

    service = Service()
    tx_hash = service.push_model(timestamp, threat_level, ip_address)

    return jsonify({
        'message': 'Model pushed successfully',
        'txHash': tx_hash
    }), 200

@app.get('/get-models')
def get_models():
    service = Service()
    return jsonify(service.get_models()), 200

