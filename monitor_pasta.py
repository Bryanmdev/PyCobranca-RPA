import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from robo_cobranca import executar_disparos

# [CONFIG] Caminho da pasta monitorada
# Exemplo: G:\Meu Drive\Automacao_Financeira\Entrada
PASTA_ALVO = r"C:\Caminho\Para\Sua\Pasta\Entrada" 
PASTA_PROCESSADOS = os.path.join(PASTA_ALVO, "Processados")

class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        self.processar(event)

    def on_modified(self, event):
        # Filtro: Ignora arquivos temporários (~$)
        if not event.is_directory and not os.path.basename(event.src_path).startswith("~$"):
            self.processar(event)

    def processar(self, event):
        caminho_arquivo = event.src_path
        arquivo_nome = os.path.basename(caminho_arquivo)

        # [CRITICAL] Prevenção de "Double Fire"
        if not os.path.exists(caminho_arquivo): return
        if "Processados" in caminho_arquivo: return 
        if not (arquivo_nome.endswith('.csv') or arquivo_nome.endswith('.xlsx')): return 

        print(f"\n🔔 [EVENTO] Arquivo detectado: {arquivo_nome}")
        
        # [SYNC DELAY] Aguarda finalização do I/O (Upload da Nuvem)
        print("⏳ Aguardando consistência do arquivo...")
        time.sleep(15) 

        if not os.path.exists(caminho_arquivo): return

        print("🚀 Iniciando pipeline...")
        try:
            executar_disparos(caminho_arquivo)
            
            if not os.path.exists(PASTA_PROCESSADOS):
                os.makedirs(PASTA_PROCESSADOS)
            
            nome_final = f"Processado_{int(time.time())}_{arquivo_nome}"
            destino = os.path.join(PASTA_PROCESSADOS, nome_final)
            
            shutil.move(caminho_arquivo, destino)
            print(f"✅ Arquivo movido para: {destino}")
            
        except Exception as e:
            if "No such file" in str(e): return
            print(f"❌ Erro Crítico: {e}")

if __name__ == "__main__":
    # Criação de pastas para teste local
    if not os.path.exists(PASTA_ALVO): 
        try:
            os.makedirs(PASTA_ALVO)
        except:
            pass # Pode falhar se for caminho de rede invalido

    if not os.path.exists(PASTA_PROCESSADOS): 
        try:
            os.makedirs(PASTA_PROCESSADOS)
        except:
            pass

    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=PASTA_ALVO, recursive=False)
    
    observer.start()
    print(f"👀 SERVIDOR DE MONITORAMENTO ATIVO\n[Target]: {PASTA_ALVO}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()