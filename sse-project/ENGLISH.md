# SSE & Long-Lived Connections Project

This project demonstrates a production-grade implementation of Server-Sent Events (SSE) using a modern stack: FastAPI for the backend and React for the frontend.

## Core Concepts

### What are Long-lived Connections?

Traditionally, the web operates on a Request-Response model: the client requests data, the server responds, and the connection closes. Long-lived Connections break this paradigm by keeping a communication channel open between client and server. This allows data to flow continuously without the overhead of renegotiating a connection (handshake) for every new piece of information.

### Server-Sent Events (SSE) vs. WebSockets

* SSE: A standard HTTP-based protocol that allows servers to push data to clients unidirectionally. It is significantly simpler to implement and more resource-efficient for scenarios where the client does not need to send data back through the same channel.
* WebSockets: A full-duplex (bidirectional) protocol. While robust for chats or gaming, it requires more server overhead and complex network configurations regarding proxies and firewalls.

## Execution Guide

### Backend

1. Navigate to the backend folder.
2. Create a virtual environment: python -m venv .venv and activate it:
* Linux/macOS: source .venv/bin/activate
* Windows: .venv\Scripts\activate


3. Install dependencies: pip install -r requirements.txt.
4. Run the server: python main.py.

### Frontend

1. Navigate to the frontend folder.
2. Install dependencies: npm install.
3. Start the project: npm start.

![](./browser.png)

## Why use SSE in this project?

1. Automatic Reconnection: The browser natively attempts to reconnect if the server goes down.
2. Lightweight Protocol: It operates over standard HTTP (ports 80/443), making it firewall-friendly.
3. Efficiency: Ideal for dashboards, real-time notifications, and feeds where the server is the primary source of updates.

## Observing SSE & Long-lived Connections

To validate the nature of the long-lived connection in this project, observe the following behaviors in your browser's Developer Tools (F12):

### 1. Network Stream Inspection

In the Network tab, filter by Fetch/XHR or EventStream. Upon clicking the /stream endpoint, you will notice:

* Persistent Status: The request never finishes. The status remains Pending, and the duration time continues to climb indefinitely.
* Response Headers: The server confirms SSE usage via:
* Content-Type: text/event-stream — Directs the browser to treat the response as a continuous stream.
* Cache-Control: no-cache — Prevents intermediaries from buffering the data.
* Connection: keep-alive — Instructs the TCP socket to remain open.



### 2. Data Format (Frames)

Unlike a standard JSON response that arrives in a single block, SSE sends chunks. In the EventStream sub-tab of the network request, you will see each message arriving as an individual event. The raw data format on the wire looks like this:

```text
id: message_1
event: message
data: 14:30:05 - Atualização do sistema

```

### 3. Resilience Proof (Auto-Reconnection)

The definitive evidence of a robust Long-lived Connection is its self-healing capability:

1. Kill the Server: Stop the Python process (Ctrl+C). The React UI will show a connection error status.
2. Retry Mechanism: The browser’s EventSource object automatically enters a CONNECTING state, retrying the HTTP channel without any extra frontend code.
3. Recovery: Once the Python server is restarted, the browser completes a new handshake, and the data flow resumes instantly.

## Implementation Highlights

* Native Heartbeat: The server periodically sends silent pings (comments starting with :) to prevent infrastructure timeouts from closing the idle connection.
* Async Backpressure Handling: By using async/await in FastAPI, the server manages thousands of concurrent connections using an Event Loop, preventing thread exhaustion.

