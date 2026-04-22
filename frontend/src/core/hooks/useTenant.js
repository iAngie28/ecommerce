import { useContext } from 'react';
import { TenantContext } from 'core/contexts/TenantContext';

/**
 * Hook para obtener el tenant activo (subdominio).
 * Uso: const tenant = useTenant();
 */
export const useTenant = () => {
  const ctx = useContext(TenantContext);
  if (ctx === null) throw new Error('useTenant debe usarse dentro de <TenantProvider>');
  return ctx;
};
