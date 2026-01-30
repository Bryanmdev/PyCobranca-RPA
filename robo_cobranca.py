import pandas as pd
from playwright.sync_api import sync_playwright
import time
import urllib.parse
import os
from datetime import datetime

# --- CONFIGURAÇÕES GERAIS ---
PASTA_PERFIL = "./whatsapp_session"
PASTA_RELATORIOS = "./relatorios"
NOME_EMPRESA = "Empresa Demo LTDA" # <--- Alterar para o nome real em produção

def formatar_telefone(tel_bruto):
    """
    Sanitização de dados: Remove caracteres não numéricos e garante
    o formato internacional (DDI 55) exigido pela URL do WhatsApp.
    """
    apenas_numeros = "".join(filter(str.isdigit, str(tel_bruto)))
    if not apenas_numeros or len(apenas_numeros) < 10:
        return None
    if not apenas_numeros.startswith("55"):
        return "55" + apenas_numeros
    return apenas_numeros

def gerar_relatorio_txt(dados):
    """
    Gera logs de auditoria para o gestor.
    Essencial para rastreabilidade de quem recebeu ou não a cobrança.
    """
    if not os.path.exists(PASTA_RELATORIOS):
        os.makedirs(PASTA_RELATORIOS)
    
    agora = datetime.now()
    nome_arquivo = f"Log_Cobranca_{agora.strftime('%Y-%m-%d_%H-%M')}.txt"
    caminho_completo = os.path.join(PASTA_RELATORIOS, nome_arquivo)
    
    total = len(dados)
    sucessos = sum(1 for d in dados if d['Status'] == 'Sucesso')
    erros = sum(1 for d in dados if d['Status'] == 'Erro')
    
    try:
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write(f"LOG DE EXECUÇÃO - RPA {NOME_EMPRESA.upper()}\n")
            f.write(f"Timestamp: {agora.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            f.write(f"STATS: Total: {total} | Sucessos: {sucessos} | Falhas: {erros}\n")
            f.write("-" * 30 + "\n\n")
            
            for item in dados:
                f.write(f"[{item['Hora']}] {item['Cliente']} ({item['Telefone Formatado']})\n")
                f.write(f"    Valor: R$ {item['Valor']} | Status: {item['Status']}\n")
                if item['Status'] != 'Sucesso':
                    f.write(f"    Erro: {item['Observacao']}\n")
                f.write("-" * 40 + "\n")
            
        print(f"📄 Log gerado: {caminho_arquivo}")
    except Exception as e:
        print(f"❌ Falha ao gravar log: {e}")

def executar_disparos(caminho_arquivo):
    print(f"📂 Processando dataset: {caminho_arquivo}")
    resultados_log = []
    
    try:
        if caminho_arquivo.endswith('.csv'):
            df = pd.read_csv(caminho_arquivo, sep=',', encoding='utf-8') 
        else:
            df = pd.read_excel(caminho_arquivo)
    except Exception as e:
        print(f"❌ Erro de Leitura: {e}")
        return

    with sync_playwright() as p:
        # [CORE] Browser Context
        # Persistent Context mantém cookies/sessão, evitando QR Code repetitivo.
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=PASTA_PERFIL,
                headless=False, 
                args=["--start-maximized"],
                no_viewport=True
            )
        except Exception as e:
            print(f"❌ Erro ao instanciar browser: {e}")
            return

        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://web.whatsapp.com")

        try:
            page.wait_for_selector('div[aria-label="Lista de conversas"]', timeout=60000)
            print("✅ Sessão autenticada.")
        except:
            print("⚠️ Sessão não encontrada. Necessário login manual.")

        for index, row in df.iterrows():
            nome = row.get('Nome do Cliente', 'Cliente')
            telefone = formatar_telefone(row.get('Telefone', ''))
            valor = row.get('Sld Devedor', '0,00')
            titulo = row.get('Título', '')
            vencimento = row.get('Vencimento', '')

            log_entry = {
                "Cliente": nome,
                "Telefone Formatado": telefone,
                "Valor": valor,
                "Status": "Pendente",
                "Hora": datetime.now().strftime("%H:%M:%S"),
                "Observacao": ""
            }

            if not telefone:
                log_entry["Status"] = "Ignorado"
                log_entry["Observacao"] = "Sem telefone válido"
                resultados_log.append(log_entry)
                continue

            try:
                data_obj = datetime.strptime(str(vencimento), '%Y-%m-%d')
                data_fmt = data_obj.strftime('%d/%m/%Y')
            except:
                data_fmt = str(vencimento)

            # --- MENSAGEM GENÉRICA (Template) ---
            mensagem = (
                f"Olá, *{nome}*! Setor financeiro da {NOME_EMPRESA}.\n\n"
                f"Consta em aberto o título *{titulo}* vencido em *{data_fmt}*, valor *R$ {valor}*.\n"
                f"Evite restrições regularizando em até 7 dias.\n\n"
                f"Pagamento exclusivo via boleto bancário.\n"
                f"Dúvidas? Estamos à disposição."
            )
            
            msg_encoded = urllib.parse.quote(mensagem)
            print(f"📨 [{index+1}/{len(df)}] Enviando para {nome}...")

            try:
                page.goto(f"https://web.whatsapp.com/send?phone={telefone}&text={msg_encoded}")
                time.sleep(8) 

                botao = page.get_by_label("Enviar", exact=True)
                botao.wait_for(state="visible", timeout=15000)
                botao.click()
                
                log_entry["Status"] = "Sucesso"
                print("   ✅ Enviado.")
                time.sleep(5) 
                
            except Exception as e:
                print(f"   ❌ Erro de envio: {e}")
                log_entry["Status"] = "Erro"
                log_entry["Observacao"] = str(e)
            
            resultados_log.append(log_entry)

        print("🏁 Fim do lote. Gerando relatórios...")
        time.sleep(2)
        context.close()
        
        gerar_relatorio_txt(resultados_log)