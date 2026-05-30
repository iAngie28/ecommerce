import { useState } from 'react';
import { X, Package, User, CreditCard, Calendar, Truck, CheckCircle } from 'lucide-react';
import { Button, Badge, Spinner } from 'shared/components';
import { ventasApi } from '../services/ventasApi';

export default function PedidoDetailModal({ open, pedido, onClose, onStatusChanged }) {
  const [loadingAction, setLoadingAction] = useState(false);

  if (!open || !pedido) return null;

  const handleCambiarEstado = async (nuevoEstado) => {
    if (!window.confirm(`¿Estás seguro de cambiar el estado a ${nuevoEstado}?`)) return;
    setLoadingAction(true);
    try {
      await ventasApi.cambiarEstado(pedido.id, nuevoEstado);
      if (onStatusChanged) onStatusChanged();
      onClose();
    } catch (err) {
      alert("Error al cambiar de estado");
      console.error(err);
    } finally {
      setLoadingAction(false);
    }
  };

  const getStatusColor = (estado) => {
    switch (estado?.toUpperCase()) {
      case 'PENDIENTE': return 'warning';
      case 'PAGADO': return 'info';
      case 'PROCESADO': return 'primary';
      case 'ENVIADO': return 'success';
      case 'ENTREGADO': return 'default';
      case 'CANCELADO': return 'danger';
      default: return 'default';
    }
  };

  return (
    <div 
      style={{
        position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh',
        backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1000,
        display: 'flex', justifyContent: 'center', alignItems: 'center'
      }}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div style={{
        backgroundColor: 'var(--color-surface)',
        borderRadius: 'var(--radius-lg)',
        width: '90%', maxWidth: '600px',
        maxHeight: '90vh', overflowY: 'auto',
        boxShadow: 'var(--shadow-xl)'
      }}>
        <div style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          padding: 'var(--space-4)', borderBottom: '1px solid var(--color-border)'
        }}>
          <h2 style={{ margin: 0, fontSize: 'var(--text-lg)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Package size={20} /> Pedido #{pedido.id}
          </h2>
          <button onClick={onClose} style={{
            background: 'none', border: 'none', cursor: 'pointer', color: 'var(--color-text-muted)'
          }}>
            <X size={20} />
          </button>
        </div>

        <div style={{ padding: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
          {/* Detalles del Cliente y Pedido */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-4)' }}>
            <div style={{
              padding: 'var(--space-3)', backgroundColor: 'var(--color-surface-2)', borderRadius: 'var(--radius-md)'
            }}>
              <h3 style={{ margin: '0 0 var(--space-2) 0', fontSize: 'var(--text-sm)', color: 'var(--color-text-muted)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <User size={14} /> Cliente
              </h3>
              <p style={{ margin: 0, fontWeight: '500' }}>{pedido.cliente_nombre}</p>
              <p style={{ margin: 0, fontSize: 'var(--text-sm)', color: 'var(--color-text-muted)' }}>{pedido.cliente_email}</p>
            </div>
            <div style={{
              padding: 'var(--space-3)', backgroundColor: 'var(--color-surface-2)', borderRadius: 'var(--radius-md)'
            }}>
              <h3 style={{ margin: '0 0 var(--space-2) 0', fontSize: 'var(--text-sm)', color: 'var(--color-text-muted)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Calendar size={14} /> Fecha
              </h3>
              <p style={{ margin: 0, fontWeight: '500' }}>{new Date(pedido.fecha_creacion).toLocaleString()}</p>
              <p style={{ margin: '4px 0 0 0' }}>
                <Badge variant={getStatusColor(pedido.estado)}>
                  {pedido.estado}
                </Badge>
              </p>
            </div>
          </div>

          {/* Lista de Items */}
          <div>
            <h3 style={{ margin: '0 0 var(--space-3) 0', fontSize: 'var(--text-md)' }}>Productos comprados</h3>
            <div style={{ border: '1px solid var(--color-border)', borderRadius: 'var(--radius-md)', overflow: 'hidden' }}>
              {pedido.items && pedido.items.length > 0 ? (
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: 'var(--text-sm)' }}>
                  <thead style={{ backgroundColor: 'var(--color-surface-2)', borderBottom: '1px solid var(--color-border)' }}>
                    <tr>
                      <th style={{ padding: 'var(--space-2) var(--space-3)' }}>Producto</th>
                      <th style={{ padding: 'var(--space-2) var(--space-3)', textAlign: 'center' }}>Cant.</th>
                      <th style={{ padding: 'var(--space-2) var(--space-3)', textAlign: 'right' }}>Precio Unit.</th>
                      <th style={{ padding: 'var(--space-2) var(--space-3)', textAlign: 'right' }}>Subtotal</th>
                    </tr>
                  </thead>
                  <tbody>
                    {pedido.items.map((item, idx) => (
                      <tr key={item.id || idx} style={{ borderBottom: '1px solid var(--color-border)' }}>
                        <td style={{ padding: 'var(--space-2) var(--space-3)' }}>{item.producto_nombre}</td>
                        <td style={{ padding: 'var(--space-2) var(--space-3)', textAlign: 'center' }}>{item.cantidad}</td>
                        <td style={{ padding: 'var(--space-2) var(--space-3)', textAlign: 'right' }}>Bs. {item.producto_precio}</td>
                        <td style={{ padding: 'var(--space-2) var(--space-3)', textAlign: 'right', fontWeight: '500' }}>Bs. {item.subtotal}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p style={{ padding: 'var(--space-4)', textAlign: 'center', color: 'var(--color-text-muted)', margin: 0 }}>
                  No se encontraron items.
                </p>
              )}
            </div>
          </div>

          {/* Total */}
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            padding: 'var(--space-3)', backgroundColor: 'var(--color-surface-2)', borderRadius: 'var(--radius-md)'
          }}>
            <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '6px' }}>
              <CreditCard size={18} /> Total del Pedido
            </h3>
            <span style={{ fontSize: 'var(--text-xl)', fontWeight: 'bold', color: 'var(--color-primary)' }}>
              Bs. {pedido.total_pedido}
            </span>
          </div>

        </div>

        <div style={{
          padding: 'var(--space-4)', borderTop: '1px solid var(--color-border)',
          display: 'flex', justifyContent: 'space-between', alignItems: 'center'
        }}>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <span style={{ fontSize: 'var(--text-sm)', fontWeight: '500' }}>Actualizar estado:</span>
            <select
              style={{
                padding: 'var(--space-2) var(--space-3)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--color-border)',
                backgroundColor: 'var(--color-surface)',
                color: 'var(--color-text)',
                fontSize: 'var(--text-sm)'
              }}
              value={pedido.estado}
              onChange={(e) => handleCambiarEstado(e.target.value)}
              disabled={loadingAction}
            >
              <option value="PENDIENTE">Pendiente</option>
              <option value="PAGADO">Pagado</option>
              <option value="PROCESADO">Procesado</option>
              <option value="ENVIADO">Enviado</option>
              <option value="ENTREGADO">Entregado</option>
              <option value="CANCELADO">Cancelado</option>
            </select>
            {loadingAction && <Spinner size="sm" />}
          </div>
          <Button onClick={onClose} variant="secondary" disabled={loadingAction}>Cerrar</Button>
        </div>
      </div>
    </div>
  );
}
