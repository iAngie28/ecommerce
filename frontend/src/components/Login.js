import React, { useState } from 'react';
import './Login.css';
import { User, KeySquare, Box } from 'lucide-react';
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

            const { access, refresh, schema_name, subdomain } = res.data;

            // Extraemos el subdominio del API (ej: empresa1.localhost) o intentamos adivinarlo
            let tenantHost = subdomain || (schema_name ? `${schema_name.replace('_', '')}.localhost` : null);

            // Si el usuario está accediendo a través de la IP directa del VPS (ej: 157.173.102.129)
            // los dominios '.localhost' fallarán porque el cliente no los resuelve.
            // Para pruebas en VPS sin dominio real, usamos nip.io automáticamente.
            if (tenantHost && typeof window !== 'undefined') {
                const currentIP = window.location.hostname;
                // Si la URL actual es una IP (ej: 123.45.67.89) y el tenantHost es .localhost
                if (/^[0-9.]+$/.test(currentIP) && currentIP !== '127.0.0.1' && tenantHost.endsWith('.localhost')) {
                    // Convertimos empresa1.localhost -> empresa1.157.173.102.129.nip.io
                    const slug = tenantHost.replace('.localhost', '');
                    tenantHost = `${slug}.${currentIP}.nip.io`;
                }
            }

            // Construir la URL de SSO usando el tenantHost y manteniendo el puerto actual
            if (tenantHost) {
                // Removemos puertos si venían en tenantHost
                const cleanHost = tenantHost.split(':')[0];
                const portPart = window.location.port ? `:${window.location.port}` : '';
                const protocol = window.location.protocol;
                
                // Redirigir al subdominio con ambos tokens para SSO
                window.location.href = `${protocol}//${cleanHost}${portPart}/sso?token=${access}&refresh=${refresh}`;
            } else {
                // Sin tenant (admin global), guardar y redirigir al dashboard
                localStorage.setItem('access_token', access);
                if (refresh) localStorage.setItem('refresh_token', refresh);
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
                                <a href="#" className="forgot-link">¿Olvidaste tu contraseña?</a>
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
                        ¿No tienes cuenta? <a href="#">Registrarte aquí</a>
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