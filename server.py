from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Permette chiamate da qualsiasi dominio (fix CORS)

BREACH_RIP_BASE = 'https://www.breach.rip/api'
BREACH_RIP_KEY  = 'T44QdtP1r6QDS3HwvOpmDouVxHSTQPxf'
BREACH_VIP_BASE = 'https://breach.vip/api'
GHOSINT_BASE    = 'https://api.ghosint.io'
GHOSINT_KEY     = '3982a6571d1cea8961cc2abab6fc0a1e'

HEADERS_RIP = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-API-Key': BREACH_RIP_KEY
}
HEADERS_JSON = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# ── breach.rip proxy ──
@app.route('/proxy/breach-rip/<path:endpoint>', methods=['GET', 'POST'])
def proxy_breach_rip(endpoint):
    url = f"{BREACH_RIP_BASE}/{endpoint}"
    try:
        if request.method == 'POST':
            r = requests.post(url, json=request.get_json(), headers=HEADERS_RIP, timeout=10)
        else:
            r = requests.get(url, headers=HEADERS_RIP, params=request.args, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── breach.vip proxy ──
@app.route('/proxy/breach-vip/<path:endpoint>', methods=['GET', 'POST'])
def proxy_breach_vip(endpoint):
    url = f"{BREACH_VIP_BASE}/{endpoint}"
    try:
        if request.method == 'POST':
            r = requests.post(url, json=request.get_json(), headers=HEADERS_JSON, timeout=10)
        else:
            r = requests.get(url, headers=HEADERS_JSON, params=request.args, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── ghosint.io proxy ──
@app.route('/proxy/ghosint/<path:endpoint>', methods=['GET', 'POST'])
def proxy_ghosint(endpoint):
    url = f"{GHOSINT_BASE}/{endpoint}"
    try:
        body = request.get_json() or {}
        body['key'] = GHOSINT_KEY  # Inietta sempre la key
        if request.method == 'POST':
            r = requests.post(url, json=body, headers=HEADERS_JSON, timeout=15)
        else:
            r = requests.get(url, headers=HEADERS_JSON, params=request.args, timeout=15)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── Health check ──
@app.route('/')
def index():
    return jsonify({'status': 'ok', 'message': 'CsintX Proxy Server online'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
