import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

// Componente para proteger rutas
const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem('access_token');
    return token ? children : <Navigate to="/login" />;
};

function App() {
    // Función para manejar el cierre de sesión y limpiar el token
    const handleLogout = () => {
        localStorage.clear();
        window.location.href = '/login';
    };

    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                
                <Route path="/dashboard" element={
                    <PrivateRoute>
                        {/* Aquí es donde llamamos a tu nuevo Dashboard profesional */}
                        <Dashboard onLogout={handleLogout} />
                    </PrivateRoute>
                } />

                {/* Si no reconoce la ruta, lo manda al login */}
                <Route path="*" element={<Navigate to="/login" />} />
            </Routes>
        </Router>
    );
}

export default App;