import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
// Importamos el proveedor que detecta el subdominio
import { TenantProvider } from './contexts/TenantContext'; 

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    {/* Envolvemos App con TenantProvider según la arquitectura del PDF */}
    <TenantProvider>
      <App />
    </TenantProvider>
  </React.StrictMode>
);

reportWebVitals();