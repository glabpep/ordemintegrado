from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import hmac
import hashlib

app = Flask(__name__)

# Configuração de CORS idêntica à que você já aprovou
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# PREENCHIDO COM SEUS DADOS ORIGINAIS
INFINITE_TOKEN = os.environ.get("INFINITE_TOKEN", "glabpeplog")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "SEU_WEBHOOK_SECRET_AQUI")
INFINITE_TAG = os.environ.get("INFINITE_TAG", "glabpeplog")

@app.route('/gerar-link-pagamento', methods=['POST'])
def gerar_link():
    try:
        dados_pedido = request.json
        valor_total = dados_pedido.get('total')
        nome_cliente = dados_pedido.get('nome')

        # Converte para float para garantir que o link seja gerado corretamente
        valor_float = float(valor_total)

        # MÉTODO DE LINK DIRETO (Para funcionar sem o Bearer Token que a InfinitePay não deu)
        # O link levará para: https://pay.infinitepay.io/glabpeplog/VALOR
        link_pagamento = f"https://pay.infinitepay.io/{INFINITE_TAG}/{valor_float:.2f}"
        
        return jsonify({"url": link_pagamento})

    except Exception as e:
        print(f"Erro no servidor: {str(e)}")
        return jsonify({"erro": str(e)}), 500

@app.route('/webhook/infinitepay', methods=['POST'])
def webhook_infinitepay():
    # 1. Verificação de Segurança (Assinatura)
    signature = request.headers.get('x-infinitepay-signature')
    payload = request.data
    
    if signature:
        # Usa o seu WEBHOOK_SECRET configurado acima
        hash_check = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(hash_check, signature):
            return jsonify({"status": "invalid signature"}), 401

    # 2. Processamento dos dados recebidos (Conforme seu original)
    dados = request.json
    
    if dados.get('status') in ['approved', 'paid']:
        valor_pago = dados.get('amount', 0) / 100
        order_id = dados.get('order_nsu')
        print(f"✅ PAGAMENTO CONFIRMADO!")
        print(f"Pedido: {order_id} | Valor: R$ {valor_pago:.2f}")
    
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    # Porta padrão do Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
