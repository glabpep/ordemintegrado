import pandas as pd
import os
import json

def gerar_site_vendas_completo():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Busca o arquivo de dados
    arquivo_dados = None
    for nome in ['stock_0202.xlsx', 'stock_2901.xlsx - Plan1.csv']:
        caminho = os.path.join(diretorio_atual, nome)
        if os.path.exists(caminho):
            arquivo_dados = caminho
            break

    if not arquivo_dados:
        print(f"Erro: Arquivo não encontrado em: {diretorio_atual}")
        return

    # Dicionário de informações técnicas integral
    infos_tecnicas = {
        "5-AMINO": "Inibidor Seletivo de NNMT: Atua bloqueando a enzima nicotinamida N-metiltransferase, o que eleva os níveis de NAD+ e SAM intracelular. Indica eficácia na reversão da obesidade e otimização do gasto energético basal.",
        "AICAR": "Ativador de AMPK: Mimetiza o AMP intracelular para ativar a proteína quinase. Investigado por aumentar a captação de glicose muscular, a oxidação de ácidos graxos e a resistência cardiovascular.",
        "AOD 9604": "Análogo Lipolítico do hGH: Focado no isolamento das propriedades de queima de gordura do GH sem induzir efeitos hiperglicêmicos. Aplicado em estudos de obesidade e regeneração de cartilagem.",
        "HGH FRAGMENT": "Modulador de Lipídios: Parte terminal do GH responsável pela quebra de gordura. Mostra capacidade de inibir a formação de nova gordura e acelerar a lipólise visceral sem alterar a insulina.",
        "L-CARNITINE": "Cofator de Transporte Mitocondrial: Essencial para o transporte de ácidos graxos para a matriz mitocondrial (β-oxidação). Reduz a fadiga muscular e suporta a performance atlética.",
        "MOTS-C": "Peptídeo Derivado da Mitocôndria: Regulador hormonal do metabolismo sistêmico. Melhora a homeostase da glicose e combate a resistência à insulina via ativação da via AMPK.",
        "SLU PP": "Agonista Pan-ERR (Pílula do Exercício): Ativa receptores ERRα, β, γ. Aumenta drasticamente a biogênese mitocondrial e a resistência física, comparável ao treino de alta intensidade.",
        "LIPO C": "Mix Lipotrópico Injetável: Composto por Metionina, Inositol e Colina. Atua na exportação de gorduras do fígado e na otimização da mobilização lipídica sistêmica.",
        "CJC-1295": "Secretagogo de GH de Longa Duração: Análogo do GHRH que aumenta secreção de GH e IGF-1. Aplicado em antienvelhecimento, melhora da composição corporal e síntese proteica acelerada.",
        "IPAMORELIN": "Agonista de Grelina Seletivo: Estimula a liberação pulsátil de GH sem elevar cortisol ou prolactina. Seguro para indução de anabolismo e melhora da density mineral óssea.",
        "CJC-1295 + IPAMORELIN": "Sinergia Hormonal Dual: Combinação de GHRH com GHRP. Mimetiza a liberação fisiológica natural, resultando em secreção de GH significativamente maior que o uso isolado.",
        "GHRP-6": "Peptídeo Liberador de GH: Estimula a hipófise e aumenta a sinalização da fome via grelina. Focado em recuperação de tecidos, aumento de massa bruta e estados catabólicos.",
        "HEXARELIN": "Potencializador de Força: Secretagogo potente da classe GHRP. Aumenta a força contrátil cardíaca e muscular, protegendo o miocárdio e promovendo volume fibroso.",
        "IGF-1 LR3": "Análogo de IGF-1 de Meia-vida Longa: Permanece ativo por até 20 horas. Principal mediador da hiperplasia (criação de novas fibras musculares) e transporte de acesso de aminoácidos.",
        "IGF DES": "Variante de IGF-1 de Ação Local: Afinidade 10x maior pelos receptores. Ideal para aplicação pós-treino visando recuperação imediata e crescimento muscular localizado.",
        "SERMORELIN": "Estimulador de Eixo Natural: Mimetiza o GHRH natural. Promove melhorias na qualidade do sono profundo, vitalidade da pele e recuperação pós-esforço.",
        "MK-677": "Secretagogo Oral (Ibutamoren): Agonista dos receptores de grelina. Aumenta sustentadamente os níveis de GH e IGF-1, aumentando a massa livre de gordura e densidade óssea.",
        "BPC-157": "Pentadecapeptídeo Gástrico: Acelera a angiogênese e cicatrização. Estudado para cura de rupturas de tendões, ligamentos, danos musculares e tecidos moles.",
        "BPC-157 ORAL": "Modulador Gastrointestinal: Versão estável em suco gástrico. Focado no tratamento de Doença de Crohn, SII, úlceras e restauração da barreira intestinal.",
        "TB-500": "Timosina Beta-4 Sintética: Essencial para migração celular e reparo de tecidos. Promove formação de novos vasos e reduz inflamação articular e miocárdica.",
        "TB-500 + BPC": "Protocolo de Reparo Total: União sinérgica do TB-500 (sistêmico) com BPC-157 (tecido). Padrão ouro para recuperação de lesões atléticas graves.",
        "GHK-CU": "Complexo Peptídeo-Cobre: Atua na remodelação do DNA e síntese de colágeno I e III. Possui propriedades antioxidantes e anti-inflamatórias para pele e tecidos conectivos.",
        "GLOW": "Bioestimulação Dérmica (GHK-Cu + BPC + TB): Blend estético-regenerativo focado em rejuvenescimento cutâneo, redução de cicatrizes e regeneração da matriz extracelular.",
        "ARA 290": "Agonista de Receptor de Reparo Inato: Derivado da eritropoietina sem efeitos hematológicos. Pesquisado para dor neuropática severa e regeneração nervosa periférica.",
        "KPV": "Tripeptídeo Anti-inflamatório: Inibe vias inflamatórias (NF-κB). Possui propriedades antimicrobianas e é utilizado em estudos sobre dermatite e colite.",
        "LL-37": "Peptídeo Antimicrobiano: Parte do sistema imune inato. Neutraliza endotoxinas bacterianas, modula a resposta inflamatória e acelera cicatrização de feridas infectadas.",
        "KLOW": "Quarteto de Reparo Profundo (GHK+BPC+TB+KPV): Projetado para sinalização celular máxima em remodelação de tecidos complexos e equilíbrio imunológico.",
        "TIRZEPATIDE": "Agonista Dual GIP/GLP-1: Supera a Semaglutida na perda de peso. Promove saciedade central e melhora drástica na sensibilidade à insulina.",
        "RETATRUTIDE": "Agonista Triplo (GIP/GLP-1/GCGR): Aumenta o gasto calórico basal e a oxidação de gordura no fígado. Promete perdas de peso superiores a 24%.",
        "SEMAGLUTIDE": "Agonista de GLP-1: Retarda o esvaziamento gástrico e sinaliza saciedade ao hipotálamo. Base para tratamento de obesidade e controle glicêmico.",
        "SELANK": "Ansiolítico Regulador: Modula serotonina e norepinefrina. Reduz ansiedade e melhora o foco cognitivo sem o efeito sedativo dos ansiolíticos comuns.",
        "SEMAX": "Nootrópico Neuroprotetor: Eleva níveis de BDNF e NGF no hipocampo. Aplicado em recuperação pós-AVC e otimização do aprendizado sob estresse.",
        "PINEALON": "Bioregulador de Cadeia Curta: Atua na expressão gênica neuronal. Restaura o ritmo circadiano e protege contra o estresse oxidativo cerebral.",
        "NAD+": "Coenzima de Vitalidade: Essencial para reparação do DNA e sirtuínas. Associado à reversão de marcadores de envelhecimento e aumento da energia celular.",
        "METHYLENE BLUE": "Otimizador Mitocondrial (Azul de Metileno): Transportador alternativo de elétrons. Melhora a memória de curto prazo e protege contra neurodegeneração.",
        "DSIP": "Indutor de Sono Delta: Neuromodulador que sincroniza ritmos biológicos, promove sono profundo e mitiga sintomas de estresse emocional.",
        "OXYTOCIN": "Neuromodulador Social: Regula confiança, redução de medo e ansiedade social. Explorado também na regulação do apetite por carboidratos.",
        "EPITHALON": "Ativador da Telomerase: Induz o alongamento dos telômeros. Focado na extensão da vida celular e restauração da secreção de melatonina.",
        "KISSPEPTIN": "Regulador de Eixo HPG: Atua no hipotálamo para restaurar a produção natural de testosterona e regular a função reprodutiva de forma fisiológica.",
        "MELANOTAN 1": "Agonista de Melanocortina Seletivo: Estimula a liberação de melanina com alta segurança e proteção contra danos UV.",
        "MELANOTAN 2": "Bronzeamento e Libido: Atua no SNC aumentando a pigmentação da pele, elevando o desejo sexual e reduzindo o apetite.",
        "PT-141": "Tratamento de Disfunção Sexual: Atua via SNC nos centros de excitação do cérebro. Indicado para desejo sexual hipoativo.",
        "VITAMIN B-12": "Metilcobalamina de Alta Potência: Essencial para a bainha de mielina, produção de glóbulos vermelhos e prevenção da fadiga neuromuscular.",
        "BACTERIOSTIC WATER": "Solvente Bacteriostático: Água com 0,9% de Álcool Benzílico. Impede proliferação bacteriana, permitindo uso seguro por até 30 dias.",
        "SS-31": "Protetor de Cardiolipina: Previne a formação de radicais livres na mitocôndria e restaura a produção de ATP.",
        "HYALURONIC ACID 2% + GHK": "Arquitetura Extracelular: Une hidratação profunda (HA) com sinalização regenerativa (GHK).",
        "HCG": "Mimetizador de LH: Sinaliza aos testículos a produção de testosterona. Vital para prevenir atrofia testicular e reinício do eixo hormonal (TPC).",
        "HEMP OIL": "Suporte Fitocanabinoide: Propriedades analgésicas e anti-inflamatórias. Suporta o sistema endocanabinoide.",
        "TESAMORELIN": "Redutor de Lipodistrofia: Único aprovado para reduzir gordura visceral abdominal severa."
    }

    try:
        if arquivo_dados.endswith('.xlsx'):
            df = pd.read_excel(arquivo_dados)
        else:
            df = pd.read_csv(arquivo_dados)
        df.columns = [str(col).strip() for col in df.columns]
        
        produtos_base = []
        for idx, row in df.iterrows():
            nome_prod = str(row.get('PRODUTO', 'N/A')).strip()
            info_prod = "Informação técnica detalhada não disponível para este item."
            for chave, texto in infos_tecnicas.items():
                if chave in nome_prod.upper():
                    info_prod = texto
                    break

            produtos_base.append({
                "id": idx,
                "nome": nome_prod,
                "espec": f"{row.get('VOLUME', '')} {row.get('MEDIDA', '')}".strip(),
                "preco": float(row.get('Preço (R$)', 0)),
                "info": info_prod
            })
        js_produtos = json.dumps(produtos_base)
        
    except Exception as e:
        print(f"Erro ao ler os dados: {e}")
        return

    html_template = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>G-LAB PEPTIDES - Pedidos</title>
        <style>
            :root {{ --primary: #004a99; --secondary: #28a745; --danger: #dc3545; --bg: #f4f7f9; }}
            body {{ font-family: 'Segoe UI', Roboto, sans-serif; background: var(--bg); margin: 0; padding: 0; color: #333; }}
            .container {{ max-width: 900px; margin: auto; background: white; min-height: 100vh; padding: 15px; box-sizing: border-box; padding-bottom: 220px; }}
            
            .header-logo-container {{ text-align: center; padding: 10px 0; }}
            .header-logo {{ max-width: 250px; height: auto; }}
            .subtitle {{ text-align: center; color: #666; font-size: 0.9rem; margin-bottom: 20px; font-weight: 500; }}
            
            /* NOVOS ALERTAS SOLICITADOS */
            .info-alert-card {{ background: #fff3cd; border: 1px solid #ffeeba; color: #856404; padding: 15px; border-radius: 12px; margin-bottom: 10px; position: relative; font-size: 0.9rem; line-height: 1.4; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
            .lote-alert-card {{ background: #e3f2fd; border: 1px solid #bbdefb; color: #0d47a1; padding: 15px; border-radius: 12px; margin-bottom: 20px; font-size: 0.9rem; line-height: 1.4; font-weight: bold; border-left: 5px solid #2196f3; }}
            .close-alert {{ position: absolute; top: 10px; right: 10px; cursor: pointer; font-weight: bold; font-size: 1.2rem; }}
            
            .frete-card {{ background: #fff; border: 2px solid var(--primary); padding: 15px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
            .table-container {{ overflow-x: auto; border-radius: 8px; border: 1px solid #eee; }}
            table {{ width: 100%; border-collapse: collapse; background: white; min-width: 400px; }}
            th {{ background: var(--primary); color: white; padding: 12px 8px; text-align: left; font-size: 0.85rem; }}
            td {{ padding: 12px 8px; border-bottom: 1px solid #f0f0f0; font-size: 0.9rem; }}
            .status-disponivel {{ color: var(--secondary); font-weight: bold; }}
            .status-espera {{ color: var(--danger); font-weight: bold; background: #fff5f5; padding: 4px 8px; border-radius: 4px; border: 1px solid var(--danger); display: inline-block; }}
            .input-style {{ padding: 12px; border: 1px solid #ccc; border-radius: 8px; width: 100%; box-sizing: border-box; font-size: 16px; }}
            .btn-add {{ background: var(--secondary); color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; }}
            .btn-add:disabled {{ background: #eee; color: #999; cursor: not-allowed; }}
            .btn-info {{ background: none; border: none; color: var(--primary); font-size: 0.75rem; text-decoration: underline; cursor: pointer; padding: 0; margin-top: 5px; font-weight: bold; }}
            
            .cart-panel {{ position: fixed; bottom: 0; left: 0; right: 0; background: var(--primary); color: white; padding: 15px; border-radius: 20px 20px 0 0; z-index: 1000; display: none; box-shadow: 0 -5px 20px rgba(0,0,0,0.3); max-height: 80vh; overflow-y: auto; }}
            @media (min-width: 768px) {{ .cart-panel {{ width: 400px; left: auto; right: 20px; bottom: 20px; border-radius: 20px; }} }}
            .cart-list {{ margin: 10px 0; max-height: 150px; overflow-y: auto; background: rgba(255,255,255,0.1); border-radius: 8px; padding: 5px; }}
            .cart-item {{ display: flex; justify-content: space-between; padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 0.85rem; align-items: center; }}
            .btn-remove {{ background: #ff4444; border: none; color: white; cursor: pointer; font-weight: bold; border-radius: 4px; padding: 2px 8px; margin-left: 10px; }}
            .coupon-section {{ display: flex; gap: 5px; margin: 10px 0; }}
            .coupon-input {{ flex: 1; padding: 8px; border-radius: 5px; border: none; font-size: 0.8rem; color: #333; }}
            .btn-coupon {{ background: #ffeb3b; color: #333; border: none; padding: 8px 12px; border-radius: 5px; font-weight: bold; cursor: pointer; font-size: 0.8rem; }}
            .ship-row {{ display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; color: #ffeb3b; margin-top: 5px; font-weight: bold; }}
            .total-row {{ display: flex; justify-content: space-between; font-size: 1.1rem; font-weight: bold; margin: 5px 0; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 10px; }}
            .discount-line {{ display: none; justify-content: space-between; color: #ffeb3b; font-size: 0.9rem; margin-bottom: 5px; }}
            .btn-checkout-final {{ background: white; color: var(--primary); border: none; width: 100%; padding: 14px; border-radius: 12px; font-weight: bold; font-size: 1rem; cursor: pointer; margin-top: 5px; }}
            
            .modal {{ display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); overflow-y: auto; }}
            .modal-content {{ background: white; margin: 5% auto; padding: 20px; width: 95%; max-width: 500px; border-radius: 15px; box-sizing: border-box; text-align: center; }}
            .modal-info-body {{ background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid var(--primary); margin: 15px 0; font-size: 0.95rem; line-height: 1.5; text-align: left; }}
            .prod-img-modal {{ max-width: 250px; height: auto; border-radius: 10px; margin: 0 auto 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: none; }}
            .form-group {{ margin-bottom: 12px; }}
        </style>
    </head>
    <body>

    <div class="container">
        <div class="header-logo-container">
            <img src="1.png" alt="G-LAB PEPTIDES" class="header-logo">
        </div>
        <p class="subtitle">Estoque Atualizado e Pedidos Online</p>

        <div class="lote-alert-card">
            📢 Previsão de chegada de novos itens 13/02/2026, o estoque do site será atualizado!
        </div>

        <div id="main-info-alert" class="info-alert-card">
            <span class="close-alert" onclick="this.parentElement.style.display='none'">&times;</span>
            <strong>Aviso importante:</strong> Os produtos são envasados em forma sólida, assim não necessitam de refrigeração para manter as propriedades. O produto deve ser diluído em solução bacteriostática (vendida à parte). Após diluição manter refrigerado!. <br><strong>NOME DA SOLUÇÃO:</strong> Bacteriostic Water.
        </div>
        
        <div class="frete-card">
            <strong>🚚 1. Informe seu CEP para Localizar Região</strong>
            <div style="display: flex; gap: 8px;">
                <input type="tel" id="cep-destino" class="input-style" style="flex: 1;" placeholder="00000-000">
                <button id="btn-calc" onclick="calcularFrete()" class="btn-add" style="width: auto; padding: 0 15px;">Localizar</button>
            </div>
            <div id="resultado-frete" style="margin-top:12px; font-size: 0.95rem; line-height: 1.4; color: var(--primary); font-weight: bold;"></div>
        </div>

        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th style="width: 45%;">Produto</th>
                        <th>Status</th>
                        <th>Preço</th>
                        <th>Ação</th>
                    </tr>
                </thead>
                <tbody>
    """

    for idx, row in df.iterrows():
        produto = str(row.get('PRODUTO', 'N/A')).strip()
        espec = f"{row.get('VOLUME', '')} {row.get('MEDIDA', '')}".strip()
        preco = row.get('Preço (R$)', 0)
        estoque_status = str(row.get('ESTOQUE', row.get('STATUS', ''))).strip().upper()
        
        is_available = "DISPONÍVEL" in estoque_status
        status_class = "status-disponivel" if is_available else "status-espera"
        btn_disabled = "" if is_available else "disabled"
        simbolo = "+" if is_available else "✖"
        
        html_template += f"""
                    <tr>
                        <td>
                            <strong>{produto}</strong><br>
                            <small style="color:#666">{espec}</small><br>
                            <button class="btn-info" onclick="abrirInfo({idx})">+ informações</button>
                        </td>
                        <td><span class="{status_class}">{estoque_status}</span></td>
                        <td style="white-space: nowrap;">R$ {preco:,.2f}</td>
                        <td>
                            <button onclick="adicionar({idx})" {btn_disabled} class="btn-add">
                                {simbolo}
                            </button>
                        </td>
                    </tr>
        """

    html_template += f"""
                </tbody>
            </table>
        </div>
    </div>

    <div id="modalInfo" class="modal">
        <div class="modal-content">
            <h2 id="info-titulo" style="color: var(--primary); margin-top: 0; font-size: 1.2rem;"></h2>
            <img id="info-imagem" src="" alt="Produto" class="prod-img-modal">
            <div class="modal-info-body" id="info-texto"></div>
            <button onclick="fecharInfo()" class="btn-add" style="background:#6c757d">Fechar</button>
        </div>
    </div>

    <div id="cart-panel" class="cart-panel">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h3 style="margin:0">🛒 Seu Pedido (<span id="cart-count">0</span>)</h3>
            <button onclick="document.getElementById('cart-panel').style.display='none'" style="background:none; border:none; color:white; font-size:1.5rem;">▾</button>
        </div>
        
        <div id="cart-list" class="cart-list"></div>

        <div class="coupon-section">
            <input type="text" id="coupon-code" class="coupon-input" placeholder="Cupom de Desconto">
            <button onclick="aplicarCupom()" class="btn-coupon">Aplicar</button>
        </div>

        <div id="ship-info-container" class="ship-row" style="display:none;">
            <span id="ship-info-text"></span>
            <button onclick="removerFrete()" class="btn-remove" style="background:rgba(255,255,255,0.2); margin:0;">✖</button>
        </div>
        
        <div id="discount-row" class="discount-line">
            <span>Desconto (<span id="discount-name"></span>):</span>
            <span>- R$ <span id="discount-val">0.00</span></span>
        </div>

        <div class="total-row">
            <span>TOTAL GERAL:</span>
            <span>R$ <span id="total-val">0.00</span></span>
        </div>
        <button class="btn-checkout-final" onclick="abrirCheckout()">Ir para Pagamento</button>
    </div>

    <div id="modalCheckout" class="modal">
        <div class="modal-content" style="text-align: left;">
            <h2 style="color: var(--primary); margin-top: 0;">📦 Dados de Entrega</h2>
            <div class="form-group"><input type="text" id="f_nome" class="input-style" placeholder="Nome Completo"></div>
            <div class="form-group"><input type="text" id="f_end" class="input-style" placeholder="Endereço (Rua/Av)"></div>
            <div style="display:flex; gap:10px; margin-bottom:12px;">
                <input type="text" id="f_num" class="input-style" style="width:30%" placeholder="Nº">
                <input type="text" id="f_bairro" class="input-style" style="width:70%" placeholder="Bairro">
            </div>
            <div class="form-group"><input type="text" id="f_comp" class="input-style" placeholder="Complemento (Opcional)"></div>
            <div style="display:flex; gap:10px; margin-bottom:12px;">
                <input type="text" id="f_cidade" class="input-style" placeholder="Cidade">
                <input type="text" id="f_estado" class="input-style" style="width:30%" placeholder="UF">
            </div>
            <div class="form-group"><input type="tel" id="f_tel" class="input-style" placeholder="WhatsApp"></div>
            <div class="form-group">
                <label style="font-size:12px; font-weight:bold;">Forma de Pagamento:</label>
                <select id="f_pgto" class="input-style">
                    <option value="Pix">Pix (Aprovação Imediata)</option>
                    <option value="Cartão de crédito">Cartão de Crédito</option>
                </select>
            </div>
            <button onclick="enviarPedido()" class="btn-add" style="padding:15px; font-size:1.1rem; background:var(--primary);">ENVIAR PARA WHATSAPP</button>
            <button onclick="fecharCheckout()" style="background:none; border:none; width:100%; color:#666; margin-top:15px;">Cancelar / Voltar</button>
        </div>
    </div>

    <script>
        const PRODUTOS = {js_produtos};
        let carrinho = [];
        let freteV = 0;
        let freteD = "";
        let cupomAtivo = null;

        const REGIOES = {{
            'SUL': ['PR', 'SC', 'RS'],
            'SUDESTE': ['SP', 'RJ', 'MG', 'ES'],
            'CENTRO-OESTE': ['DF', 'GO', 'MT', 'MS'],
            'NORTE': ['AM', 'RR', 'AP', 'PA', 'TO', 'RO', 'AC'],
            'NORDESTE': ['BA', 'SE', 'AL', 'PE', 'PB', 'RN', 'CE', 'PI', 'MA']
        }};

        function abrirInfo(id) {{
            const p = PRODUTOS.find(x => x.id === id);
            if(p) {{
                document.getElementById('info-titulo').innerText = p.nome;
                document.getElementById('info-texto').innerText = p.info;
                
                const imgElement = document.getElementById('info-imagem');
                const nomeLimpo = p.nome.trim();
                const extensoes = ['.webp', '.png', '.jpg', '.jpeg'];

                function tentarExtensao(index) {{
                    if (index >= extensoes.length) {{
                        imgElement.style.display = 'none';
                        return;
                    }}
                    imgElement.src = "imagens produtos/" + nomeLimpo + extensoes[index];
                    imgElement.onload = function() {{ imgElement.style.display = 'block'; }};
                    imgElement.onerror = function() {{ tentarExtensao(index + 1); }};
                }}
                tentarExtensao(0);
                document.getElementById('modalInfo').style.display = 'block';
            }}
        }}

        function fecharInfo() {{ document.getElementById('modalInfo').style.display = 'none'; }}

        function adicionar(id) {{
            const p = PRODUTOS.find(x => x.id === id);
            if(p) {{
                carrinho.push({{...p, uid: Date.now() + Math.random()}});
                atualizarInterface();
            }}
        }}

        function remover(uid) {{
            carrinho = carrinho.filter(x => x.uid !== uid);
            if (carrinho.length === 0) removerFrete();
            atualizarInterface();
        }}

        function removerFrete() {{
            freteV = 0; freteD = "";
            document.getElementById('resultado-frete').innerText = "";
            document.getElementById('cep-destino').value = "";
            atualizarInterface();
        }}

        function aplicarCupom() {{
            const code = document.getElementById('coupon-code').value.trim().toUpperCase();
            const cupons = {{
                'BRUNA5': 0.05, 'DANI5': 0.05, 'GILMARA5': 0.05,
                'DAFNE10': 0.10, 'NOS5': 0.05, 'ROGERIO5': 0.05,
                'ANDERSON5': 0.05,
            }};
            if(cupons[code]) {{
                cupomAtivo = {{ nome: code, desc: cupons[code] }};
                alert("Cupom aplicado!");
            }} else {{
                cupomAtivo = null; alert("Cupom inválido.");
            }}
            atualizarInterface();
        }}

        function atualizarInterface() {{
            const list = document.getElementById('cart-list');
            const panel = document.getElementById('cart-panel');
            panel.style.display = carrinho.length > 0 ? 'block' : 'none';
            document.getElementById('cart-count').innerText = carrinho.length;
            list.innerHTML = '';
            let subtotal = 0;
            
            carrinho.forEach(item => {{
                subtotal += item.preco;
                list.innerHTML += `<div class="cart-item"><span>${{item.nome}}</span><span>R$ ${{item.preco.toFixed(2)}} <button class="btn-remove" onclick="remover(${{item.uid}})">×</button></span></div>`;
            }});

            let valorDesconto = cupomAtivo ? subtotal * cupomAtivo.desc : 0;
            document.getElementById('discount-row').style.display = cupomAtivo ? 'flex' : 'none';
            if(cupomAtivo) {{
                document.getElementById('discount-name').innerText = cupomAtivo.nome;
                document.getElementById('discount-val').innerText = valorDesconto.toFixed(2);
            }}

            const shipContainer = document.getElementById('ship-info-container');
            shipContainer.style.display = freteV > 0 ? 'flex' : 'none';
            if(freteV > 0) document.getElementById('ship-info-text').innerText = "🚚 " + freteD;

            const totalFinal = (subtotal - valorDesconto) + freteV;
            document.getElementById('total-val').innerText = totalFinal.toLocaleString('pt-BR', {{minimumFractionDigits: 2}});
        }}

        async function calcularFrete() {{
            const inputCep = document.getElementById('cep-destino').value.replace(/\D/g, '');
            const btn = document.getElementById('btn-calc');
            const res = document.getElementById('resultado-frete');

            if(inputCep.length !== 8) {{ alert("Por favor, digite um CEP válido com 8 dígitos."); return; }}

            btn.disabled = true;
            btn.innerText = "...";

            try {{
                const response = await fetch(`https://viacep.com.br/ws/${{inputCep}}/json/`);
                const data = await response.json();

                if(data.erro) {{
                    alert("CEP não encontrado. Verifique os números.");
                    btn.disabled = false;
                    btn.innerText = "Localizar";
                    return;
                }}

                const uf = data.uf.toUpperCase();
                
                if(REGIOES['SUL'].includes(uf)) {{
                    freteV = 90.00;
                    freteD = "SUL R$ 90,00 (3 a 6 dias úteis)";
                }} 
                else if(REGIOES['SUDESTE'].includes(uf) || REGIOES['CENTRO-OESTE'].includes(uf)) {{
                    freteV = 110.00;
                    freteD = "SUDESTE/CENTRO-OESTE R$ 110,00 (5 a 8 dias úteis)";
                }}
                else {{
                    freteV = 140.00;
                    freteD = "NORTE/NORDESTE R$ 140,00 (8 a 12 dias úteis)";
                }}

                document.getElementById('f_cidade').value = data.localidade;
                document.getElementById('f_estado').value = uf;
                document.getElementById('f_end').value = data.logradouro;
                document.getElementById('f_bairro').value = data.bairro;

                res.innerText = "✅ " + data.localidade + "-" + uf + ": " + freteD;
                atualizarInterface();

            }} catch (error) {{
                alert("Erro ao consultar CEP. Verifique sua conexão.");
            }} finally {{
                btn.disabled = false;
                btn.innerText = "Localizar";
            }}
        }}


        /* TRAVA DE FRETE OBRIGATÓRIO PARA O CHECKOUT */
        function abrirCheckout() {{ 
            if(freteV <= 0) {{
                alert("Por favor, informe seu CEP e calcule o frete antes de prosseguir!");
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
                return;
            }}
            document.getElementById('modalCheckout').style.display = 'block'; 
        }}

        function fecharCheckout() {{ document.getElementById('modalCheckout').style.display = 'none'; }}

        function enviarPedido() {{
            const dados = {{
                n: document.getElementById('f_nome').value.trim().toUpperCase(),
                e: document.getElementById('f_end').value.trim().toUpperCase(),
                nu: document.getElementById('f_num').value.trim().toUpperCase(),
                ba: document.getElementById('f_bairro').value.trim().toUpperCase(),
                co: document.getElementById('f_comp').value.trim().toUpperCase(),
                ci: document.getElementById('f_cidade').value.trim().toUpperCase(),
                es: document.getElementById('f_estado').value.trim().toUpperCase(),
                ce: document.getElementById('cep-destino').value.trim().toUpperCase(),
                t: document.getElementById('f_tel').value.trim().toUpperCase(),
                p: document.getElementById('f_pgto').value.toUpperCase()
            }};
            
            if(!dados.n || !dados.e || !dados.nu || !dados.ba || !dados.ci || !dados.es || !dados.t) {{
                alert("Por favor, preencha todos os campos obrigatórios!");
                return;
            }}

            const temSolucao = carrinho.some(item => item.nome.toUpperCase().includes("BACTERIOSTIC WATER"));
            if(!temSolucao) {{
                const confirmar = confirm("Você tem certeza que deseja realizar o pedido sem a solução para diluição do item?");
                if(!confirmar) {{
                    fecharCheckout();
                    document.getElementById('cart-panel').style.display = 'none';
                    alert("Por favor, adicione a Bacteriostic Water (3ml, 10ml ou 30ml) à sua lista de produtos.");
                    window.scrollTo({{ top: 0, behavior: 'smooth' }});
                    return; 
                }}
            }}
            
            let subtotalItens = 0;
            carrinho.forEach(i => subtotalItens += i.preco);
            let descTotal = cupomAtivo ? subtotalItens * cupomAtivo.desc : 0;
            let valorFinal = (subtotalItens - descTotal + freteV);
            
            let msg = "*NOVO PEDIDO G-LAB*%0A%0A";
            msg += "*DADOS DO CLIENTE:*%0A";
            msg += "• *NOME:* " + dados.n + "%0A";
            msg += "• *WHATSAPP:* " + dados.t + "%0A";
            msg += "• *END:* " + dados.e + ", " + dados.nu + "%0A";
            msg += "• *BAIRRO:* " + dados.ba + "%0A";
            if(dados.co) msg += "• *COMPL:* " + dados.co + "%0A";
            msg += "• *CIDADE:* " + dados.ci + "-" + dados.es + "%0A";
            msg += "• *CEP:* " + (dados.ce || "NÃO INFORMADO") + "%0A";
            msg += "• *PAGAMENTO:* " + dados.p + "%0A%0A";
            
            msg += "*ITENS DO PEDIDO:*%0A";
            carrinho.forEach(i => {{ 
                let linhaItem = "• " + i.nome.toUpperCase() + " (" + i.espec.toUpperCase() + ") - R$ " + i.preco.toFixed(2);
                if(cupomAtivo) {{
                    let descI = i.preco * cupomAtivo.desc;
                    linhaItem += " - COM DESCONTO (" + (cupomAtivo.desc * 100) + "%) R$ " + (i.preco - descI).toFixed(2);
                }}
                msg += linhaItem + "%0A"; 
            }});

            if(cupomAtivo) msg += "%0A🏷️ *CUPOM:* " + cupomAtivo.nome + " (-R$ " + descTotal.toFixed(2) + ")";
            msg += "%0A🚚 *FRETE:* " + freteD.toUpperCase();
            msg += "%0A%0A*TOTAL GERAL: R$ " + valorFinal.toFixed(2) + "*";
            
            // --- LOGICA CARTÃO DE CRÉDITO (BACKEND) ---
            if (dados.p === "CARTÃO DE CRÉDITO") {{
                // AJUSTE PARA A URL DO RENDER QUANDO ESTIVER ONLINE
                const URL_BACKEND = "https://ordemintegrado.onrender.com";
                
                // Feedback visual no botão do modal
                const btnEnvia = document.querySelector("#modalCheckout .btn-add");
                const textoOriginal = btnEnvia.innerText;
                btnEnvia.innerText = "⏳ GERANDO LINK...";
                btnEnvia.disabled = true;

                fetch(URL_BACKEND, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        total: valorFinal,
                        nome: dados.n
                    }})
                }})
                .then(response => response.json())
                .then(res => {{
                    if (res.url) {{
                        msg += "%0A%0A💳 *LINK DE PAGAMENTO:* " + res.url;
                        window.open("https://wa.me/+17746222523?text=" + msg, '_blank');
                    }} else {{
                        alert("Houve um problema ao gerar o link. Por favor, finalize via PIX no WhatsApp.");
                        window.open("https://wa.me/+17746222523?text=" + msg, '_blank');
                    }}
                }})
                .catch(err => {{
                    console.error("Erro no fetch:", err);
                    alert("O sistema de cartões está em manutenção. Finalizando via WhatsApp (PIX).");
                    window.open("https://wa.me/+17746222523?text=" + msg, '_blank');
                }})
                .finally(() => {{
                    btnEnvia.innerText = textoOriginal;
                    btnEnvia.disabled = false;
                }});
            }} else {{
                // ENVIO NORMAL PARA PIX/OUTROS
                window.open("https://wa.me/+17746222523?text=" + msg, '_blank');
            }}
        }}
    </script>
    </body>
    </html>
    """

    # Salva o arquivo final
    caminho_saida = os.path.join(diretorio_atual, 'index.html')
    try:
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"✅ Sucesso! Site gerado em: {caminho_saida}")
        print(f"🚀 Funcionalidade de Frete Obrigatório e Integração InfinitePay Aplicadas.")
    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo: {e}")

if __name__ == "__main__":

    gerar_site_vendas_completo()


