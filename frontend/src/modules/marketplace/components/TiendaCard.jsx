export default function TiendaCard({ tienda }) {
  const handleVisit = () => {
    if (tienda.subdominio) {
      const port = window.location.port ? `:${window.location.port}` : '';
      const url = `${window.location.protocol}//${tienda.subdominio}${port}`;
      window.location.href = url;
    }
  };

  return (
    <div
      style={{
        border: '1px solid #ddd',
        borderRadius: '4px',
        padding: '16px',
        backgroundColor: '#fff',
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
        textAlign: 'center',
      }}
    >
      {tienda.logo_url && (
        <img
          src={tienda.logo_url}
          alt={tienda.nombre_comercial}
          style={{ width: '80px', height: '80px', objectFit: 'cover', margin: '0 auto', borderRadius: '4px' }}
        />
      )}

      <h3 style={{ margin: '0', fontSize: '16px', fontWeight: 'bold' }}>
        {tienda.nombre_comercial}
      </h3>

      {tienda.descripcion && (
        <p style={{ margin: '0', fontSize: '12px', color: '#666' }}>
          {tienda.descripcion}
        </p>
      )}

      {tienda.categoria_tienda && (
        <p style={{ margin: '0', fontSize: '11px', color: '#999' }}>
          {tienda.categoria_tienda}
        </p>
      )}

      <button
        type="button"
        onClick={handleVisit}
        disabled={!tienda.subdominio}
        style={{
          padding: '8px 12px',
          backgroundColor: tienda.subdominio ? '#007bff' : '#ccc',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: tienda.subdominio ? 'pointer' : 'not-allowed',
          fontSize: '13px',
          fontWeight: 'bold',
          marginTop: 'auto',
        }}
      >
        Visitar Tienda
      </button>
    </div>
  );
}
