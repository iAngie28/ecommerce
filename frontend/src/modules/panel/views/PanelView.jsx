import { useState, useEffect } from 'react';
import { Plus, TrendingUp, Package, AlertTriangle } from 'lucide-react';
import AppView   from 'shared/widgets/AppView/AppView';
import StatCard  from 'shared/widgets/StatCard/StatCard';
import DataTable from 'shared/widgets/DataTable/DataTable';
import { Button, Badge, Alert } from 'shared/components';
import { useTenant } from 'core/hooks/useTenant';
import api from 'core/services/api';

// ─── Columnas de la tabla de productos ───────────────────────
const COLUMNS = [
  { key: 'nombre',      label: 'Producto',    render: (v) => <strong style={{ color: 'var(--color-text)' }}>{v}</strong> },
  { key: 'descripcion', label: 'Descripción', render: (v) => v || '—' },
  { key: 'precio',      label: 'Precio',      render: (v) => `BS. ${parseFloat(v).toLocaleString()}` },
  { key: 'stock',       label: 'Stock',       align: 'center', render: (v) => `${v} un.` },
  {
    key: 'stock',
    label: 'Estado',
    align: 'center',
    render: (v) => (
      <Badge variant={v < 10 ? 'warning' : 'success'} dot>
        {v < 10 ? 'Bajo Stock' : 'Disponible'}
      </Badge>
    ),
  },
];

export default function PanelView() {
  const tenant = useTenant();
  const [products, setProducts] = useState([]);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const res  = await api.get('/productos/');
        const data = res.data;
        const list = Array.isArray(data) ? data : Array.isArray(data?.results) ? data.results : [];
        setProducts(list);
        setError(null);
      } catch {
        setError('No se pudo conectar con el servidor.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [tenant]);

  const valorTotal  = products.reduce((acc, p) => acc + parseFloat(p.precio || 0) * (p.stock || 0), 0);
  const stockBajo   = products.filter((p) => p.stock < 10).length;

  return (
    <AppView
      title={`Bienvenido, ${tenant}`}
      subtitle="Resumen del inventario y actividad de tu tienda."
      actions={
        <Button leftIcon={<Plus size={16} />}>
          Nuevo Producto
        </Button>
      }
    >
      {error && <Alert variant="danger">{error}</Alert>}

      {/* KPI Cards */}
      <StatCard.Group>
        <StatCard
          label="Valor del Inventario"
          value={`BS. ${valorTotal.toLocaleString()}`}
          change="Calculado en tiempo real"
          trend="neutral"
          icon={<TrendingUp size={18} />}
        />
        <StatCard
          label="Productos Activos"
          value={products.length}
          change="Sincronizado con API"
          trend="positive"
          icon={<Package size={18} />}
          accentColor="var(--color-accent)"
        />
        <StatCard
          label="Stock Crítico"
          value={stockBajo}
          change={stockBajo > 0 ? 'Requieren atención' : 'Todo en orden'}
          trend={stockBajo > 0 ? 'negative' : 'positive'}
          icon={<AlertTriangle size={18} />}
          accentColor={stockBajo > 0 ? 'var(--color-warning)' : 'var(--color-success)'}
        />
      </StatCard.Group>

      {/* Tabla de productos */}
      <DataTable
        title="Inventario de Base de Datos"
        columns={COLUMNS}
        data={products}
        loading={loading}
        emptyText="No hay productos registrados para este tenant."
        footer={!loading ? `Mostrando ${products.length} producto${products.length !== 1 ? 's' : ''}` : ''}
      />
    </AppView>
  );
}
