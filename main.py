from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import hmac
import hashlib

app = Flask(__name__)

# Configuração robusta de CORS para evitar bloqueios no navegador
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# Garante que todos os cabeçalhos de permissão sejam enviados em cada resposta
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Variáveis configuradas no Render
INFINITE_TAG = os.environ.get("INFINITE_TAG", "glabpeplog")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "SEU_WEBHOOK_SECRET_AQUI")

@app.route('/gerar-link-pagamento', methods=['POST'])
def gerar_link():
    try:
        dados_pedido = request.json
        valor_total = dados_pedido.get('total')
        
        # Converte o valor para o formato decimal (ex: 345.87)
        valor_float = float(valor_total)

        # --- MÉTODO SEM TOKEN (Smart Checkout) ---
        # Cria o link direto: pay.infinitepay.io/SUA_TAG/VALOR
        link_pagamento = f"https://pay.infinitepay.io/{INFINITE_TAG}/{valor_float:.2f}"
        
        # Retorna o link para o seu site redirecionar o cliente
        return jsonify({"url": link_pagamento})

    except Exception as e:
        print(f"Erro no servidor: {str(e)}")
        return jsonify({"erro": str(e)}), 500

@app.route('/webhook/infinitepay', methods=['POST'])
def webhook_infinitepay():
    # 1. Verificação de Segurança (Assinatura)
    signature = request.headers.get('x-infinitepay-signature')
    payload = request.data
    
    if signature and WEBHOOK_SECRET != "SEU_WEBHOOK_SECRET_AQUI":
        hash_check = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(hash_check, signature):
            return jsonify({"status": "invalid signature"}), 401

    # 2. Processamento dos dados recebidos
    dados = request.json
    
    # Verifica se o pagamento foi aprovado
    if dados.get('status') in ['approved', 'paid']:
        valor_pago = dados.get('amount', 0) / 100
        order_id = dados.get('order_nsu', 'N/A')
        print(f"✅ PAGAMENTO CONFIRMADO!")
        print(f"Pedido: {order_id} | Valor: R$ {valor_pago:.2f}")
        
        # Aqui você poderá futuramente inserir o código de disparo de WhatsApp
    
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    # O Render define a porta automaticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
