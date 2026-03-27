import React, { useState } from 'react';
import api from '../services/api';

function Login() {
    const [user, setUser] = useState('');
    const [pass, setPass] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const res = await api.post('/token/', { username: user, password: pass });
            localStorage.setItem('access_token', res.data.access);
            localStorage.setItem('refresh_token', res.data.refresh);
            alert("¡Sesión iniciada con éxito!");
            window.location.href = '/dashboard'; 
        } catch (error) {
            console.error('Error en el login:', error);
            alert("Credenciales incorrectas");
        }
    };

    return (
        <form onSubmit={handleLogin} style={{ padding: '20px' }}>
            <h2>Iniciar Sesión</h2>
            <input type="text" placeholder="Usuario" onChange={e => setUser(e.target.value)} /><br/>
            <input type="password" placeholder="Contraseña" onChange={e => setPass(e.target.value)} /><br/>
            <button type="submit">Entrar</button>
        </form>
    );
}

export default Login;