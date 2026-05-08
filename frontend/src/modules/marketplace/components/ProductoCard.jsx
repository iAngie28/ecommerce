export default function ProductoCard({ producto, onAdd }) {
  if (!producto) return null;

  const stock = Number(producto.stock || 0);

  return (
    <div
      style={{
        border: '1px solid #ddd',
        borderRadius: '4px',
        padding: '12px',
        backgroundColor: '#fff',
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
        minHeight: '160px',
      }}
    >
      <h4 style={{ margin: '0 0 4px 0', fontSize: '14px', fontWeight: 'bold' }}>
        {producto.nombre}
      </h4>

      {producto.descripcion && (
        <p style={{ margin: '0', fontSize: '12px', color: '#666' }}>
          {producto.descripcion}
        </p>
      )}

      <p style={{ margin: '0', fontSize: '11px', color: '#999' }}>
        Stock: {stock}
      </p>

      <div
        style={{
          marginTop: 'auto',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          borderTop: '1px solid #eee',
          paddingTop: '8px',
          gap: '8px',
        }}
      >
        <span style={{ fontSize: '16px', fontWeight: 'bold', color: '#007bff' }}>
          ${Number(producto.precio || 0).toFixed(2)}
        </span>
        <button
          type="button"
          onClick={() => onAdd(producto)}
          disabled={stock <= 0}
          style={{
            padding: '8px 10px',
            backgroundColor: stock > 0 ? '#007bff' : '#ccc',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: stock > 0 ? 'pointer' : 'not-allowed',
            fontSize: '12px',
          }}
        >
          Agregar
        </button>
      </div>
    </div>
  );
}
