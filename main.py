from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import hmac
import hashlib

app = Flask(__name__)

# 1. MANTIDO: Configuração de CORS completa
# Isso é o que impede o erro que você viu ao entrar no site
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 2. MANTIDO: Suas chaves originais do Render
INFINITE_TOKEN = os.environ.get("INFINITE_TOKEN", "glabpeplog")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "SEU_WEBHOOK_SECRET_AQUI")
INFINITE_TAG = os.environ.get("INFINITE_TAG", "glabpeplog")

@app.route('/gerar-link-pagamento', methods=['POST'])
def gerar_link():
    try:
        dados_pedido = request.json
        valor_total = dados_pedido.get('total')
        nome_cliente = dados_pedido.get('nome')

        # 3. MANTIDO: Tratamento de valor
        # Remove R$, espaços e ajusta pontos/vírgulas para o padrão numérico
        valor_limpo = str(valor_total).replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
        valor_float = float(valor_limpo)

        # 4. CORREÇÃO FINAL DA URL:
        # Removemos o '$' que apareceu no seu WhatsApp e estava quebrando o link
        # O padrão oficial para o seu perfil 'linknabio' é este abaixo:
        tag_ajustada = INFINITE_TAG.replace('$', '')
        link_pagamento = f"https://linknabio.gg/{tag_ajustada}"
        
        # Se você quiser testar o formato pay.infinitepay, use a linha abaixo:
        # link_pagamento = f"https://pay.infinitepay.io/{tag_ajustada}/{valor_float:.2f}"
        
        print(f"DEBUG: Link enviado ao cliente {nome_cliente}: {link_pagamento}")

        return jsonify({"url": link_pagamento})

    except Exception as e:
        print(f"ERRO NO SERVIDOR: {str(e)}")
        return jsonify({"erro": str(e)}), 500

@app.route('/webhook/infinitepay', methods=['POST'])
def webhook_infinitepay():
    # 5. MANTIDO: Segurança da Assinatura original
    signature = request.headers.get('x-infinitepay-signature')
    payload = request.data
    
    if signature:
        hash_check = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(hash_check, signature):
            return jsonify({"status": "invalid signature"}), 401

    # 6. MANTIDO: Processamento de confirmação de pagamento
    dados = request.json
    if dados.get('status') in ['approved', 'paid']:
        print(f"✅ PAGAMENTO APROVADO! NSU: {dados.get('order_nsu')}")
    
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
