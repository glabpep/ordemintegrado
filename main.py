from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import hmac
import hashlib

app = Flask(__name__)

# 1. MANTIDO: Configuração de CORS completa
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 2. MANTIDO: Suas chaves originais
INFINITE_TAG = os.environ.get("INFINITE_TAG", "glabpeplog").replace('$', '')
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "SEU_WEBHOOK_SECRET_AQUI")

@app.route('/gerar-link-pagamento', methods=['POST'])
def gerar_link():
    try:
        dados_pedido = request.json
        valor_total = str(dados_pedido.get('total', '0'))
        
        # --- CORREÇÃO DO VALOR ---
        # Remove R$, espaços e pontos de milhar. Garante que a vírgula vire ponto decimal.
        valor_limpo = valor_total.replace('R$', '').replace(' ', '').replace('.', '')
        valor_limpo = valor_limpo.replace(',', '.')
        
        valor_final = float(valor_limpo)

        # --- URL DE CHECKOUT DIRETO ---
        # Usando o domínio 'pay.infinitepay.io' que aceita valor cravado na URL
        link_pagamento = f"https://pay.infinitepay.io/{INFINITE_TAG}/{valor_final:.2f}"
        
        print(f"DEBUG: Link Gerado: {link_pagamento}")
        return jsonify({"url": link_pagamento})

    except Exception as e:
        print(f"ERRO: {str(e)}")
        return jsonify({"erro": str(e)}), 500

@app.route('/webhook/infinitepay', methods=['POST'])
def webhook_infinitepay():
    signature = request.headers.get('x-infinitepay-signature')
    payload = request.data
    if signature:
        hash_check = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(hash_check, signature):
            return jsonify({"status": "invalid signature"}), 401

    dados = request.json
    if dados.get('status') in ['approved', 'paid']:
        print(f"✅ PAGAMENTO APROVADO: {dados.get('order_nsu')}")
    
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
