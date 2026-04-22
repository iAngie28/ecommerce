import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { User, KeySquare, ArrowRight } from 'lucide-react';
import AuthLayout from 'shared/layouts/AuthLayout/AuthLayout';
import { Button, Input, Alert } from 'shared/components';
import { useAuth } from 'core/hooks/useAuth';
import api from 'core/services/api';
import styles from './AuthView.module.css';

export default function LoginView() {
  const { login } = useAuth();
  const navigate   = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await api.post('/token/', { username, password });
      const { access, refresh, subdomain, full_name } = res.data;

      if (subdomain) {
        const protocol    = window.location.protocol;
        const currentPort = window.location.port;
        const portPart    = (currentPort && currentPort !== '80' && currentPort !== '443')
          ? `:${currentPort}` : '';
        window.location.href = `${protocol}//${subdomain}${portPart}/sso?token=${access}&refresh=${refresh}&full_name=${encodeURIComponent(full_name || '')}`;
      } else {
        login(access, refresh, full_name);
        navigate('/dashboard', { replace: true });
      }
    } catch {
      setError('Credenciales incorrectas o problema de conexión.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout
      headline={<>Bienvenido de nuevo a tu <span>panel de control.</span></>}
      subheadline="Revisa predicciones, gestiona pedidos y atiende clientes desde un solo lugar."
    >
      <div className={styles.formWrap}>
        <div className={styles.formHeader}>
          <h1 className={styles.formTitle}>Iniciar Sesión</h1>
          <p className={styles.formSubtitle}>Accede a tu tienda MiQhatu</p>
        </div>

        {error && <Alert variant="danger">{error}</Alert>}

        <form onSubmit={handleLogin} className={styles.form}>
          <Input
            id="login-username"
            label="Usuario"
            leftIcon={<User size={16} />}
            type="text"
            placeholder="Tu nombre de usuario"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            autoFocus
          />
          <Input
            id="login-password"
            label="Contraseña"
            leftIcon={<KeySquare size={16} />}
            type="password"
            placeholder="••••••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            labelRight={
              <Link to="/forgot-password" className={styles.forgotLink}>
                ¿Olvidaste tu contraseña?
              </Link>
            }
          />
          <Button
            type="submit"
            fullWidth
            loading={loading}
            rightIcon={<ArrowRight size={16} />}
            style={{ marginTop: '8px' }}
          >
            Entrar
          </Button>
        </form>

        <p className={styles.footer}>
          ¿No tienes cuenta?{' '}
          <Link to="/crear-tienda">Créala gratis aquí</Link>
        </p>
      </div>
    </AuthLayout>
  );
}
