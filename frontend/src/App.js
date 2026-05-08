import { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// ── Core ─────────────────────────────────────────────────────
import { APP_MODULES, AUTH_ROUTES } from 'core/router/routes.config';
import { TenantProvider } from 'core/contexts/TenantContext';
import { AuthProvider   } from 'core/contexts/AuthContext';
import PrivateRoute from 'core/guards/PrivateRoute';

// ── Layout ───────────────────────────────────────────────────
import AppShell from 'shared/layouts/AppShell/AppShell';

// ── Loading Fallback ─────────────────────────────────────────
const LoadingFallback = () => (
  <main>
    <p>Cargando...</p>
  </main>
);

// ════════════════════════════════════════════════════════════
// App — solo enrutamiento. Para añadir nuevas secciones
// ve a core/router/routes.config.jsx y añade una entrada.
// ════════════════════════════════════════════════════════════
function App() {
  return (
    <TenantProvider>
      <AuthProvider>
        <Router>
          <Suspense fallback={<LoadingFallback />}>
            <Routes>
              {/* ── Rutas públicas ── */}
              {AUTH_ROUTES.map(({ id, path, component: Component }) => (
                <Route key={id} path={path} element={<Component />} />
              ))}

              {/* ── Rutas protegidas con AppShell ── */}
              <Route
                element={
                  <PrivateRoute>
                    <AppShell />
                  </PrivateRoute>
                }
              >
                {APP_MODULES.filter((m) => m.protected).map(({ id, path, component: Component }) => (
                  <Route key={id} path={path} element={<Component />} />
                ))}
              </Route>

              {/* ── Fallback ── */}
              <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
          </Suspense>
        </Router>
      </AuthProvider>
    </TenantProvider>
  );
}

export default App;
