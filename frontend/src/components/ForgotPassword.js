import React, { useState } from 'react';
import { Mail, ArrowLeft, Box } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import './Login.css'; // Reutilizamos estilos base
import './ForgotPassword.css'; // Estilos específicos si los hay

function ForgotPassword() {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [devUrl, setDevUrl] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');
        setError('');
        setDevUrl('');

        try {
            const res = await api.post('/password-reset/', { email });
            setMessage(res.data?.message || 'Si el email existe, recibirás un enlace.');
            // Modo desarrollo: el backend devuelve el link directo si no hay email configurado
            if (res.data?.dev_reset_url) {
                setDevUrl(res.data.dev_reset_url);
            }
        } catch (err) {
            const msg = err.response?.data?.error || 'Error al procesar la solicitud. Intenta nuevamente.';
            setError(msg);
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
                    {devUrl && (
                        <div className="alert-message" style={{background:'#fff3cd', color:'#856404', borderLeft:'4px solid #ffc107', marginTop:'10px', fontSize:'0.85rem'}}>
                            <strong>Modo Desarrollo</strong> — Email no configurado.<br/>
                            <a href={devUrl} style={{wordBreak:'break-all', color:'#0d6efd'}}>{devUrl}</a>
                        </div>
                    )}
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
