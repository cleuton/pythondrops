# SSE & Long-Lived Connections Project

Este projeto demonstra a implementação de **Server-Sent Events (SSE)** utilizando um ecossistema moderno: **FastAPI** para o backend e **React** para o frontend.

## Conceitos Fundamentais

### O que são Long-lived Connections?

Tradicionalmente, a web funciona no modelo *Request-Response*: o cliente pede algo, o servidor responde e a conexão fecha.
As **Long-lived Connections** (Conexões de Longa Duração) quebram esse paradigma. Elas mantêm um canal aberto entre cliente e servidor, permitindo que os dados fluam continuamente sem a necessidade de renegociar a conexão (handshake) a cada nova informação.

### Server-Sent Events (SSE) vs WebSockets

* **SSE:** É um padrão HTTP que permite ao servidor "empurrar" dados para o cliente de forma unidirecional. É muito mais simples de implementar e consome menos recursos se você não precisa que o cliente envie dados de volta pelo mesmo canal.
* **WebSockets:** É um protocolo bidirecional (Full-Duplex). É mais robusto para chats ou jogos, mas exige mais do servidor e de configurações de rede (proxies/firewalls).

## Como Executar

### Backend

1. Navegue até a pasta `backend`.
2. Crie um ambiente virtual: `python -m venv .venv` e ative: `source .venv/bin/activate`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Execute o servidor: `python main.py`.

### Frontend

1. Navegue até a pasta `frontend`.
2. Instale as dependências: `npm install`.
3. Inicie o projeto: `npm start`.

![](./browser.png)

## Por que usar SSE neste projeto?

1. **Reconexão Automática:** O navegador tenta reconectar sozinho se o servidor cair.
2. **Protocolo Leve:** Funciona sobre o protocolo HTTP padrão (porta 80/443).
3. **Eficiência:** Perfeito para dashboards, notificações e feeds onde o servidor é a fonte da verdade.


## Constatação de SSE e Long-lived Connections

Para validar a natureza da conexão de longa duração deste projeto, você pode observar os seguintes comportamentos técnicos no seu navegador (Chrome/Edge/Firefox):

### 1. Inspeção do Fluxo de Rede (Network)

Ao abrir o **Developer Tools (F12)** e navegar até a aba **Network**, filtre por `Fetch/XHR` ou `EventStream`. Ao clicar no endpoint `/stream`, você notará:

* **Status Permanente:** A requisição não termina. O status permanecerá como "Pending" ou o tempo de carregamento continuará subindo indefinidamente.
* **Headers de Resposta:** O servidor confirma o uso de SSE através dos cabeçalhos:
* `Content-Type: text/event-stream` — Indica que o corpo da resposta é um fluxo contínuo de dados.
* `Cache-Control: no-cache` — Impede que intermediários (proxies) armazenem os dados.
* `Connection: keep-alive` — Mantém o socket TCP aberto.

### 2. O Formato dos Dados (Frames)

Diferente de uma resposta JSON comum que vem em um bloco único `{...}`, o SSE envia "chunks" (pedaços). Na aba **EventStream** (dentro da requisição no Network), você verá cada mensagem chegando como um evento individual. O formato bruto que viaja pela rede é:

```text
id: message_1
event: message
data: 14:30:05 - Atualização do sistema

```

### 3. Prova de Resiliência (Reconexão Automática)

A maior evidência da robustez de uma **Long-lived Connection** gerenciada pelo protocolo SSE é a sua capacidade de auto-recuperação:

1. **Derrube o Servidor:** Pare o processo Python (`Ctrl+C`). No console do React, você verá o erro de conexão.
2. **Mecanismo de Retentativa:** O objeto `EventSource` no navegador entrará automaticamente em estado de `CONNECTING`. Ele tentará restabelecer o canal HTTP sem nenhuma linha de código adicional no frontend.
3. **Recuperação:** Assim que o servidor Python for reiniciado, o navegador completará o novo "Handshake" e o fluxo de dados será retomado instantaneamente, provando que o cliente está programado para manter a conexão viva o tempo todo.

## Diferenciais da Implementação

* **Heartbeat Nativo:** O servidor envia pings silenciosos (comentários `:`) para evitar que timeouts de infraestrutura (como Nginx ou Cloudflare) encerrem a conexão por inatividade.
* **Backpressure Handling:** O uso de `async/await` no FastAPI garante que, se o cliente estiver lento para processar, o servidor não trave, liberando recursos para outros usuários.

