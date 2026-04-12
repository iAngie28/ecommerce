import React, { useState } from 'react';
import { Lock, Box, CheckCircle } from 'lucide-react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import './Login.css';
import './ForgotPassword.css';

function ResetPassword() {
    const { uid, token } = useParams();
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [completed, setCompleted] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (password !== confirmPassword) {
            setError('Las contraseñas no coinciden.');
            return;
        }

        setLoading(true);
        setMessage('');
        setError('');
        
        try {
            await api.post('/password-reset-confirm/', {
                uid,
                token,
                new_password: password
            });
            setCompleted(true);
            setMessage('Tu contraseña ha sido actualizada con éxito.');
        } catch (err) {
            setError('El enlace es inválido o ha expirado. Por favor, solicita uno nuevo.');
        } finally {
            setLoading(false);
        }
    };

    if (completed) {
        return (
            <div className="login-wrapper">
                <div className="login-card">
                    <div className="login-form-side">
                        <div className="text-center">
                            <CheckCircle size={60} color="#18aea4" style={{ marginBottom: '20px' }} />
                            <h2>¡Todo listo!</h2>
                            <p className="subtitle">Tu contraseña ha sido restablecida correctamente. Ya puedes iniciar sesión con tu nueva clave.</p>
                            <Link to="/login" className="btn-submit" style={{ display: 'block', textDecoration: 'none', textAlign: 'center' }}>
                                Ir al Login
                            </Link>
                        </div>
                    </div>
                    <div className="login-info-side">
                        <div className="brand">
                            <Box size={32} color="#18aea4" />
                            <span className="brand-name">MiQhatu</span>
                        </div>
                        <div className="info-content">
                            <h1>Seguridad restablecida.</h1>
                            <p>Tu cuenta está protegida. Recuerda no compartir tu contraseña con nadie.</p>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="login-wrapper">
            <div className="login-card">
                <div className="login-form-side">
                    <h2>Nueva Contraseña</h2>
                    <p className="subtitle">Ingresa tu nueva contraseña para recuperar el acceso.</p>
                    
                    <form onSubmit={handleSubmit}>
                        <div className="input-group">
                            <label htmlFor="pass-input" className="label-with-icon">
                                <Lock size={16} /> Nueva Contraseña
                            </label>
                            <input
                                id="pass-input"
                                type="password"
                                placeholder="************"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                required
                            />
                        </div>

                        <div className="input-group">
                            <label htmlFor="confirm-pass-input" className="label-with-icon">
                                <Lock size={16} /> Confirmar Contraseña
                            </label>
                            <input
                                id="confirm-pass-input"
                                type="password"
                                placeholder="************"
                                value={confirmPassword}
                                onChange={e => setConfirmPassword(e.target.value)}
                                required
                            />
                        </div>
                        
                        <button type="submit" className="btn-submit" disabled={loading}>
                            {loading ? 'Actualizando...' : 'Restablecer Contraseña'}
                        </button>
                    </form>

                    {error && <div className="alert-message error">{error}</div>}
                    {!error && message && <div className="alert-message success">{message}</div>}
                </div>

                <div className="login-info-side">
                    <div className="brand">
                        <Box size={32} color="#18aea4" />
                        <span className="brand-name">MiQhatu</span>
                    </div>
                    <div className="info-content">
                        <h1>Elige una clave fuerte.</h1>
                        <p>Te recomendamos usar una combinación de letras, números y símbolos para mayor seguridad.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ResetPassword;
