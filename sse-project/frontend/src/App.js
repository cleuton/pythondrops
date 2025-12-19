import React, { useState, useEffect } from 'react';

function App() {
  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState('Conectando...');

  useEffect(() => {
    let sse;

    const connect = () => {
      sse = new EventSource('http://localhost:8000/stream');

      sse.onopen = () => {
        setStatus('Conectado ao Servidor (SSE)');
      };

      sse.onmessage = (event) => {
        setMessages((prev) => [event.data, ...prev]);
      };

      sse.onerror = (err) => {
        // IMPORTANTE: Não chamamos sse.close() aqui para erros temporários.
        // O navegador tentará reconectar sozinho a cada poucos segundos.
        setStatus('Conexão perdida. Tentando reconectar automaticamente...');
      };
    };

    connect();

    // Cleanup: Só fechamos quando o usuário sair da página/componente
    return () => {
      if (sse) sse.close();
    };
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>SSE Real-Time Monitor</h1>
      <p>Status: <strong>{status}</strong></p>
      <div style={{ border: '1px solid #ccc', height: '200px', overflowY: 'auto', padding: '10px' }}>
        {messages.map((m, i) => <div key={i}>{m}</div>)}
      </div>
    </div>
  );
}

export default App; // Esta linha é crucial para o index.js encontrá-lo