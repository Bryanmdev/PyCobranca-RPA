# 🤖 PyCobranca RPA - Automação Financeira Event-Driven

> *Sistema de Agente Autônomo para otimização de processos de cobrança corporativa via WhatsApp.*

## 🎯 O Problema
Muitos setores financeiros ainda realizam cobranças manuais, exigindo horas de trabalho repetitivo para enviar mensagens, consultar planilhas e registrar contatos. Isso gera gargalos operacionais e aumenta o risco de erro humano.

## 💡 A Solução
Desenvolvi um **Agente Autônomo (RPA)** em Python que opera em arquitetura orientada a eventos:
1.  **Monitoramento Remoto:** O sistema vigia uma pasta sincronizada (ex: Google Drive/OneDrive).
2.  **Disparo Inteligente:** Ao detectar uma nova planilha, o robô ativa o navegador, processa os devedores e envia as mensagens via WhatsApp Web.
3.  **Auditoria:** Gera logs detalhados (Sucesso/Erro) para controle do gestor.

## 🛠️ Stack Tecnológica
-   **Python 3.x** (Lógica core)
-   **Playwright** (Automação de Browser e manipulação de DOM)
-   **Watchdog** (Monitoramento de Sistema de Arquivos em tempo real)
-   **Pandas** (ETL e limpeza de dados)

## ⚙️ Arquitetura e Decisões Técnicas
-   **Persistent Context:** Utilização do contexto persistente do Playwright para manter a sessão do WhatsApp salva, eliminando a necessidade de ler QR Code a cada execução.
-   **Idempotência:** O script de monitoramento possui travas lógicas para evitar que o mesmo arquivo seja processado duas vezes (concorrência de eventos de I/O).
-   **Sanitização de Dados:** Tratamento automático de números de telefone para o padrão internacional (DDI) e formatação de moeda.

## 🚀 Como Rodar
1. Clone o repositório.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Configure o caminho da pasta monitorada no `monitor_pasta.py`.
4. Execute o script de monitoramento.

---
*Desenvolvido por Bryan [Seu Sobrenome] - Estudante de Ciência da Computação*