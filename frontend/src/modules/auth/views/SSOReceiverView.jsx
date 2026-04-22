import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from 'core/hooks/useAuth';
import { getBaseDomain } from 'core/utils/domain';
import Spinner from 'shared/components/Spinner/Spinner';

export default function SSOReceiverView() {
  const navigate  = useNavigate();
  const location  = useLocation();
  const { login } = useAuth();

  useEffect(() => {
    const params   = new URLSearchParams(location.search);
    const token    = params.get('token');
    const refresh  = params.get('refresh');
    const fullName = params.get('full_name');

    if (token) {
      login(token, refresh || '', fullName ? decodeURIComponent(fullName) : '');
      navigate('/dashboard', { replace: true });
    } else {
      const baseDomain = getBaseDomain(window.location.hostname);
      const port = window.location.port ? `:${window.location.port}` : '';
      window.location.href = `${window.location.protocol}//${baseDomain}${port}/login`;
    }
  }, [navigate, location, login]);

  return (
    <div style={{ display: 'flex', height: '100vh', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '16px', background: 'var(--color-bg)' }}>
      <Spinner size="lg" />
      <p style={{ color: 'var(--color-text-muted)', fontSize: 'var(--text-sm)' }}>
        Sincronizando sesión...
      </p>
    </div>
  );
}
