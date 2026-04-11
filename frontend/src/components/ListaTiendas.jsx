import { useState, useEffect } from "react";
import api from "../services/api";

const th = { padding: "10px 14px", textAlign: "left", fontWeight: "bold" };
const td = { padding: "10px 14px", borderBottom: "1px solid #ddd" };

export default function ListaTiendas() {
  const [tiendas, setTiendas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null); // ✅ corregido

  useEffect(() => {
    api.get("/tiendas/")
      .then(res => {
        setTiendas(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Error al cargar tiendas");
        setLoading(false);
      });
  }, []);

  if (loading) return <p style={{ textAlign: "center" }}>Cargando tiendas...</p>;
  if (error) return <p style={{ color: "red", textAlign: "center" }}>{error}</p>;

  return (
    <div style={{ maxWidth: 700, margin: "auto", padding: 24 }}>
      <h2>🏪 Tiendas Registradas</h2>

      {tiendas.length === 0 ? (
        <p>No hay tiendas registradas aún.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#1976d2", color: "#fff" }}>
              <th style={th}>#</th>
              <th style={th}>Nombre</th>
              <th style={th}>Schema</th>
              <th style={th}>Dominio</th>
              <th style={th}>Acceso</th>
            </tr>
          </thead>
          <tbody>
            {tiendas.map((t, i) => (
              <tr
                key={t.schema}
                style={{ background: i % 2 === 0 ? "#f5f5f5" : "#fff" }}
              >
                <td style={td}>{i + 1}</td>
                <td style={td}>{t.nombre}</td>
                <td style={td}>{t.schema}</td>
                <td style={td}>{t.dominio}</td>
                <td style={td}>
                  <a
                    href={`http://${t.dominio}:3000/login`}
                    target="_blank"
                    rel="noreferrer"
                    style={{ color: "#1976d2" }}
                  >
                    Ir al login →
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <br />

      <a href="/crear-tienda" style={{ color: "#1976d2" }}>
        + Crear nueva tienda
      </a>
    </div>
  );
}