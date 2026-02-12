from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import hmac
import hashlib

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# O Render vai ler essas chaves das 'Environment Variables' que configuramos
INFINITE_TOKEN = os.environ.get("INFINITE_TOKEN", "glabpeplog")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "SEU_WEBHOOK_SECRET_AQUI")
INFINITE_TAG = os.environ.get("INFINITE_TAG", "glabpeplog")

@app.route('/gerar-link-pagamento', methods=['POST'])
def gerar_link():
    try:
        dados_pedido = request.json
        valor_total = dados_pedido.get('total')
        nome_cliente = dados_pedido.get('nome')

        # Montando o payload conforme a documentação interativa que você enviou
        payload = {
            "handle": INFINITE_TAG,
            "order_nsu": f"GLAB-{os.urandom(3).hex().upper()}",
            "amount": int(float(valor_total) * 100), # Valor total em centavos
            "itens": [
                {
                    "description": f"Pedido G-LAB - {nome_cliente}",
                    "quantity": 1,
                    "price": int(float(valor_total) * 100)
                }
            ],
            # Opcional: Para onde o cliente vai após pagar
            "redirect_url": "https://seusite.com/obrigado", 
            # URL do seu serviço no Render para receber confirmação automática
            "webhook_url": f"https://{request.host}/webhook/infinitepay"
        }

        headers = {
            "Authorization": f"Bearer {INFINITE_TOKEN}",
            "Content-Type": "application/json"
        }

        # Rota oficial de checkout da documentação
        url_api = "https://api.infinitepay.io/invoices/public/checkout/links"
        
        response = requests.post(url_api, json=payload, headers=headers)
        res_data = response.json()

        if response.status_code in [200, 201]:
            # Retornamos a URL para o site abrir
            return jsonify({"url": res_data.get('url')})
        else:
            print(f"Erro na API: {res_data}")
            return jsonify({"erro": "Erro na InfinitePay", "details": res_data}), 400

    except Exception as e:
        print(f"Erro no servidor: {str(e)}")
        return jsonify({"erro": str(e)}), 500

@app.route('/webhook/infinitepay', methods=['POST'])
def webhook_infinitepay():
    # 1. Verificação de Segurança (Assinatura)
    signature = request.headers.get('x-infinitepay-signature')
    payload = request.data
    
    if signature:
        hash_check = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(hash_check, signature):
            return jsonify({"status": "invalid signature"}), 401

    # 2. Processamento dos dados recebidos
    dados = request.json
    
    # Na rota de checkout/links, o status de aprovado vem como 'paid' ou 'approved'
    # dependendo da versão. Verificamos se há sucesso.
    if dados.get('status') in ['approved', 'paid']:
        valor_pago = dados.get('amount', 0) / 100
        order_id = dados.get('order_nsu')
        print(f"✅ PAGAMENTO CONFIRMADO!")
        print(f"Pedido: {order_id} | Valor: R$ {valor_pago:.2f}")
        
        # TODO: Adicione aqui seu código para disparar o WhatsApp de aviso
    
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    # No Render a porta é definida automaticamente pela variável PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


