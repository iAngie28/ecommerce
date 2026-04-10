import { useState } from "react";

export default function CrearTienda() {
  const [form, setForm] = useState({
    nombre_tienda: "", schema_name: "", dominio: "",
    first_name: "", last_name: "", email: "", password: ""
  });
  const [mensaje, setMensaje] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    const updated = { ...form, [name]: value };

    if (name === "nombre_tienda") {
      const slug = value.toLowerCase()
        .replace(/\s+/g, '_')
        .replace(/[^a-z0-9_]/g, '');
      updated.schema_name = slug;
      updated.dominio = `${slug}.localhost`;
    }

    setForm(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setMensaje(null);
    try {
      const res = await fetch("http://localhost:8001/api/tiendas/crear/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) throw data;
      setMensaje(`✅ Tienda "${data.tienda}" creada. Accede en: http://${data.dominio}:3000/login`);
      setForm({ nombre_tienda: "", schema_name: "", dominio: "", first_name: "", last_name: "", email: "", password: "" });
    } catch (err) {
      setError(err);
    }
  };

  return (
    <div style={{ maxWidth: 450, margin: "auto", padding: 24 }}>
      <h2>Crear Nueva Tienda</h2>
      {mensaje && <p style={{ color: "green" }}>{mensaje}</p>}
      {error && <pre style={{ color: "red", fontSize: 12 }}>{JSON.stringify(error, null, 2)}</pre>}

      <form onSubmit={handleSubmit}>
        <h4 style={{ color: "#555" }}>📦 Datos de la Tienda</h4>
        {[
          { label: "Nombre de la tienda", name: "nombre_tienda", placeholder: "Ej: Tienda Ropa Valeria" },
          { label: "Schema (auto)", name: "schema_name", placeholder: "tienda_ropa_valeria" },
          { label: "Dominio (auto)", name: "dominio", placeholder: "tienda_ropa_valeria.localhost" },
        ].map(({ label, name, placeholder }) => (
          <div key={name} style={{ marginBottom: 12 }}>
            <label>{label}</label><br />
            <input
              name={name} value={form[name]} onChange={handleChange}
              placeholder={placeholder} required
              style={{ width: "100%", padding: 8 }}
            />
          </div>
        ))}

        <h4 style={{ color: "#555" }}>👤 Datos del Dueño (Admin)</h4>
        {[
          { label: "Nombre", name: "first_name" },
          { label: "Apellido", name: "last_name" },
          { label: "Email", name: "email", type: "email" },
          { label: "Contraseña", name: "password", type: "password" },
        ].map(({ label, name, type = "text" }) => (
          <div key={name} style={{ marginBottom: 12 }}>
            <label>{label}</label><br />
            <input
              type={type} name={name} value={form[name]}
              onChange={handleChange} required
              style={{ width: "100%", padding: 8 }}
            />
          </div>
        ))}

        <button type="submit" style={{
          width: "100%", padding: 10, background: "#1976d2",
          color: "#fff", border: "none", borderRadius: 4, cursor: "pointer"
        }}>
          Crear Tienda
        </button>
      </form>
    </div>
  );
}