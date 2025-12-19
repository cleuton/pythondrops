import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App'; // Importação sem extensão .js

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);