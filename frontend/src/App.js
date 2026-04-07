import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';

import Home from './components/Home';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

// 1. LA ADUANA: Recibe el token que viene desde localhost y lo guarda en cliente1.localhost
const SSOReceiver = () => {
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const token = params.get('token');
        const refresh = params.get('refresh');

        if (token) {
            // Se guarda en el localStorage EXCLUSIVO de este subdominio
            localStorage.setItem('access_token', token);
            if (refresh) localStorage.setItem('refresh_token', refresh);
            // Salto al dashboard limpiando la URL
            navigate('/dashboard', { replace: true });
        } else {
            // Sin token → login en el dominio base LIMPIO
            const currentHost = window.location.hostname;
            let baseDomain;
            if (currentHost.endsWith('.nip.io')) {
                const parts = currentHost.split('.');
                const ipParts = parts.slice(0, -2).filter(p => /^\d+$/.test(p));
                baseDomain = ipParts.join('.');
            } else if (currentHost.endsWith('.localhost')) {
                baseDomain = 'localhost';
            } else {
                const parts = currentHost.split('.');
                baseDomain = parts.length > 1 ? parts.slice(1).join('.') : currentHost;
            }
            const port = window.location.port ? `:${window.location.port}` : '';
            window.location.href = `${window.location.protocol}//${baseDomain || 'localhost'}${port}/login`;
        }
    }, [navigate, location]);

    return (
        <div className="flex h-screen items-center justify-center bg-slate-50">
            <div className="animate-pulse font-bold text-blue-600 tracking-widest uppercase">
                Sincronizando Tienda...
            </div>
        </div>
    );
};

// 2. Guardia de seguridad normal (Ya no tiene que leer URLs, solo el disco duro)
const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem('access_token');
    return token ? children : <Navigate to="/login" />;
};

function App() {
    const handleLogout = () => {
        localStorage.clear();
        // Redirige al dominio base LIMPIO (sin subdominio tenant ni nip.io)
        const currentHost = window.location.hostname;
        let baseDomain;
        if (currentHost.endsWith('.nip.io')) {
            const parts = currentHost.split('.');
            const ipParts = parts.slice(0, -2).filter(p => /^\d+$/.test(p));
            baseDomain = ipParts.join('.');
        } else if (currentHost.endsWith('.localhost')) {
            baseDomain = 'localhost';
        } else {
            const parts = currentHost.split('.');
            baseDomain = parts.length > 1 ? parts.slice(1).join('.') : currentHost;
        }
        const port = window.location.port ? `:${window.location.port}` : '';
        window.location.href = `${window.location.protocol}//${baseDomain}${port}/login`;
    };

    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                {/* Ruta de Login Global */}
                <Route path="/login" element={<Login />} />
                
                {/* NUEVA RUTA: El puente de sincronización */}
                <Route path="/sso" element={<SSOReceiver />} />
                
                {/* Ruta del Dashboard (Totalmente aislada y segura) */}
                <Route path="/dashboard" element={
                    <PrivateRoute>
                        <Dashboard onLogout={handleLogout} />
                    </PrivateRoute>
                } />

                <Route path="*" element={<Navigate to="/login" />} />
            </Routes>
        </Router>
    );
}

export default App;