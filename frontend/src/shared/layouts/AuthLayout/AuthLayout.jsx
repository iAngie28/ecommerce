import { Box } from 'lucide-react';
import styles from './AuthLayout.module.css';

/**
 * AuthLayout — Lego layout para páginas de autenticación.
 * Renderiza una pantalla dividida: panel oscuro con brand (izquierda)
 * + formulario centrado (derecha).
 *
 * Props:
 *   features: Array<{ icon: ReactNode, title, description }>
 *             — íconos y textos del panel de marca (opcional)
 *   children: ReactNode — el formulario (va en el panel derecho)
 *
 * Uso:
 *   <AuthLayout features={[{ icon: <Zap/>, title: "Rápido", description: "..." }]}>
 *     <LoginForm />
 *   </AuthLayout>
 */
const AuthLayout = ({ children, features = [], headline, subheadline }) => {
  return (
    <div className={styles.wrapper}>
      {/* ── Brand Panel (izquierda) ── */}
      <div className={styles.brandPanel}>
        <div className={styles.brandTop}>
          <Box size={26} className={styles.brandIcon} />
          <span className={styles.brandName}>MiQhatu</span>
        </div>

        <div className={styles.brandContent}>
          <h2>
            {headline || <>La plataforma que <span>hace crecer</span> tu negocio.</>}
          </h2>
          {subheadline && <p>{subheadline}</p>}
        </div>

        {features.length > 0 && (
          <div className={styles.brandFeatures}>
            {features.map((feat, i) => (
              <div key={i} className={styles.brandFeature}>
                <div className={styles.featureIcon}>{feat.icon}</div>
                <div className={styles.featureText}>
                  <h4>{feat.title}</h4>
                  <p>{feat.description}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ── Form Panel (derecha) ── */}
      <div className={styles.formPanel}>
        <div className={styles.formCard}>{children}</div>
      </div>
    </div>
  );
};

export default AuthLayout;
