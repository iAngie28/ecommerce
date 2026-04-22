import { Link } from 'react-router-dom';
import { ShoppingCart, BrainCircuit, Box, CreditCard, BarChart3, Package, Layers3, Check } from 'lucide-react';
import styles from './HomeView.module.css';

const features = [
  { icon: ShoppingCart, color: '#e91e63', title: 'Carrito Inteligente',   text: 'Motor de recomendaciones personalizadas que sugiere productos relevantes al cliente.' },
  { icon: BrainCircuit, color: '#6366f1', title: 'Predicción de Ventas IA', text: 'Algoritmos ML analizan tu historial para proyectar demanda futura.' },
  { icon: CreditCard,   color: '#22c55e', title: 'Facturación SIN y QR',  text: 'Integración nativa para pagos QR y emisión automática de facturas.' },
  { icon: BarChart3,    color: '#f97316', title: 'Reportes',              text: 'Dashboard con métricas en tiempo real para analizar tu negocio.' },
  { icon: Package,      color: '#eab308', title: 'Control de Inventario', text: 'Stock en tiempo real, alertas automáticas y manejo de variantes.' },
  { icon: Layers3,      color: '#ef4444', title: 'Arquitectura Headless', text: 'Rápido y adaptable. Tu tienda perfecta en cualquier dispositivo.' },
];

export default function HomeView() {
  return (
    <div className={styles.page}>
      {/* NAVBAR */}
      <header className={styles.nav}>
        <div className={styles.brand}>
          <Box size={26} className={styles.brandIcon} />
          <span className={styles.brandName}>MiQhatu</span>
        </div>
        <nav className={styles.navLinks}>
          <a href="#features">Características</a>
          <a href="#pricing">Precios</a>
          <Link to="/login"        className={styles.btnLogin}>Iniciar Sesión</Link>
          <Link to="/crear-tienda" className={styles.btnRegister}>Crear tienda</Link>
        </nav>
      </header>

      {/* HERO */}
      <section className={styles.hero}>
        <div className={styles.heroBadge}>Nueva plataforma SaaS para emprendedores</div>
        <h1 className={styles.heroTitle}>
          La plataforma e-commerce que <span className={styles.highlight}>piensa por ti</span>, hecho simple.
        </h1>
        <p className={styles.heroSubtitle}>
          Crea tu tienda online en minutos. Carrito inteligente con recomendaciones y predicciones de ventas con IA.
        </p>
        <div className={styles.heroBtns}>
          <Link to="/crear-tienda" className={styles.btnPrimary}>Empezar Gratis</Link>
          <a href="#features"      className={styles.btnSecondary}>Ver características</a>
        </div>
      </section>

      {/* FEATURES */}
      <section id="features" className={styles.features}>
        <div className={styles.sectionHeader}>
          <h2>Todo lo que tu tienda necesita</h2>
          <p>Herramientas avanzadas de grado empresarial a un precio accesible.</p>
        </div>
        <div className={styles.featuresGrid}>
          {features.map((feat, i) => (
            <div key={i} className={styles.featureCard}>
              <div className={styles.featureIcon} style={{ background: `${feat.color}18`, color: feat.color }}>
                <feat.icon size={22} />
              </div>
              <h3>{feat.title}</h3>
              <p>{feat.text}</p>
            </div>
          ))}
        </div>
      </section>

      {/* PRICING */}
      <section id="pricing" className={styles.pricing}>
        <div className={styles.sectionHeader}>
          <h2>Planes para hacer crecer tu negocio</h2>
          <p>Sin costos ocultos. Cancela cuando quieras.</p>
        </div>
        <div className={styles.pricingGrid}>
          <div className={styles.priceCard}>
            <h3>Básico</h3>
            <p>Para emprendedores que están comenzando.</p>
            <div className={styles.price}>BS. — <span>/mes</span></div>
            <ul className={styles.featList}>
              <li><Check size={14} /> Hasta 50 productos</li>
              <li><Check size={14} /> Panel de administración</li>
              <li><Check size={14} /> Subdominio propio</li>
            </ul>
            <Link to="/crear-tienda" className={styles.btnCardSecondary}>Empezar</Link>
          </div>
          <div className={`${styles.priceCard} ${styles.featured}`}>
            <div className={styles.popularBadge}>Más Popular</div>
            <h3>Profesional</h3>
            <p>El ecosistema completo para negocios en crecimiento.</p>
            <div className={styles.price}>BS. — <span>/mes</span></div>
            <ul className={styles.featList}>
              <li><Check size={14} /> Productos ilimitados</li>
              <li><Check size={14} /> IA para predicciones</li>
              <li><Check size={14} /> Facturación SIN/QR</li>
              <li><Check size={14} /> Reportes avanzados</li>
            </ul>
            <Link to="/crear-tienda" className={styles.btnCardPrimary}>Empezar Gratis</Link>
          </div>
          <div className={styles.priceCard}>
            <h3>Enterprise</h3>
            <p>Para grandes volúmenes y múltiples tiendas.</p>
            <div className={styles.price}>Personalizado</div>
            <ul className={styles.featList}>
              <li><Check size={14} /> Multi-tienda</li>
              <li><Check size={14} /> SLA garantizado</li>
              <li><Check size={14} /> Onboarding dedicado</li>
            </ul>
            <a href="mailto:contacto@miqhatu.com" className={styles.btnCardSecondary}>Contáctanos</a>
          </div>
        </div>
      </section>

      <footer className={styles.footer}>
        <p>© 2025 MiQhatu — Todos los derechos reservados.</p>
      </footer>
    </div>
  );
}
