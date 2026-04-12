import React, { useState } from 'react';
import './Login.css';
import { User, KeySquare, Box } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../services/api';


function Login() {
    const [user, setUser] = useState('');
    const [pass, setPass] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const res = await api.post('/token/', {
                username: user,
                password: pass
            });

            const { access, refresh, subdomain, full_name } = res.data;
            const tenantHost = subdomain; // FQDN completo que da el backend (ej: gerle.192.168.100.244.nip.io)

            // Construir la URL de redirección al subdominio del tenant
            if (tenantHost) {
                const protocol = window.location.protocol;
                const currentPort = window.location.port;

                // En modo IP directa (puerto 3000/8001), el navegador accede a la app
                // por IP:PUERTO. nip.io resuelve la IP pero el puerto lo decide el cliente.
                // El dev server de React escucha en 0.0.0.0 así que es accesible.
                const portPart = (currentPort && currentPort !== '80' && currentPort !== '443')
                    ? `:${currentPort}`
                    : '';

                window.location.href = `${protocol}//${tenantHost}${portPart}/sso?token=${access}&refresh=${refresh}&full_name=${encodeURIComponent(full_name || '')}`;
            } else {
                // Sin tenant (admin global), guardar y redirigir al dashboard
                localStorage.setItem('access_token', access);
                if (refresh) localStorage.setItem('refresh_token', refresh);
                localStorage.setItem('user_full_name', full_name || '');
                window.location.href = '/dashboard';
            }
        } catch (error) {
            console.error('Error en el login:', error);
            alert("Credenciales incorrectas o problema de conexión");
        }
    };

    return (
        <div className="login-wrapper">
            <div className="login-card">
                {/* PARTE IZQUIERDA: FORMULARIO */}
                <div className="login-form-side">
                    <h2>Inicia Sesión</h2>
                    <form onSubmit={handleLogin}>
                        <div className="input-group">
                            <label htmlFor="usuario-input" className="label-with-icon">
                                <User size={16} />
                                Usuario 
                            </label>
                            <input
                                id="usuario-input"
                                name="username"
                                type="text"
                                placeholder="Ingresar tu usuario"
                                value={user}
                                onChange={e => setUser(e.target.value)}
                                required 
                            />

                        </div>
                        <div className="input-group">
                            <div className="label-row">
                                <label htmlFor="pass-input" className="label-with-icon">
                                    <KeySquare size={16} />
                                    Contraseña
                                </label>
                                <Link to="/forgot-password" size={16} className="forgot-link">¿Olvidaste tu contraseña?</Link>
                            </div>
                            <input
                                id="pass-input"
                                name="password"
                                type="password"
                                placeholder="************"
                                value={pass}
                                onChange={e => setPass(e.target.value)}
                                required
                            />
                        </div>
                        <button type="submit" className="btn-submit">
                            Entrar
                        </button>
                    </form>
                    <p className="footer-text">
                        ¿No tienes cuenta? <Link to="/crear-tienda">Registrarte aquí</Link>
                    </p>
                </div>

                {/* PARTE DERECHA: BIENVENIDA (LADO OSCURO) */}
                <div className="login-info-side">
                    <div className="brand">
                        <Box size={32} color="#18aea4" /> {/* Icono de caja para el logo */}
                        <span className="brand-name">MiQhatu</span>
                    </div>
                    <div className="info-content">
                        <h1>Bienvenido de nuevo a tu panel de control.</h1>
                        <p>Revisa tus predicciones de ventas, gestiona tus pedidos y atiende a tus clientes desde un solo lugar.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Login;