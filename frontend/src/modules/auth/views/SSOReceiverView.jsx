import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from 'core/hooks/useAuth';
import { getBaseDomain } from 'core/utils/domain';
import { syncLocalCart } from 'modules/marketplace/services/carritoService';

const decodeJwtPayload = (token) => {
  try {
    const payload = token.split('.')[1];
    const normalized = payload.replace(/-/g, '+').replace(/_/g, '/');
    const padded = normalized.padEnd(normalized.length + ((4 - normalized.length % 4) % 4), '=');
    return JSON.parse(atob(padded));
  } catch {
    return {};
  }
};

export default function SSOReceiverView() {
  const navigate  = useNavigate();
  const location  = useLocation();
  const { login } = useAuth();
  const [message, setMessage] = useState('Sincronizando sesión...');
  const [error, setError] = useState('');

  useEffect(() => {
    const receiveSession = async () => {
      const params = new URLSearchParams(location.search);
      const token = params.get('token');
      const refresh = params.get('refresh');
      const fullName = params.get('full_name');

      if (token) {
        login(token, refresh || '', fullName ? decodeURIComponent(fullName) : '');
        window.history.replaceState(null, '', '/sso');
        const payload = decodeJwtPayload(token);

        if (payload.role === 'CLIENTE') {
          try {
            const result = await syncLocalCart();
            setMessage(`Sesión recibida. Items sincronizados: ${result.synced}.`);
            navigate('/catalogo', { replace: true });
          } catch (err) {
            console.error('Error sincronizando carrito en SSO:', err);
            setError(err.response?.data?.error || 'Sesión recibida, pero falló la sincronización del carrito.');
          }
          return;
        }

        navigate('/dashboard', { replace: true });
      } else {
        const baseDomain = getBaseDomain(window.location.hostname);
        const port = window.location.port ? `:${window.location.port}` : '';
        const redirect = encodeURIComponent(window.location.hostname);
        window.location.href = `${window.location.protocol}//${baseDomain}${port}/login?redirect=${redirect}`;
      }
    };

    receiveSession();
  }, [navigate, location, login]);

  return (
    <main>
      <h1>SSO de prueba</h1>
      <p>{message}</p>
      {error && <p>{error}</p>}
      {error && <p><a href="/catalogo">Volver al catálogo</a></p>}
    </main>
  );
}
