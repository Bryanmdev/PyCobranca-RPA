# 🤖 PyCobranca RPA - Automação Financeira Event-Driven

> *Sistema de Agente Autônomo para otimização de processos de cobrança corporativa via WhatsApp.*

## 🎯 O Problema
Muitos setores financeiros ainda realizam cobranças manuais, exigindo horas de trabalho repetitivo para enviar mensagens, consultar planilhas e registrar contatos. Isso gera gargalos operacionais e aumenta o risco de erro humano.

## 💡 A Solução
Desenvolvi um **Agente Autônomo (RPA)** em Python que opera em arquitetura orientada a eventos:
1.  **Monitoramento Remoto:** O sistema vigia uma pasta sincronizada (ex: Google Drive, OneDrive ou Rede).
2.  **Disparo Inteligente:** Ao detectar uma nova planilha, o robô ativa o navegador, processa os devedores e envia as mensagens via WhatsApp Web.
3.  **Auditoria:** Gera logs detalhados (Sucesso/Erro) para controle do gestor.

## 🛠️ Stack Tecnológica
-   **Python 3.x**
-   **Playwright** (Automação de Browser e manipulação de DOM)
-   **Watchdog** (Monitoramento de Sistema de Arquivos em tempo real)
-   **Pandas** (ETL e limpeza de dados)

## ⚙️ Arquitetura
-   **Sessão Persistente:** Utiliza um contexto de navegador persistente para manter o login do WhatsApp salvo localmente. Não é necessário ler QR Code a cada execução (apenas na primeira vez).
-   **Idempotência:** Travas lógicas evitam processamento duplicado do mesmo arquivo.
-   **Sanitização de Dados:** Tratamento automático de números de telefone e formatação de moeda.

## 🚀 Guia de Uso Passo a Passo
### 1. Instalação
Certifique-se de ter o Python instalado. Clone este repositório e instale as dependências:

```bash
pip install -r requirements.txt
playwright install chromium
```
### 2. Configuração
Abra o arquivo monitor_pasta.py e edite a variável PASTA_ALVO para indicar qual pasta o robô deve vigiar:
#### Exemplo no monitor_pasta.py:
PASTA_ALVO = r"C:\Users\SeuUsuario\Google Drive\Automacao\Entrada"

### 3. Primeira Execução (Setup do WhatsApp)
Como o sistema usa uma sessão persistente, você precisa logar apenas na primeira vez.

1. Execute o arquivo `iniciar_robo.bat` (ou rode `python monitor_pasta.py` no terminal).
2. O terminal mostrará: `👀 SERVIDOR DE MONITORAMENTO ATIVO`.
3. **Coloque uma planilha de teste** na pasta monitorada.
4. O robô detectará o arquivo e abrirá o navegador Chrome/Chromium.
5. **Escaneie o QR Code do WhatsApp** com o celular da empresa.
6. O robô enviará a mensagem da planilha e, ao fechar, salvará automaticamente sua sessão na pasta `whatsapp_session`.

> **Nota:** Nas próximas execuções, o navegador abrirá já logado e pronto para enviar.

### 4. Rotina de Uso
Com o robô rodando em background:

1. O gestor gera a planilha de cobrança.
2. Salva ou arrasta o arquivo para a pasta **Entrada**.
3. O robô detecta, processa os envios e move a planilha para a pasta **Processados**.
4. Um relatório de execução é gerado na pasta `relatorios`.

## 📁 Estrutura de Arquivos
O robô cria automaticamente a estrutura necessária na primeira execução:

```text
/ (Raiz do Projeto)
│── monitor_pasta.py    # Script de Vigilância (Watchdog)
│── robo_cobranca.py    # Script Executor (Playwright)
│── whatsapp_session/   # Pasta que guarda o Login (Gerada sozinha)
│── relatorios/         # Logs de auditoria (Gerado sozinho)
│── entrada/            # Onde você coloca as planilhas
    └── Processados/    # Para onde os arquivos vão após o envio
```
## ⚠️ Disclaimer
Este projeto foi desenvolvido para fins de automação de demandas e otimização de processos internos.
---
*Desenvolvido por Bryan M - Cientista da Computação & Marcus F - Engenheiro de Software*

