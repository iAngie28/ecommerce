import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { User, Mail, Phone, KeySquare, FileText, ArrowRight } from 'lucide-react';
import AuthLayout from 'shared/layouts/AuthLayout/AuthLayout';
import { Button, Input, Alert } from 'shared/components';
import { useAuth } from 'core/hooks/useAuth';
import api from 'core/services/api';
import styles from './AuthView.module.css';

const getErrorMessage = (error) => {
  const data = error.response?.data;
  if (!data) return 'Error en el registro. Por favor, intenta de nuevo.';

  const candidates = [
    data.correo,
    data.contrasena,
    data.password,
    data.redirect,
    data.non_field_errors,
    data.detail,
  ];

  for (const value of candidates) {
    if (Array.isArray(value) && value[0]) return value[0];
    if (typeof value === 'string' && value) return value;
  }

  return 'Error en el registro. Por favor, intenta de nuevo.';
};

export default function RegistroView() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const redirect = new URLSearchParams(location.search).get('redirect') || '';

  const [nombre, setNombre] = useState('');
  const [correo, setCorreo] = useState('');
  const [telefono, setTelefono] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [nit, setNit] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleRegistro = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const registroPayload = {
        nombre,
        correo,
        telefono: telefono || null,
        contrasena,
        nit: nit || null,
      };
      if (redirect) registroPayload.redirect = redirect;

      const registroRes = await api.post('/clientes/', registroPayload);

      if (registroRes.status === 201) {
        setSuccess('¡Registro exitoso! Iniciando sesión automáticamente...');

        if (registroRes.data.sso_url) {
          window.location.href = registroRes.data.sso_url;
          return;
        }

        const { access, refresh } = registroRes.data;
        if (access) {
          login(access, refresh, registroRes.data.cliente?.nombre || registroRes.data.nombre);
          navigate('/marketplace', { replace: true });
          return;
        }

        const loginRes = await api.post('/clientes/login/', {
          correo,
          contrasena,
          ...(redirect ? { redirect } : {}),
        });

        if (loginRes.data.sso_url) {
          window.location.href = loginRes.data.sso_url;
          return;
        }

        login(loginRes.data.access, loginRes.data.refresh, loginRes.data.cliente?.nombre);
        navigate('/marketplace', { replace: true });
      }
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const loginUrl = redirect
    ? `/login?redirect=${encodeURIComponent(redirect)}`
    : '/login';

  return (
    <AuthLayout
      headline={<>Bienvenido al Marketplace</>}
      subheadline="Crea tu cuenta para empezar a comprar en nuestras tiendas"
    >
      <div className={styles.formWrap}>
        <div className={styles.formHeader}>
          <h1 className={styles.formTitle}>Registro de Comprador</h1>
          <p className={styles.formSubtitle}>Crea tu cuenta para empezar a comprar</p>
          {redirect && (
            <p className={styles.formSubtitle}>Volverás a: {redirect}</p>
          )}
        </div>

        {error && <Alert variant="danger">{error}</Alert>}
        {success && <Alert variant="success">{success}</Alert>}

        <form onSubmit={handleRegistro} className={styles.form}>
          <Input
            id="registro-nombre"
            label="Nombre Completo"
            leftIcon={<User size={16} />}
            type="text"
            placeholder="Juan Pérez García"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
            autoFocus
          />

          <Input
            id="registro-correo"
            label="Correo Electrónico"
            leftIcon={<Mail size={16} />}
            type="email"
            placeholder="tu@correo.com"
            value={correo}
            onChange={(e) => setCorreo(e.target.value)}
            required
          />

          <Input
            id="registro-telefono"
            label="Teléfono"
            leftIcon={<Phone size={16} />}
            type="tel"
            placeholder="+591 71234567"
            value={telefono}
            onChange={(e) => setTelefono(e.target.value)}
          />

          <Input
            id="registro-nit"
            label="NIT"
            leftIcon={<FileText size={16} />}
            type="text"
            placeholder="1234567890"
            value={nit}
            onChange={(e) => setNit(e.target.value)}
          />

          <Input
            id="registro-contrasena"
            label="Contraseña"
            leftIcon={<KeySquare size={16} />}
            type="password"
            placeholder="••••••••••••"
            value={contrasena}
            onChange={(e) => setContrasena(e.target.value)}
            required
          />

          <Button
            type="submit"
            fullWidth
            loading={loading}
            rightIcon={<ArrowRight size={16} />}
            style={{ marginTop: '8px' }}
          >
            Crear Cuenta
          </Button>
        </form>

        <p className={styles.footer}>
          ¿Ya tienes cuenta?{' '}
          <Link to={loginUrl}>Inicia sesión aquí</Link>
        </p>
      </div>
    </AuthLayout>
  );
}
