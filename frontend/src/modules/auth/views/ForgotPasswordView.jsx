import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, ArrowLeft } from 'lucide-react';
import AuthLayout from 'shared/layouts/AuthLayout/AuthLayout';
import { Button, Input, Alert } from 'shared/components';
import api from 'core/services/api';
import styles from './AuthView.module.css';

export default function ForgotPasswordView() {
  const [email,   setEmail]   = useState('');
  const [loading, setLoading] = useState(false);
  const [sent,    setSent]    = useState(false);
  const [error,   setError]   = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await api.post('/password-reset/', { email });
      setSent(true);
    } catch {
      setError('No encontramos una cuenta con ese correo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout
      headline={<>Recupera el acceso a tu <span>cuenta.</span></>}
      subheadline="Te enviaremos un enlace seguro para restablecer tu contraseña."
    >
      <div className={styles.formWrap}>
        <div className={styles.formHeader}>
          <h1 className={styles.formTitle}>Recuperar Contraseña</h1>
          <p className={styles.formSubtitle}>
            Ingresa el correo de tu cuenta MiQhatu.
          </p>
        </div>

        {error && <Alert variant="danger">{error}</Alert>}
        {sent  && (
          <Alert variant="success" title="¡Correo enviado!">
            Revisa tu bandeja de entrada. El enlace es válido por 24 horas.
          </Alert>
        )}

        {!sent && (
          <form onSubmit={handleSubmit} className={styles.form}>
            <Input
              id="forgot-email"
              label="Correo electrónico"
              leftIcon={<Mail size={16} />}
              type="email"
              placeholder="tu@correo.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoFocus
            />
            <Button type="submit" fullWidth loading={loading} style={{ marginTop: '8px' }}>
              Enviar enlace
            </Button>
          </form>
        )}

        <p className={styles.footer}>
          <Link to="/login">
            <ArrowLeft size={14} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'middle' }} />
            Volver al login
          </Link>
        </p>
      </div>
    </AuthLayout>
  );
}
