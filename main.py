from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import hmac
import hashlib

app = Flask(__name__)

# 1. MANTIDO: Configuração de CORS completa para evitar erros no navegador
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 2. MANTIDO: Seus dados originais e variáveis do Render
INFINITE_TOKEN = os.environ.get("INFINITE_TOKEN", "glabpeplog")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "SEU_WEBHOOK_SECRET_AQUI")
INFINITE_TAG = os.environ.get("INFINITE_TAG", "glabpeplog")

@app.route('/gerar-link-pagamento', methods=['POST'])
def gerar_link():
    try:
        dados_pedido = request.json
        valor_total = dados_pedido.get('total')
        nome_cliente = dados_pedido.get('nome')

        # 3. CORREÇÃO CRUCIAL: Garante que o valor vire um número decimal correto para a InfinitePay
        # Se vier "1.591,038" do site, precisamos converter para 1591.04
        valor_limpo = str(valor_total).replace('.', '').replace(',', '.')
        valor_float = float(valor_limpo)

        # 4. MANTIDO: Payload completo conforme seu código original (caso consiga o token depois)
        # Por enquanto, geramos o link direto que funciona sem token
        link_pagamento = f"https://pay.infinitepay.io/{INFINITE_TAG}/{valor_float:.2f}"
        
        # Log para você conferir no Render se o link está saindo certo
        print(f"Link gerado para {nome_cliente}: {link_pagamento}")

        return jsonify({"url": link_pagamento})

    except Exception as e:
        print(f"Erro no servidor: {str(e)}")
        return jsonify({"erro": str(e)}), 500

@app.route('/webhook/infinitepay', methods=['POST'])
def webhook_infinitepay():
    # 5. MANTIDO: Verificação de Segurança (Assinatura) original
    signature = request.headers.get('x-infinitepay-signature')
    payload = request.data
    
    if signature:
        hash_check = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(hash_check, signature):
            return jsonify({"status": "invalid signature"}), 401

    # 6. MANTIDO: Processamento dos dados recebidos original
    dados = request.json
    
    if dados.get('status') in ['approved', 'paid']:
        valor_pago = dados.get('amount', 0) / 100
        order_id = dados.get('order_nsu')
        print(f"✅ PAGAMENTO CONFIRMADO!")
        print(f"Pedido: {order_id} | Valor: R$ {valor_pago:.2f}")
    
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
