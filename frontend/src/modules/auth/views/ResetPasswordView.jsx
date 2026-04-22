import { useState } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { Lock, ArrowRight } from 'lucide-react';
import AuthLayout from 'shared/layouts/AuthLayout/AuthLayout';
import { Button, Input, Alert } from 'shared/components';
import api from 'core/services/api';
import styles from './AuthView.module.css';

export default function ResetPasswordView() {
  const { uid, token } = useParams();
  const navigate        = useNavigate();
  const [password,  setPassword]  = useState('');
  const [password2, setPassword2] = useState('');
  const [loading,   setLoading]   = useState(false);
  const [error,     setError]     = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== password2) { setError('Las contraseñas no coinciden.'); return; }
    setLoading(true);
    setError('');
    try {
      await api.post('/password-reset/confirm/', { uid, token, new_password: password });
      navigate('/login', { replace: true });
    } catch {
      setError('El enlace es inválido o ya expiró. Solicita uno nuevo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout
      headline={<>Crea una <span>nueva contraseña</span> segura.</>}
      subheadline="Elige una contraseña fuerte de al menos 8 caracteres."
    >
      <div className={styles.formWrap}>
        <div className={styles.formHeader}>
          <h1 className={styles.formTitle}>Nueva Contraseña</h1>
          <p className={styles.formSubtitle}>Ingresa y confirma tu nueva contraseña.</p>
        </div>

        {error && <Alert variant="danger">{error}</Alert>}

        <form onSubmit={handleSubmit} className={styles.form}>
          <Input
            id="reset-password"
            label="Nueva contraseña"
            leftIcon={<Lock size={16} />}
            type="password"
            placeholder="Mínimo 8 caracteres"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
          />
          <Input
            id="reset-password2"
            label="Confirmar contraseña"
            leftIcon={<Lock size={16} />}
            type="password"
            placeholder="Repite la contraseña"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            required
            error={password2 && password !== password2 ? 'Las contraseñas no coinciden' : ''}
          />
          <Button type="submit" fullWidth loading={loading} rightIcon={<ArrowRight size={16} />} style={{ marginTop: '8px' }}>
            Cambiar contraseña
          </Button>
        </form>

        <p className={styles.footer}>
          <Link to="/login">Volver al login</Link>
        </p>
      </div>
    </AuthLayout>
  );
}
