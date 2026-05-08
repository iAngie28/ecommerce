
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from 'core/hooks/useAuth';
import marketplaceService from '../services/marketplaceService';
import TiendaCard from '../components/TiendaCard';

export default function MarketplaceView() {
  const [tiendas, setTiendas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [nextPage, setNextPage] = useState(null);
  const [prevPage, setPrevPage] = useState(null);
  
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate('/login');
  };

  const pageSize = 12;

  const loadTiendas = async (page = 1) => {
    try {
      setLoading(true);
      setError(null);

      const response = await marketplaceService.getTiendas({
        page: page,
        page_size: pageSize,
      });

      setTiendas(response.results || []);
      setTotalCount(response.count || 0);
      setNextPage(response.next);
      setPrevPage(response.previous);
      setCurrentPage(page);
    } catch (err) {
      console.error('Error cargando tiendas:', err);
      setError('No se pudieron cargar las tiendas');
      setTiendas([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTiendas(1);
  }, []);

  const handleNextPage = () => {
    if (nextPage) loadTiendas(currentPage + 1);
  };

  const handlePrevPage = () => {
    if (prevPage) loadTiendas(currentPage - 1);
  };

  const totalPages = Math.ceil(totalCount / pageSize);

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Directorio de Tiendas</h1>
        {isAuthenticated ? (
          <div style={{ fontSize: '16px', fontWeight: '500' }}>
            Bienvenido, {user?.fullName || 'Cliente'}
          </div>
        ) : (
          <button
            type="button"
            onClick={handleLogin}
            style={{
              padding: '10px 20px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            Iniciar Sesión
          </button>
        )}
      </div>
      
      <p style={{ color: '#666', marginBottom: '20px' }}>
        Descubre nuestras tiendas y explora sus productos
      </p>

      {loading && <p style={{ textAlign: 'center' }}>Cargando tiendas...</p>}

      {error && (
        <div style={{ padding: '12px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px' }}>
          {error}
        </div>
      )}

      {!loading && tiendas.length === 0 && !error && (
        <div style={{ padding: '20px', backgroundColor: '#e7f3ff', borderRadius: '4px', textAlign: 'center' }}>
          <p>Sin tiendas disponibles</p>
        </div>
      )}

      {!loading && tiendas.length > 0 && (
        <p style={{ fontSize: '12px', color: '#666', marginBottom: '12px' }}>
          Mostrando {tiendas.length} de {totalCount} tiendas
        </p>
      )}

      {!loading && tiendas.length > 0 && (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
            gap: '16px',
            marginBottom: '20px',
          }}
        >
          {tiendas.map((tienda) => (
            <TiendaCard key={tienda.id} tienda={tienda} />
          ))}
        </div>
      )}

      {!loading && totalPages > 1 && (
        <div style={{ display: 'flex', justifyContent: 'center', gap: '10px' }}>
          <button
            type="button"
            onClick={handlePrevPage}
            disabled={!prevPage}
            style={{
              padding: '8px 16px',
              backgroundColor: prevPage ? '#007bff' : '#ccc',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: prevPage ? 'pointer' : 'not-allowed',
            }}
          >
            ← Anterior
          </button>

          <span style={{ padding: '8px 12px', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>
            Página {currentPage} de {totalPages}
          </span>

          <button
            type="button"
            onClick={handleNextPage}
            disabled={!nextPage}
            style={{
              padding: '8px 16px',
              backgroundColor: nextPage ? '#007bff' : '#ccc',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: nextPage ? 'pointer' : 'not-allowed',
            }}
          >
            Siguiente →
          </button>
        </div>
      )}
    </div>
  );
}
