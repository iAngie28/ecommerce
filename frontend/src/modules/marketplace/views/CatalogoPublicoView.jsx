import React, { useState, useEffect } from 'react';
import { useAuth } from 'core/hooks/useAuth';
import { getBaseDomain } from 'core/utils/domain';
import productosService from '../services/productosService';
import ProductoCard from '../components/ProductoCard';
import {
  addServerCartItem,
  addLocalCartItem,
  clearServerCart,
  clearLocalCart,
  getLocalCart,
  getLocalCartTotal,
  getServerCartItems,
  removeLocalCartItem,
  removeServerCartItem,
  syncLocalCart,
} from '../services/carritoService';

const readStoredAuth = () => ({
  token: localStorage.getItem('access_token') || '',
  name: localStorage.getItem('user_full_name') || '',
});

/**
 * CatalogoPublicoView - Catálogo público de productos
 * Escenario C: Visitante anónimo explora productos sin login
 */
export default function CatalogoPublicoView() {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [nextPage, setNextPage] = useState(null);
  const [prevPage, setPrevPage] = useState(null);
  const [cartItems, setCartItems] = useState(() => getLocalCart());
  const [syncMessage, setSyncMessage] = useState('');
  const [storedAuth, setStoredAuth] = useState(() => readStoredAuth());

  const { user, isAuthenticated, logout } = useAuth();

  const goToGlobalAuth = (path) => {
    const baseDomain = getBaseDomain(window.location.hostname);
    const port = window.location.port ? `:${window.location.port}` : '';
    const redirect = encodeURIComponent(window.location.hostname);
    window.location.href = `${window.location.protocol}//${baseDomain}${port}${path}?redirect=${redirect}`;
  };

  const pageSize = 12;

  // Cargar productos
  const loadProductos = async (page = 1) => {
    try {
      setLoading(true);
      setError(null);

      const response = await productosService.getProductos({
        page: page,
        page_size: pageSize,
      });

      setProductos(response.results || []);
      setTotalCount(response.count || 0);
      setNextPage(response.next);
      setPrevPage(response.previous);
      setCurrentPage(page);
    } catch (err) {
      console.error('Error cargando productos:', err);
      setError('No se pudieron cargar los productos');
      setProductos([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProductos(1);
  }, []);

  useEffect(() => {
    const refreshAuthAndCart = async () => {
      const nextAuth = readStoredAuth();
      setStoredAuth(nextAuth);

      if (!nextAuth.token) return;

      const localCart = getLocalCart();
      if (localCart.length) {
        setCartItems(localCart);
        return;
      }

      try {
        const { items } = await getServerCartItems();
        setCartItems(items);
      } catch (err) {
        console.error('Error cargando carrito persistido:', err);
      }
    };

    refreshAuthAndCart();

    const handleFocus = () => refreshAuthAndCart();
    window.addEventListener('focus', handleFocus);
    return () => window.removeEventListener('focus', handleFocus);
  }, []);

  const handleAddProduct = async (producto) => {
    setError(null);
    setSyncMessage('');

    if (localStorage.getItem('access_token')) {
      try {
        const { items } = await addServerCartItem(producto);
        setCartItems(items);
        setSyncMessage('Producto agregado al carrito persistido.');
      } catch (err) {
        console.error('Error agregando producto al carrito persistido:', err);
        setError(err.response?.data?.error || 'No se pudo agregar el producto al carrito.');
      }
      return;
    }

    setCartItems(addLocalCartItem(producto));
  };

  const handleRemoveProduct = async (productoId) => {
    setError(null);
    setCartItems(removeLocalCartItem(productoId));
    setSyncMessage('');

    const item = cartItems.find((cartItem) => cartItem.producto_id === productoId);
    if (localStorage.getItem('access_token') && item?.persisted) {
      try {
        const { items } = await removeServerCartItem(productoId);
        setCartItems(items);
      } catch (err) {
        console.error('Error quitando producto del carrito persistido:', err);
        setError(err.response?.data?.error || 'No se pudo quitar el producto del carrito.');
      }
    }
  };

  const handleClearCart = async () => {
    clearLocalCart();
    setCartItems([]);
    setSyncMessage('');

    if (localStorage.getItem('access_token')) {
      try {
        await clearServerCart();
      } catch (err) {
        console.error('Error vaciando carrito persistido:', err);
        setError(err.response?.data?.error || 'No se pudo vaciar el carrito persistido.');
      }
    }
  };

  const handleCheckout = async () => {
    setError(null);
    setSyncMessage('');

    if (!cartItems.length) {
      setError('El carrito está vacío.');
      return;
    }

    if (!localStorage.getItem('access_token')) {
      goToGlobalAuth('/login');
      return;
    }

    try {
      const localCart = getLocalCart();
      if (!localCart.length) {
        const { items } = await getServerCartItems();
        setCartItems(items);
        setSyncMessage('Carrito ya sincronizado en la tienda.');
        return;
      }

      const result = await syncLocalCart();
      setCartItems(result.items || []);
      setSyncMessage(`Carrito sincronizado. Items enviados: ${result.synced}.`);
    } catch (err) {
      console.error('Error sincronizando carrito:', err);
      setError(err.response?.data?.error || 'No se pudo sincronizar el carrito.');
    }
  };

  const handleNextPage = () => {
    if (nextPage) loadProductos(currentPage + 1);
  };

  const handlePrevPage = () => {
    if (prevPage) loadProductos(currentPage - 1);
  };

  const totalPages = Math.ceil(totalCount / pageSize);
  const cartTotal = getLocalCartTotal(cartItems);
  const hasSession = isAuthenticated || !!storedAuth.token;
  const displayName = user?.fullName || storedAuth.name || 'Cliente';

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', gap: '12px' }}>
        <div>
          <h1>Catálogo de Productos</h1>
          <p style={{ color: '#666', margin: 0 }}>Tienda actual: {window.location.hostname}</p>
        </div>

        {hasSession ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span>Bienvenido, {displayName}</span>
            <button
              type="button"
              onClick={logout}
              style={{
                padding: '8px 12px',
                backgroundColor: '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              Cerrar sesión
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              type="button"
              onClick={() => goToGlobalAuth('/login')}
              style={{
                padding: '10px 20px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              Iniciar sesión
            </button>
            <button
              type="button"
              onClick={() => goToGlobalAuth('/registro-cliente')}
              style={{
                padding: '10px 20px',
                backgroundColor: '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              Registrarme
            </button>
          </div>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 320px', gap: '20px', alignItems: 'start' }}>
        <div>
          {syncMessage && (
            <div style={{ padding: '12px', backgroundColor: '#d4edda', color: '#155724', borderRadius: '4px', marginBottom: '12px' }}>
              {syncMessage}
            </div>
          )}

          {loading && <p style={{ textAlign: 'center' }}>Cargando productos...</p>}

          {error && (
            <div style={{ padding: '12px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '12px' }}>
              {error}
            </div>
          )}

      {!loading && productos.length === 0 && !error && (
            <div style={{ padding: '20px', backgroundColor: '#e7f3ff', borderRadius: '4px', textAlign: 'center' }}>
              <p>Sin productos disponibles</p>
            </div>
      )}

      {!loading && productos.length > 0 && (
            <p style={{ fontSize: '12px', color: '#666', marginBottom: '12px' }}>
          Mostrando {productos.length} de {totalCount} productos (Página {currentPage} de {totalPages})
        </p>
      )}

      {!loading && productos.length > 0 && (
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
                gap: '12px',
                marginBottom: '20px',
              }}
            >
          {productos.map((producto) => (
            <ProductoCard key={producto.id} producto={producto} onAdd={handleAddProduct} />
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

        <aside
          style={{
            border: '1px solid #ddd',
            borderRadius: '4px',
            padding: '16px',
            backgroundColor: '#fff',
            position: 'sticky',
            top: '16px',
          }}
        >
          <h2 style={{ marginTop: 0 }}>Carrito</h2>

          {cartItems.length === 0 ? (
            <p>Carrito vacío.</p>
          ) : (
            <ul style={{ paddingLeft: '18px' }}>
              {cartItems.map((item) => (
                <li key={item.producto_id} style={{ marginBottom: '8px' }}>
                  <div>{item.nombre}</div>
                  <div>
                    x {item.cantidad} = ${(Number(item.precio || 0) * item.cantidad).toFixed(2)}
                  </div>
                  <button
                    type="button"
                    onClick={() => handleRemoveProduct(item.producto_id)}
                    style={{
                      padding: '4px 8px',
                      backgroundColor: '#dc3545',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      fontSize: '12px',
                    }}
                  >
                    Quitar
                  </button>
                </li>
              ))}
            </ul>
          )}

          <p style={{ fontWeight: 'bold' }}>Total: ${cartTotal.toFixed(2)}</p>

          <button
            type="button"
            onClick={handleCheckout}
            disabled={!cartItems.length}
            style={{
              width: '100%',
              padding: '10px 12px',
              backgroundColor: cartItems.length ? '#007bff' : '#ccc',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: cartItems.length ? 'pointer' : 'not-allowed',
              marginBottom: '8px',
            }}
          >
            Pagar
          </button>

          <button
            type="button"
            onClick={handleClearCart}
            disabled={!cartItems.length}
            style={{
              width: '100%',
              padding: '10px 12px',
              backgroundColor: cartItems.length ? '#6c757d' : '#ccc',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: cartItems.length ? 'pointer' : 'not-allowed',
            }}
          >
            Vaciar carrito local
          </button>

          {!hasSession && (
            <p style={{ fontSize: '12px', color: '#666' }}>
              Al pagar sin sesión se redirige al login global con la tienda actual.
            </p>
          )}
        </aside>
      </div>
    </div>
  );
}
