from flask import Flask, request, jsonify
import requests
import hmac
import hashlib

app = Flask(__name__)

# Suas credenciais
INFINITE_TOKEN = "SEU_BEARER_TOKEN"
WEBHOOK_SECRET = "SEU_WEBHOOK_SECRET_INFINITEPAY" # Obtido no painel da InfinitePay

@app.route('/gerar-link-pagamento', methods=['POST'])
def gerar_link():
    # ... (mesmo código anterior para gerar o link)
    pass

@app.route('/webhook/infinitepay', methods=['POST'])
def webhook_infinitepay():
    # 1. Autenticação do Webhook (Segurança)
    # A InfinitePay envia um hash no cabeçalho para você validar
    signature = request.headers.get('x-infinitepay-signature')
    payload = request.data
    
    # Validação da assinatura (Opcional mas recomendado)
    if not validar_assinatura(payload, signature):
        return jsonify({"status": "invalid signature"}), 401

    dados = request.json
    status_pagamento = dados.get('status') # 'approved', 'payout', 'reversed', etc.
    valor = dados.get('amount')
    id_pedido = dados.get('metadata', {}).get('order_id')

    if status_pagamento == 'approved':
        print(f"✅ Pagamento do pedido {id_pedido} APROVADO! Valor: {valor}")
        # Aqui você pode disparar um bot de WhatsApp para o seu número avisando
        # ou atualizar seu banco de dados.
    
    return jsonify({"status": "received"}), 200

def validar_assinatura(payload, signature):
    # Lógica de validação HMAC conforme documentação da InfinitePay
    if not signature: return False
    hash_check = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(hash_check, signature)

if __name__ == '__main__':
    app.run(port=5000)