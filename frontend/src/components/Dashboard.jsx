import React, { useState, useEffect, useContext } from 'react';
import { 
  LayoutDashboard, 
  Package, 
  ShoppingCart, 
  Users, 
  Settings, 
  LogOut, 
  Plus,
  Search,
  Bell,
  AlertCircle // Añadido para mostrar errores
} from 'lucide-react';
import { TenantContext } from '../contexts/TenantContext';
import api from '../services/api'; // Tu servicio de API
import './Dashboard.css';

const Dashboard = ({ onLogout }) => {
  // 1. ESTADOS Y CONTEXTO
  const tenant = useContext(TenantContext);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const tenantNames = {
    'cliente1': 'Tienda de Tecnología',
    'cliente2': 'Boutique de Ropa',
    'localhost': 'Panel Global'
  };
  
  const clientName = tenantNames[tenant] || tenant;

  // 2. LÓGICA DE CARGA (Traída de tu dashboard anterior)
  useEffect(() => {
    const cargarProductos = async () => {
      setLoading(true);
      try {
        const response = await api.get('/productos/');
        setProducts(response.data);
        setError(null);
      } catch (err) {
        console.error("Error al cargar productos:", err);
        setError("No se pudo conectar con el servidor.");
      } finally {
        setLoading(false);
      }
    };

    cargarProductos();
  }, [tenant]); // Se recarga si el tenant cambia

  // 3. CÁLCULOS DINÁMICOS
  const valorTotal = products.reduce((acc, curr) => 
    acc + (parseFloat(curr.precio || 0) * (curr.stock || 0)), 0
  );

  return (
    <div className="dashboard-container">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <div className="logo-icon">M</div>
          <span className="brand-name">MiQhatu</span>
        </div>
        
        <nav className="sidebar-nav">
          <a href="#" className="nav-item active"><LayoutDashboard size={20} /> Panel</a>
          <a href="#" className="nav-item"><Package size={20} /> Productos</a>
          <a href="#" className="nav-item"><ShoppingCart size={20} /> Ventas</a>
          <a href="#" className="nav-item"><Users size={20} /> Clientes</a>
          <div className="nav-divider"></div>
          <a href="#" className="nav-item"><Settings size={20} /> Configuración</a>
          <button onClick={onLogout} className="nav-item logout" style={{width: '100%', border: 'none', background: 'none', cursor: 'pointer'}}>
            <LogOut size={20} /> Salir
          </button>
        </nav>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">
        <header className="topbar">
          <div className="search-bar">
            <Search size={18} />
            <input type="text" placeholder="Buscar productos..." />
          </div>
          <div className="topbar-actions">
            <div className="tenant-badge">
              <span className="badge-label">Tienda Activa:</span>
              <span className="badge-value">{clientName}</span>
            </div>
            <Bell size={20} className="icon-btn" />
            <div className="user-profile">
              <img src="https://ui-avatars.com/api/?name=Jhenny+Solis&background=18aea4&color=fff" alt="User" />
              <span>Jhenny Solis</span>
            </div>
          </div>
        </header>

        <div className="dashboard-body">
          <div className="welcome-header">
            <div>
              <h1>Bienvenido a {clientName}</h1>
              <p className="welcome-subtitle">Gestiona tu inventario real de {tenant}</p>
            </div>
            <button className="btn-add">
              <Plus size={18} /> Nuevo Producto
            </button>
          </div>

          {/* STATS CARDS (Ahora con datos reales) */}
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">Valor del Inventario</span>
              <h2 className="stat-value">BS. {valorTotal.toLocaleString()}</h2>
              <span className="stat-change positive">Calculado en tiempo real</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Productos Activos</span>
              <h2 className="stat-value">{products.length}</h2>
              <span className="stat-change">Sincronizado con API</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Stock Crítico</span>
              <h2 className="stat-value">{products.filter(p => p.stock < 10).length}</h2>
              <span className="stat-change {products.filter(p => p.stock < 10).length > 0 ? 'negative' : 'positive'}">
                Requieren atención
              </span>
            </div>
          </div>

          {/* PRODUCT TABLE */}
          <div className="table-container">
            <div className="table-header">
              <h3>Inventario de la Base de Datos</h3>
              {loading && <span className="loading-spinner">Cargando...</span>}
            </div>

            {error ? (
              <div className="error-message" style={{padding: '20px', textAlign: 'center', color: 'red'}}>
                <AlertCircle size={40} />
                <p>{error}</p>
              </div>
            ) : (
              <table className="products-table">
                <thead>
                  <tr>
                    <th>Producto</th>
                    <th>Descripción</th>
                    <th>Precio</th>
                    <th>Stock</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {products.map(prod => (
                    <tr key={prod.id}>
                      <td><strong>{prod.nombre}</strong></td>
                      <td style={{fontSize: '0.85rem', color: '#666'}}>{prod.descripcion || 'Sin descripción'}</td>
                      <td>BS. {parseFloat(prod.precio).toLocaleString()}</td>
                      <td>{prod.stock} un.</td>
                      <td>
                        <span className={`status-pill ${prod.stock < 10 ? 'low' : 'ok'}`}>
                          {prod.stock < 10 ? 'Bajo Stock' : 'Disponible'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            
            {!loading && products.length === 0 && !error && (
              <p style={{textAlign: 'center', padding: '20px'}}>No hay productos registrados para este tenant.</p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;