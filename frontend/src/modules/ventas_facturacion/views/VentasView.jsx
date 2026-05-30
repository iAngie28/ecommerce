import { useState, useEffect, useCallback, useMemo } from 'react';
import { ShoppingCart, RefreshCw, Eye, Calendar } from 'lucide-react';
import AppView from 'shared/widgets/AppView/AppView';
import { Button, Badge, Alert, Spinner } from 'shared/components';
import { ventasApi } from '../services/ventasApi';
import PedidoDetailModal from '../components/PedidoDetailModal';

export default function VentasView() {
  const [pedidos, setPedidos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedPedido, setSelectedPedido] = useState(null);

  const cargar = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await ventasApi.listarPedidos();
      const lista = Array.isArray(res.data) ? res.data : (res.data?.results ?? []);
      setPedidos(lista);
    } catch (err) {
      console.error(err);
      setError('No se pudieron cargar los pedidos. Verifica tu conexión.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    cargar();
    // Optional: Poll every 30 seconds to simulate real-time updates as requested
    const interval = setInterval(cargar, 30000);
    return () => clearInterval(interval);
  }, [cargar]);

  // Group by date (YYYY-MM-DD)
  const groupedPedidos = useMemo(() => {
    const groups = {};
    pedidos.forEach(p => {
      const dateObj = new Date(p.fecha_creacion);
      const dateStr = dateObj.toLocaleDateString('es-ES', { 
        year: 'numeric', month: 'long', day: 'numeric' 
      });
      if (!groups[dateStr]) groups[dateStr] = [];
      groups[dateStr].push(p);
    });
    // Sort groups descending by date
    return Object.entries(groups).sort((a, b) => {
      // Basic string sort works partially for ES locale, but better to parse the first item's actual date
      const dateA = new Date(a[1][0].fecha_creacion);
      const dateB = new Date(b[1][0].fecha_creacion);
      return dateB - dateA;
    });
  }, [pedidos]);

  return (
    <AppView 
      title="Ventas & Dashboard" 
      subtitle={`Tienes ${pedidos.length} ventas registradas`}
      actions={
        <Button
          variant="secondary"
          leftIcon={<RefreshCw size={15} />}
          onClick={cargar}
          disabled={loading}
        >
          {loading ? 'Actualizando...' : 'Actualizar'}
        </Button>
      }
    >
      {error && <Alert variant="danger">{error}</Alert>}

      {pedidos.length === 0 && !loading && !error ? (
        <div style={{ textAlign: 'center', padding: 'var(--space-8)', backgroundColor: 'var(--color-surface)', borderRadius: 'var(--radius-md)' }}>
          <ShoppingCart size={48} style={{ color: 'var(--color-text-muted)', marginBottom: 'var(--space-3)' }} />
          <h3>Aún no tienes ventas</h3>
          <p style={{ color: 'var(--color-text-muted)' }}>Las compras que realicen tus clientes aparecerán aquí automáticamente.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
          {groupedPedidos.map(([dateGroup, items]) => (
            <div key={dateGroup} style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
              
              <h3 style={{ 
                margin: 0, fontSize: 'var(--text-sm)', color: 'var(--color-text-muted)', 
                display: 'flex', alignItems: 'center', gap: '6px',
                borderBottom: '1px solid var(--color-border)', paddingBottom: 'var(--space-2)'
              }}>
                <Calendar size={14} /> {dateGroup}
              </h3>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 'var(--space-4)' }}>
                {items.map(pedido => (
                  <div 
                    key={pedido.id}
                    onClick={() => setSelectedPedido(pedido)}
                    style={{
                      backgroundColor: 'var(--color-surface)', border: '1px solid var(--color-border)',
                      borderRadius: 'var(--radius-md)', padding: 'var(--space-4)',
                      cursor: 'pointer', transition: 'box-shadow var(--transition-fast)',
                      display: 'flex', flexDirection: 'column', gap: 'var(--space-3)'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.boxShadow = 'var(--shadow-md)'}
                    onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'none'}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontWeight: '600' }}>#{pedido.id} - {pedido.cliente_nombre}</span>
                      <Badge variant={pedido.estado === 'PENDIENTE' ? 'warning' : 'success'}>
                        {pedido.estado}
                      </Badge>
                    </div>
                    
                    <div style={{ fontSize: 'var(--text-sm)', color: 'var(--color-text-secondary)' }}>
                      {pedido.items && pedido.items.length > 0 ? (
                        <span>{pedido.items.map(i => `${i.producto_nombre} (x${i.cantidad})`).join(', ')}</span>
                      ) : (
                        <span>{pedido.cantidad_items} items</span>
                      )}
                    </div>
                    
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'auto', paddingTop: 'var(--space-2)' }}>
                      <span style={{ fontWeight: 'bold', fontSize: 'var(--text-lg)', color: 'var(--color-primary)' }}>
                        Bs. {pedido.total_pedido}
                      </span>
                      <Button variant="ghost" size="sm" onClick={(e) => { e.stopPropagation(); setSelectedPedido(pedido); }}>
                        <Eye size={14} style={{ marginRight: 6 }} /> Detalles
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal Detalles */}
      <PedidoDetailModal 
        open={!!selectedPedido} 
        pedido={selectedPedido} 
        onClose={() => setSelectedPedido(null)}
        onStatusChanged={cargar}
      />
    </AppView>
  );
}
