import { Link } from 'react-router-dom';
import { ShoppingCart, BrainCircuit, Box, CreditCard, BarChart3, Package, Layers3, Check } from 'lucide-react';
import './Home.css'; // 

const features = [
    { icon: ShoppingCart, color: '#e91e63', title: 'Carrito Inteligente', text: 'Motor de recomendaciones personalizadas que sugiere productos relevantes al cliente, aumentando tu ticket promedio de venta.' },
    { icon: BrainCircuit, color: '#0d26df', title: 'Predeccion de Ventas IA', text: 'Algoritmos de Machine Learning analizan tu historial para proyectar la demanda futura, optimizando así tu control de inventario.' },
    { icon: CreditCard, color: '#4ade80', title: 'Facturación SIN y QR', text: 'Integración nativa para pagos con código QR, pasarelas locales y emisión automática de facturas electrónicas válidas' },
    { icon: BarChart3, color: '#fb923c', title: 'Reportes', text: 'Dashboard interactivo con métricas en tiempo real. Analiza el comportamiento de tus clientes y la rotación de tus productos.' },
    { icon: Package, color: '#facc15', title: 'Gestión de Inventario', text: 'Control de stock en tiempo real, alertas de productos agotados y manejo eficiente de categorías y variantes de catálogo.' },
    { icon: Layers3, color: '#f87171', title: 'Arquitectura Headless', text: 'Diseñado para ser rápido y adaptable. Tu tienda se verá perfecta en cualquier dispositivo móvil o computadora' },
];

function Home() {
    return (
        <div className="home-container">
            {/* 1. NAVBAR */}
            <header className="home-header">
                <div className="brand">
                    <Box size={28} color="#18aea4" />
                    <span className="brand-name">MiQhatu</span>
                </div>
                
                <nav>
                    <div className="nav-right">
                        <a href="#features">Características</a>
                        <a href="#pricing">Precios</a>
                        <Link to="/login" className="btn-login-nav">Iniciar Sesión</Link>
                        <Link to="/register" className="btn-register-nav">Registrarse</Link>
                    </div>
                </nav>

            </header>

            {/* 2. HERO */}
            <section className="hero-section">
                <div className="hero-content">
                    <h1>La plataforma e-commerce que piensa por ti, <span className="highlight">hecho simple</span>.</h1>
                    <p>Crea tu tienda online en minutos. Usa nuestro Carrito Inteligente con recomendaciones personalizadas y predice tus ventas futuras mediante Inteligencia Artificial</p>

                    <div className="hero-btns">
                        <button className="btn-primary">Empezar Gratis</button>
                        <button className="btn-secondary">Ver Demostración</button>
                    </div>
                </div>
            </section>

            {/* 3. FEATURES  */}
            <section id="features" className="features-section">
                <h2>  Todo lo que tu tienda necesita en un solo lugar </h2>
                <p>Olvídate de sistemas complejos. Te ofrecemos herramientas avanzadas de grado
                    empresarial a un precio accesible.</p>
                <div className="features-grid">
                    {features.map((feat, index) => (
                        <div key={index} className="feature-card">
                            <div className="icon-box" style={{ backgroundColor: `${feat.color}20` }}>
                                <feat.icon size={24} color={feat.color} />
                            </div>
                            <h3>{feat.title}</h3>
                            <p>{feat.text}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* 4. precio  */}
            <section id="pricing" className="pricing-section">
                <div className="pricing-header">
                    <h2>Planes diseñados para hacer crecer tu negocio</h2>
                    <p>Selecciona el plan que mejor se adapte a tu volumen de ventas.</p>
                </div>

                <div className="pricing-grid">
                    <div className="price-card gray"></div>

                    {/* PLAN PROFESIONAL (El destacado) */}
                    <div className="price-card professional">
                        <div className="badge">Más Popular</div>
                        <h3>Profesional</h3>
                        <p>El ecosistema completo para negocios en crecimiento.</p>
                        <div className="price">BS. [Precio] <span>/mes</span></div>
                        <ul className="feat-list">
                            <li><Check size={14} color="#18aea4" /> característica</li>
                            <li><Check size={14} color="#18aea4" /> característica</li>
                            <li><Check size={14} color="#18aea4" /> característica</li>
                        </ul>
                    </div>

                    <div className="price-card gray"></div> {/* Placeholder gris de tu Penpot */}
                </div>
            </section>
        </div>
    );
}

export default Home;