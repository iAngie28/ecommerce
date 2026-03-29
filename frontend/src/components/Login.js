import React, { useState } from 'react';
import api from '../services/api';

function Login() {
    const [user, setUser] = useState('');
    const [pass, setPass] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            // Petición al endpoint global
            const res = await api.post('/token/', { 
                username: user, 
                password: pass 
            });
            
            const { access, refresh, subdomain } = res.data;

            // Guardamos localmente por si el admin se queda en el dominio global
            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);
            
            if (subdomain) {
                // REDIRECCIÓN DINÁMICA (SSO): Enviamos el token a la aduana (/sso) del subdominio
                window.location.href = `http://${subdomain}:3000/sso?token=${access}`;
            } else {
                window.location.href = '/dashboard'; 
            }
        } catch (error) {
            console.error('Error en el login:', error);
            alert("Credenciales incorrectas o problema de conexión");
        }
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '50px' }}>
            <form onSubmit={handleLogin} style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px', width: '300px' }}>
                <h2 style={{ textAlign: 'center' }}>Login SaaS</h2>
                <div style={{ marginBottom: '15px' }}>
                    <label>Usuario:</label>
                    <input 
                        type="text" 
                        value={user}
                        onChange={e => setUser(e.target.value)} 
                        style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                        required
                    />
                </div>
                <div style={{ marginBottom: '15px' }}>
                    <label>Contraseña:</label>
                    <input 
                        type="password" 
                        value={pass}
                        onChange={e => setPass(e.target.value)} 
                        style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                        required
                    />
                </div>
                <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Entrar al Sistema
                </button>
            </form>
        </div>
    );
}

export default Login;