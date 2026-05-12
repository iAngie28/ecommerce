import { Navigate, useLocation } from 'react-router-dom';
import { useAuthContext } from 'core/contexts/AuthContext';

/**
 * Guard de rutas protegidas con validación de roles.
 * @param {Array} allowedRoles - Roles permitidos para esta ruta.
 */
const PrivateRoute = ({ children, allowedRoles = [] }) => {
  const { user, isAuthenticated } = useAuthContext();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Si se especifican roles y el usuario no tiene ninguno de ellos
  if (allowedRoles.length > 0 && !allowedRoles.includes(user?.role)) {
    // Redirigir según el rol que sí tenga para evitar bucles
    const fallback = user?.role === 'admin' ? '/su' : (user?.role === 'cliente' ? '/mi-portal' : '/dashboard');
    return <Navigate to={fallback} replace />;
  }

  return children;
};

export default PrivateRoute;
