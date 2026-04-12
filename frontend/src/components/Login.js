import React, { useState } from 'react';
import './Login.css';
import { User, KeySquare, Box } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { getBaseDomain } from '../utils/domain';

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

            const { access, refresh, schema_name, subdomain, full_name } = res.data;

            // En producción, confiamos 100% en el subdominio que el Backend nos entrega.
            // Si la DB tiene nip.io, el backend enviará el dominio completo correcto.
            let tenantHost = subdomain;

            // Construir la URL de redirección
            if (tenantHost) {
                const protocol = window.location.protocol;
                // No forzamos el puerto en producción (80)
                const portPart = (window.location.port && window.location.port !== '80') ? `:${window.location.port}` : '';
                
                // Redirigir al subdominio con ambos tokens para SSO
                window.location.href = `${protocol}//${tenantHost}${portPart}/sso?token=${access}&refresh=${refresh}&full_name=${encodeURIComponent(full_name || '')}`;
            } else {
                // Sin tenant (admin global), guardar y redirigir al dashboard
                localStorage.setItem('access_token', access);
                if (refresh) localStorage.setItem('refresh_token', refresh);
                if (full_name) localStorage.setItem('user_full_name', full_name);
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
                                //type="email" 
                                id="usuario-input"
                                type="text"
                                placeholder="Ingresar tu usuario"
                                value={user}
                                onChange={e => setUser(e.target.value)}
                                required //obligatorio
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