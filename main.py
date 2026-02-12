from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import hmac
import hashlib
import re

app = Flask(__name__)

# 1. CORS Total - Libera o acesso para o seu site no GitHub
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 2. Configurações
INFINITE_TAG = os.environ.get("INFINITE_TAG", "glabpeplog").replace('$', '').strip()
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "SEU_WEBHOOK_SECRET_AQUI")

@app.route('/gerar-link-pagamento', methods=['POST'])
def gerar_link():
    try:
        dados_pedido = request.json
        # Pega o total e remove TUDO que não for número, ponto ou vírgula
        total_cru = str(dados_pedido.get('total', '0'))
        
        # Lógica para limpar valores como "R$ 1.591,038" ou "412.59"
        # Mantém apenas números e a última vírgula ou ponto
        apenas_numeros = re.sub(r'[^\d,.]', '', total_cru)
        
        if ',' in apenas_numeros and '.' in apenas_numeros:
            # Se tem os dois (ex: 1.591,03), remove o ponto de milhar
            apenas_numeros = apenas_numeros.replace('.', '').replace(',', '.')
        elif ',' in apenas_numeros:
            # Se tem só vírgula, troca por ponto
            apenas_numeros = apenas_numeros.replace(',', '.')

        valor_final = float(apenas_numeros)

        # TRAVA DE SEGURANÇA: Se o site mandar "4125915", ele vira "412.59"
        # Links da InfinitePay não funcionam com valores gigantes
        if valor_final > 10000:
             valor_final = valor_final / 100
             # Se ainda for gigante, divide de novo (proteção contra erro do site)
             if valor_final > 10000:
                 valor_final = valor_final / 100

        # Gerar o link oficial que trava o valor
        link_pagamento = f"https://pay.infinitepay.io/{INFINITE_TAG}/{valor_final:.2f}"
        
        print(f"✅ LINK GERADO: {link_pagamento}")
        return jsonify({"url": link_pagamento})

    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        return jsonify({"erro": "Erro ao processar valor"}), 400

@app.route('/webhook/infinitepay', methods=['POST'])
def webhook_infinitepay():
    signature = request.headers.get('x-infinitepay-signature')
    payload = request.data
    if signature:
        hash_check = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(hash_check, signature):
            return jsonify({"status": "invalid signature"}), 401

    dados = request.json
    if dados and dados.get('status') in ['approved', 'paid']:
        print(f"💰 PAGAMENTO APROVADO: {dados.get('order_nsu')}")
    
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
