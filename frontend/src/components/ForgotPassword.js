import React, { useState } from 'react';
import { Mail, ArrowLeft, Box } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import './Login.css'; // Reutilizamos estilos base
import './ForgotPassword.css'; // Estilos específicos si los hay

function ForgotPassword() {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');
        setError('');
        
        try {
            await api.post('/password-reset/', { email });
            setMessage('Si el email existe en nuestro sistema, recibirás un enlace para restablecer tu contraseña.');
        } catch (err) {
            setError('Error al procesar la solicitud. Intenta nuevamente.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-wrapper">
            <div className="login-card">
                <div className="login-form-side">
                    <Link to="/login" className="back-link">
                        <ArrowLeft size={16} /> Volver al login
                    </Link>
                    
                    <h2>Recuperar Contraseña</h2>
                    <p className="subtitle">Ingresa tu correo electrónico y te enviaremos las instrucciones.</p>
                    
                    <form onSubmit={handleSubmit}>
                        <div className="input-group">
                            <label htmlFor="email-input" className="label-with-icon">
                                <Mail size={16} /> Correo Electrónico
                            </label>
                            <input
                                id="email-input"
                                name="email"
                                type="email"
                                placeholder="tu@email.com"
                                value={email}
                                onChange={e => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        
                        <button type="submit" className="btn-submit" disabled={loading}>
                            {loading ? 'Enviando...' : 'Enviar Enlace'}
                        </button>
                    </form>

                    {message && <div className="alert-message success">{message}</div>}
                    {error && <div className="alert-message error">{error}</div>}
                </div>

                <div className="login-info-side">
                    <div className="brand">
                        <Box size={32} color="#18aea4" />
                        <span className="brand-name">MiQhatu</span>
                    </div>
                    <div className="info-content">
                        <h1>No te preocupes, a todos nos pasa.</h1>
                        <p>Sigue los pasos que te enviaremos al correo para recuperar el acceso a tu cuenta de forma segura.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ForgotPassword;
