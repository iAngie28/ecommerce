import { useState, useEffect } from "react";
import { 
  Store, User, Mail, Lock, Globe, Building, CheckCircle2, 
  ArrowRight, Sparkles, ShieldCheck, Zap 
} from "lucide-react";
import "./CrearTienda.css";

export default function CrearTienda() {
  const [form, setForm] = useState({
    nombre_tienda: "",
    schema_name: "",
    dominio: "",
    first_name: "",
    last_name: "",
    email: "",
    password: ""
  });
  
  const [status, setStatus] = useState("idle"); // idle, loading, success, error
  const [responseData, setResponseData] = useState(null);
  const [error, setError] = useState(null);

  // Auto-gestión de slug y dominio
  useEffect(() => {
    if (form.nombre_tienda) {
      const slug = form.nombre_tienda.toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "") // Quitar acentos
        .replace(/\s+/g, '_')
        .replace(/[^a-z0-9_]/g, '');
      
      // Detectar base host
      const currentHost = window.location.hostname;
      let baseHost = "localhost";
      
      if (currentHost.endsWith(".nip.io")) {
          // Si estamos usando nip.io, mantenemos el patrón
          const parts = currentHost.split('.');
          const ipParts = parts.slice(0, -2).filter(p => /^\d+$/.test(p));
          if (ipParts.length === 4) {
              baseHost = `${ipParts.join('.')}.nip.io`;
          }
      }

      setForm(prev => ({
        ...prev,
        schema_name: slug,
        dominio: `${slug}.${baseHost}`
      }));
    }
  }, [form.nombre_tienda]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("loading");
    setError(null);
    
    try {
      // Usamos el puerto 8001 para el API central como está configurado
      const apiBase = window.location.hostname === "localhost" 
        ? "http://localhost:8001" 
        : `${window.location.protocol}//${window.location.hostname}:8001`;

      const res = await fetch(`${apiBase}/api/tiendas/crear/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      
      const data = await res.json();
      if (!res.ok) throw data;
      
      setResponseData(data);
      setStatus("success");
    } catch (err) {
      console.error("Error creating store:", err);
      setError(err);
      setStatus("error");
    }
  };

  if (status === "success") {
    // Redirigir siempre al login normal (dominio base) como pidió el usuario
    const loginUrl = "/login";

    return (
      <div className="crear-tienda-wrapper">
        <div className="crear-tienda-card" style={{ justifyContent: 'center', alignItems: 'center' }}>
          <div className="success-view">
            <div className="success-icon">
              <CheckCircle2 size={48} />
            </div>
            <h2>¡Tu tienda está lista!</h2>
            <p className="subtitle">Hemos configurado todo para que empieces a vender hoy mismo.</p>
            
            <div className="store-url-box">
              <p>Tu dominio exclusivo es:</p>
              <strong>{responseData.dominio}</strong>
            </div>

            <p style={{ marginBottom: 30, color: '#636e72' }}>
              Ya puedes iniciar sesión con tu correo <b>{responseData.admin_email}</b>
            </p>

            <a href={loginUrl} className="btn-goto-store">
              Ir a mi Tienda <ArrowRight size={20} style={{ marginLeft: 8 }} />
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="crear-tienda-wrapper">
      <div className="crear-tienda-card">
        {/* LADO IZQUIERDO: FORMULARIO */}
        <div className="form-side">
          <h2>Crea tu Negocio</h2>
          <p className="subtitle">Únete a cientos de emprendedores que ya usan MiQhatu.</p>

          <form onSubmit={handleSubmit}>
            <div className="section-title">
              <Store size={18} /> Datos de la Tienda
            </div>
            
            <div className="input-grid">
              <div className="input-group full-width">
                <label><Building size={16} /> Nombre de la Tienda</label>
                <input
                  name="nombre_tienda"
                  value={form.nombre_tienda}
                  onChange={handleChange}
                  placeholder="Ej: Mi Boutique Online"
                  required
                />
              </div>

              <div className="input-group">
                <label><Zap size={16} /> Identificador (Slug)</label>
                <input
                  name="schema_name"
                  value={form.schema_name}
                  disabled
                  placeholder="mi_boutique_online"
                />
              </div>

              <div className="input-group">
                <label><Globe size={16} /> Dominio</label>
                <input
                  name="dominio"
                  value={form.dominio}
                  disabled
                  placeholder="mi_boutique.localhost"
                />
              </div>
            </div>

            <div className="section-title">
              <User size={18} /> Datos del Dueño
            </div>

            <div className="input-grid">
              <div className="input-group">
                <label>Nombre</label>
                <input
                  name="first_name"
                  value={form.first_name}
                  onChange={handleChange}
                  placeholder="Tu nombre"
                  required
                />
              </div>

              <div className="input-group">
                <label>Apellido</label>
                <input
                  name="last_name"
                  value={form.last_name}
                  onChange={handleChange}
                  placeholder="Tu apellido"
                  required
                />
              </div>

              <div className="input-group full-width">
                <label><Mail size={16} /> Correo Electrónico</label>
                <input
                  type="email"
                  name="email"
                  value={form.email}
                  onChange={handleChange}
                  placeholder="ejemplo@correo.com"
                  required
                />
              </div>

              <div className="input-group full-width">
                <label><Lock size={16} /> Contraseña</label>
                <input
                  type="password"
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="Mínimo 6 caracteres"
                  required
                  minLength={6}
                />
              </div>
            </div>

            {error && (
              <div style={{ color: '#e74c3c', fontSize: '0.85rem', marginTop: 10, padding: 10, background: '#fdf2f2', borderRadius: 8 }}>
                <b>Error:</b> {typeof error === 'string' ? error : JSON.stringify(error)}
              </div>
            )}

            <button 
              type="submit" 
              className="btn-crear"
              disabled={status === "loading"}
            >
              {status === "loading" ? "Configurando tu tienda..." : "Crear Mi Tienda Ahora"}
            </button>
          </form>
        </div>

        {/* LADO DERECHO: BENEFICIOS */}
        <div className="info-side">
          <div className="benefit-item">
            <div className="benefit-icon"><Sparkles size={20} color="#18aea4" /></div>
            <div className="benefit-text">
              <h3>Inteligencia Artificial</h3>
              <p>Predice tus ventas y optimiza tu inventario automáticamente.</p>
            </div>
          </div>

          <div className="benefit-item">
            <div className="benefit-icon"><ShieldCheck size={20} color="#18aea4" /></div>
            <div className="benefit-text">
              <h3>Seguridad Total</h3>
              <p>Tus datos y los de tus clientes están protegidos con encriptación bancaria.</p>
            </div>
          </div>

          <div className="benefit-item">
            <div className="benefit-icon"><Globe size={20} color="#18aea4" /></div>
            <div className="benefit-text">
              <h3>Subdominio Propio</h3>
              <p>Obtén una URL personalizada y profesional para tu negocio al instante.</p>
            </div>
          </div>

          <div className="benefit-item" style={{ marginTop: 'auto', marginBottom: 0 }}>
             <p style={{ fontSize: '0.8rem', opacity: 0.6 }}>
               Al registrarte aceptas nuestros Términos y Condiciones y Política de Privacidad.
             </p>
          </div>
        </div>
      </div>
    </div>
  );
}