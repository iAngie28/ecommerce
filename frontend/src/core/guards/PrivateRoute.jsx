import { Navigate } from 'react-router-dom';

/**
 * Guard de rutas protegidas.
 * Si no hay token → redirige a /login.
 * Si hay token → renderiza children (normalmente el AppShell con <Outlet />).
 */
const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('access_token');
  return token ? children : <Navigate to="/login" replace />;
};

export default PrivateRoute;
