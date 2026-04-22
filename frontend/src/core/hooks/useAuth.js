import { useContext } from 'react';
import { AuthContext } from 'core/contexts/AuthContext';

/**
 * Hook para acceder al estado global de autenticación.
 * Uso: const { user, login, logout, isAuthenticated } = useAuth();
 */
export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth debe usarse dentro de <AuthProvider>');
  return ctx;
};
