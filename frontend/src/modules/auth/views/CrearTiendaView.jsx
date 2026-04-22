import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Store, User, Mail, Lock, Globe, Building, CheckCircle2,
  ArrowRight, Sparkles, ShieldCheck, Zap
} from 'lucide-react';
import AuthLayout from 'shared/layouts/AuthLayout/AuthLayout';
import { Button, Input, Alert } from 'shared/components';
import styles from './AuthView.module.css';

const FEATURES = [
  { icon: <Sparkles size={18} />, title: 'Inteligencia Artificial', description: 'Predice tus ventas y optimiza tu inventario automáticamente.' },
  { icon: <ShieldCheck size={18} />, title: 'Seguridad Total', description: 'Tus datos protegidos con encriptación de grado bancario.' },
  { icon: <Globe size={18} />, title: 'Subdominio Propio', description: 'URL personalizada y profesional para tu negocio al instante.' },
];

export default function CrearTiendaView() {
  const [form, setForm] = useState({
    nombre_tienda: '', schema_name: '', dominio: '',
    first_name: '', last_name: '', email: '', password: '',
  });
  const [status,       setStatus]       = useState('idle');
  const [responseData, setResponseData] = useState(null);
  const [error,        setError]        = useState(null);

  useEffect(() => {
    if (!form.nombre_tienda) return;
    const slug = form.nombre_tienda.toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/\s+/g, 'x').replace(/[^a-z0-9]/g, '');

    const baseDomain = process.env.REACT_APP_BASE_DOMAIN || 'localhost';
    const suffix     = process.env.REACT_APP_TENANT_DOMAIN_SUFFIX;
    const dominio    = suffix
      ? `${slug}${suffix}`
      : baseDomain !== 'localhost'
        ? `${slug}.${baseDomain}.nip.io`
        : `${slug}.localhost`;

    setForm((prev) => ({ ...prev, schema_name: slug, dominio }));
  }, [form.nombre_tienda]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('loading');
    setError(null);
    try {
      const apiBase = process.env.REACT_APP_API_URL
        ? process.env.REACT_APP_API_URL.replace('/api', '')
        : window.location.hostname === 'localhost'
          ? 'http://localhost:8001'
          : `${window.location.protocol}//${window.location.hostname}:8001`;

      const res  = await fetch(`${apiBase}/api/tiendas/crear/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) throw data;
      setResponseData(data);
      setStatus('success');
    } catch (err) {
      setError(err);
      setStatus('error');
    }
  };

  if (status === 'success') {
    return (
      <AuthLayout features={FEATURES}>
        <div className={styles.successBox}>
          <div className={styles.successIcon}>
            <CheckCircle2 size={36} />
          </div>
          <div>
            <h2 style={{ fontSize: 'var(--text-2xl)', fontWeight: 'var(--font-extra)', color: 'var(--color-text)', marginBottom: '8px' }}>
              ¡Tu tienda está lista!
            </h2>
            <p style={{ marginBottom: '16px' }}>Todo configurado. Empieza a vender hoy.</p>
          </div>
          <div className={styles.urlBox}>
            <p>Tu dominio exclusivo:</p>
            <strong>{responseData.dominio}</strong>
          </div>
          <p style={{ fontSize: 'var(--text-sm)', color: 'var(--color-text-muted)' }}>
            Inicia sesión con <strong>{responseData.admin_email}</strong>
          </p>
          <Button as="a" href="/login" rightIcon={<ArrowRight size={16} />} fullWidth>
            Ir a mi tienda
          </Button>
        </div>
      </AuthLayout>
    );
  }

  return (
    <AuthLayout features={FEATURES}>
      <div className={styles.formWrap}>
        <div className={styles.formHeader}>
          <h1 className={styles.formTitle}>Crea tu Negocio</h1>
          <p className={styles.formSubtitle}>Únete a cientos de emprendedores con MiQhatu.</p>
        </div>

        {error && (
          <Alert variant="danger" title="Error al crear tienda">
            {typeof error === 'string' ? error : JSON.stringify(error)}
          </Alert>
        )}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.sectionTitle}><Store size={16} /> Datos de la Tienda</div>

          <Input
            id="ct-nombre"
            label={<><Building size={14} /> Nombre de la Tienda</>}
            name="nombre_tienda"
            value={form.nombre_tienda}
            onChange={handleChange}
            placeholder="Ej: Mi Boutique Online"
            required
          />

          <div className={styles.twoCol}>
            <Input id="ct-slug" label={<><Zap size={14} /> Slug</>} name="schema_name" value={form.schema_name} disabled />
            <Input id="ct-dominio" label={<><Globe size={14} /> Dominio</>} name="dominio" value={form.dominio} disabled />
          </div>

          <div className={styles.sectionTitle}><User size={16} /> Datos del Dueño</div>

          <div className={styles.twoCol}>
            <Input id="ct-firstname" label="Nombre" name="first_name" value={form.first_name} onChange={handleChange} placeholder="Tu nombre" required />
            <Input id="ct-lastname"  label="Apellido" name="last_name" value={form.last_name} onChange={handleChange} placeholder="Tu apellido" required />
          </div>

          <Input id="ct-email" label={<><Mail size={14} /> Correo Electrónico</>} type="email" name="email" value={form.email} onChange={handleChange} placeholder="ejemplo@correo.com" required />
          <Input id="ct-pass"  label={<><Lock size={14} /> Contraseña</>} type="password" name="password" value={form.password} onChange={handleChange} placeholder="Mínimo 6 caracteres" required minLength={6} />

          <Button type="submit" fullWidth loading={status === 'loading'} style={{ marginTop: '8px' }}>
            Crear Mi Tienda Ahora
          </Button>
        </form>

        <p className={styles.footer}>
          ¿Ya tienes cuenta? <Link to="/login">Iniciar sesión</Link>
        </p>
      </div>
    </AuthLayout>
  );
}
