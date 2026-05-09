import { useState, useEffect, useCallback } from 'react';
import { Search, X, Shield, RefreshCw } from 'lucide-react';
import { bitacoraApi } from '../services/bitacoraApi';
import './bitacora.css';

// ─── Helpers ────────────────────────────────────────────────────
const ACCION_COLORS = {
  LOGIN:    { bg: '#dcfce7', color: '#16a34a' },
  LOGOUT:   { bg: '#fef9c3', color: '#ca8a04' },
  CREAR:    { bg: '#dbeafe', color: '#2563eb' },
  EDITAR:   { bg: '#ede9fe', color: '#7c3aed' },
  ELIMINAR: { bg: '#fee2e2', color: '#dc2626' },
};

function accionBadge(accion) {
  const upper = accion?.toUpperCase();
  const style = ACCION_COLORS[upper] || { bg: '#f3f4f6', color: '#6b7280' };
  return (
    <span style={{
      background: style.bg, color: style.color,
      padding: '2px 10px', borderRadius: 999,
      fontSize: 11, fontWeight: 600, letterSpacing: 0.5,
    }}>
      {accion}
    </span>
  );
}

function formatFecha(iso) {
  if (!iso) return '-';
  const d = new Date(iso);
  return d.toLocaleString('es-BO', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

// ─── Fila ───────────────────────────────────────────────────────
function BitacoraRow({ registro }) {
  return (
    <tr className="bita-row">
      <td>{formatFecha(registro.fecha)}</td>
      <td>{registro.usuario_nombre}</td>
      <td>{registro.modulo}</td>
      <td>{accionBadge(registro.accion)}</td>
    </tr>
  );
}

// ─── Vista principal ────────────────────────────────────────────
export default function BitacoraView() {
  const [registros,  setRegistros]  = useState([]);
  const [loading,    setLoading]    = useState(true);
  const [error,      setError]      = useState('');
  const [search,     setSearch]     = useState('');
  const [filtroMod,  setFiltroMod]  = useState('');
  const [filtroAcc,  setFiltroAcc]  = useState('');
  const [fechaDesde, setFechaDesde] = useState('');
  const [fechaHasta, setFechaHasta] = useState('');

  const cargar = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params = {};
      if (filtroMod)  params.modulo      = filtroMod;
      if (filtroAcc)  params.accion      = filtroAcc;
      if (fechaDesde) params.fecha_desde = fechaDesde;
      if (fechaHasta) params.fecha_hasta = fechaHasta;
      const res = await bitacoraApi.listar(params);
      const data = Array.isArray(res.data) ? res.data : res.data?.results ?? [];
      setRegistros(data);
    } catch {
      setError('No se pudieron cargar los registros de auditoría.');
    } finally {
      setLoading(false);
    }
  }, [filtroMod, filtroAcc, fechaDesde, fechaHasta]);

  useEffect(() => { cargar(); }, [cargar]);

  const filtrados = registros.filter(r => {
    if (!search) return true;
    const q = search.toLowerCase();
    return (
      r.usuario_nombre?.toLowerCase().includes(q) ||
      r.modulo?.toLowerCase().includes(q) ||
      r.accion?.toLowerCase().includes(q)
    );
  });

  const modulos  = [...new Set(registros.map(r => r.modulo).filter(Boolean))];
  const acciones = [...new Set(registros.map(r => r.accion).filter(Boolean))];

  const limpiarFiltros = () => {
    setSearch(''); setFiltroMod(''); setFiltroAcc('');
    setFechaDesde(''); setFechaHasta('');
  };

  return (
    <div className="bita-page">
      {/* Header */}
      <div className="bita-header">
        <div>
          <h1 className="bita-title">
            <Shield size={20} style={{ display: 'inline', marginRight: 8 }} />
            Bitácora de Auditoría
          </h1>
          <p className="bita-subtitle">Registro de acciones del sistema</p>
        </div>
        <button className="bita-refresh" onClick={cargar} disabled={loading}>
          <RefreshCw size={15} className={loading ? 'bita-spin' : ''} />
          Actualizar
        </button>
      </div>

      {/* Filtros */}
      <div className="bita-filters">
        <div className="bita-search">
          <Search size={15} />
          <input
            placeholder="Buscar usuario, módulo, acción..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          {search && (
            <button onClick={() => setSearch('')}><X size={13} /></button>
          )}
        </div>

        <select value={filtroMod} onChange={e => setFiltroMod(e.target.value)}>
          <option value="">Todos los módulos</option>
          {modulos.map(m => <option key={m} value={m}>{m}</option>)}
        </select>

        <select value={filtroAcc} onChange={e => setFiltroAcc(e.target.value)}>
          <option value="">Todas las acciones</option>
          {acciones.map(a => <option key={a} value={a}>{a}</option>)}
        </select>

        <input type="date" value={fechaDesde} onChange={e => setFechaDesde(e.target.value)} title="Desde" />
        <input type="date" value={fechaHasta} onChange={e => setFechaHasta(e.target.value)} title="Hasta" />

        {(search || filtroMod || filtroAcc || fechaDesde || fechaHasta) && (
          <button className="bita-clear" onClick={limpiarFiltros}>
            <X size={13} /> Limpiar
          </button>
        )}
      </div>

      {/* Error */}
      {error && <div className="bita-error">{error}</div>}

      {/* Tabla */}
      <div className="bita-table-wrap">
        <table className="bita-table">
          <thead>
            <tr>
              <th>Fecha y Hora</th>
              <th>Usuario</th>
              <th>Módulo</th>
              <th>Acción</th>
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr><td colSpan={4} className="bita-center">Cargando...</td></tr>
            )}
            {!loading && filtrados.length === 0 && (
              <tr>
                <td colSpan={4} className="bita-center">
                  <Shield size={32} style={{ opacity: 0.2, display: 'block', margin: '0 auto 8px' }} />
                  No hay registros
                </td>
              </tr>
            )}
            {!loading && filtrados.map(r => (
              <BitacoraRow key={r.id} registro={r} />
            ))}
          </tbody>
        </table>
      </div>

      {/* Footer */}
      {!loading && (
        <div className="bita-footer">
          {filtrados.length} registro{filtrados.length !== 1 ? 's' : ''}
          {filtrados.length !== registros.length && ` (de ${registros.length} total)`}
        </div>
      )}
    </div>
  );
}