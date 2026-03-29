import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

// 1. LA ADUANA: Recibe el token que viene desde localhost y lo guarda en cliente1.localhost
const SSOReceiver = () => {
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const token = params.get('token');

        if (token) {
            // Se guarda en el localStorage EXCLUSIVO de este subdominio
            localStorage.setItem('access_token', token);
            // Salto al dashboard limpiando la URL (replace: true borra el historial)
            navigate('/dashboard', { replace: true });
        } else {
            // Si alguien intenta entrar a /sso sin token, lo botamos al login
            window.location.href = 'http://localhost:3000/login';
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
        window.location.href = 'http://localhost:3000/login';
    };

    return (
        <Router>
            <Routes>
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