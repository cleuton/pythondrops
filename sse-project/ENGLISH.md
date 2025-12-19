# SSE & Long-Lived Connections Project

This project demonstrates a production-grade implementation of Server-Sent Events (SSE) using a modern stack: FastAPI for the backend and React for the frontend.

## Core Concepts

### What are Long-lived Connections?

Traditionally, the web operates on a Request-Response model: the client requests data, the server responds, and the connection closes. Long-lived Connections break this paradigm by keeping a communication channel open between client and server. This allows data to flow continuously without the overhead of renegotiating a connection (handshake) for every new piece of information.

#### 1. Server Initiation: HTTP Protocol Optimization

The server initiates the long-lived connection by simply altering the semantics of the standard HTTP response, without changing the protocol.

* **Content-Type:** The server sends `Content-Type: text/event-stream`. This notifies the browser that the response is not a static document, but a continuous data stream.
* **Persistent Connection (Keep-Alive):** The server utilizes the native HTTP/1.1 mechanism (or HTTP/2 frames) to keep the TCP socket open. It does not send the message body termination character that would normally signal the end of the request.
* **Immediate Flush:** The server must ensure that the output buffer is flushed immediately after each `yield`; otherwise, data would remain stuck in the server buffer until reaching a specific size, destroying the "real-time" experience.

#### 2. The Client's Role: Maintenance and Resilience

For the client, the secret to "long-duration" lies in the implementation of the `EventSource` interface within the browser engine:

* **Incremental Reading:** The browser does not wait for the end of the request to process data. It reads the TCP socket in chunks. Whenever it encounters the byte sequence `\n\n` (two line feeds), it triggers the event in JavaScript.
* **Connection State Management:** The browser monitors the state of the TCP socket. If the socket is closed (receiving a `FIN` or `RST` packet), the `EventSource` API does not terminate the object; it changes its internal state to `CONNECTING`.
* **Automatic Reconnection and Continuity:** The client schedules a new silent HTTP request. To ensure continuity, the browser sends the `Last-Event-ID` header containing the ID of the last successfully processed event. This allows the server to "catch up" on data lost during the downtime.

**HTTP/2** resolves the biggest bottleneck for SSE in HTTP/1.1: the limit of connections per domain (usually 6).

#### How HTTP/2 Improves SSE

* **Multiplexing:** In HTTP/1.1, each SSE stream occupied an entire TCP socket. If you had 6 tabs open with SSE, the browser could not load anything else from your site. In HTTP/2, multiple SSE streams travel within a **single TCP connection** using different binary "frames."
* **Resource Efficiency:** It drastically reduces the overhead of opening connections (TCP/TLS handshakes) and memory consumption on both the server and client.
* **Prioritization:** The protocol allows the browser to prioritize critical resources (like CSS/JS) while the SSE stream continues running in the background.

In HTTP/1.1, SSE is a **"Hanging GET"** that blocks a connection slot. In HTTP/2, SSE is just another **Stream ID** within an already established binary tunnel, eliminating concurrency limits and the cost of new sockets.

#### And how to run with HTTP/2?

To run FastAPI with **HTTP/2**, Uvicorn requires the use of **SSL/TLS**, as modern browsers do not support multiplexing on unencrypted connections.

##### 1. Requirements

You will need the `httptools` library and certificates (even if self-signed).

```bash
pip install uvicorn[standard]

```

##### 2. Python Configuration

In your `main.py` file (or via CLI), you must point to the certificate files:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8443,
        ssl_keyfile="./key.pem",
        ssl_certfile="./cert.pem",
        http="h2"  # Forces HTTP/2 support
    )

```

##### 3. Impact

* **Binary Framing:** HTTP/2 fragments SSE messages into small binary frames. This prevents one stream from "clogging" the connection, allowing other data (images, scripts) to pass through simultaneously.
* **Header Compression (HPACK):** Repetitive SSE headers are compressed, saving bandwidth on long-lived connections that undergo frequent reconnections.

#### Summary

With HTTP/2 + SSL, the limit of 6 SSE connections per domain disappears. The user can open dozens of tabs of your dashboard without stalling the loading of the rest of the site, all over a single TCP tunnel.

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

