import React, { useState, useContext } from 'react';
import { 
  LayoutDashboard, 
  Package, 
  ShoppingCart, 
  Users, 
  Settings, 
  LogOut, 
  Plus,
  Search,
  Bell
} from 'lucide-react';
import { TenantContext } from '../contexts/TenantContext';
import './Dashboard.css';

const Dashboard = () => {
  // Obtener el tenant del contexto
  const tenant = useContext(TenantContext);

  // Mapeo de tenants a nombres amigables
  const tenantNames = {
    'cliente1': 'Tienda de Tecnología',
    'cliente2': 'Boutique de Ropa',
    'localhost': 'Panel Global'
  };

  // Obtener nombre del tenant actual
  const clientName = tenantNames[tenant] || tenant;

  // Datos de prueba para tus productos 
  const [products] = useState([
    { id: 1, name: 'Camiseta Algodón', price: 85, stock: 12, category: 'Ropa' },
    { id: 2, name: 'Gorra MiQhatu', price: 45, stock: 5, category: 'Accesorios' },
    { id: 3, name: 'Taza Pixel Art', price: 30, stock: 25, category: 'Hogar' },
  ]);

  return (
    <div className="dashboard-container">
      {/* 1. SIDEBAR */}
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
          <a href="/login" className="nav-item logout"><LogOut size={20} /> Salir</a>
        </nav>
      </aside>

      {/* 2. MAIN CONTENT */}
      <main className="main-content">
        {/* TOPBAR */}
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

        {/* DASHBOARD BODY */}
        <div className="dashboard-body">
          <div className="welcome-header">
            <div>
              <h1>Bienvenido a {clientName}</h1>
              <p className="welcome-subtitle">Gestiona tu inventario, ventas y clientes</p>
            </div>
            <button className="btn-add">
              <Plus size={18} /> Nuevo Producto
            </button>
          </div>

          {/* STATS CARDS */}
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">Ventas Totales</span>
              <h2 className="stat-value">BS. 4,250</h2>
              <span className="stat-change positive">+12% este mes</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Productos Activos</span>
              <h2 className="stat-value">{products.length}</h2>
              <span className="stat-change">Actualizado ahora</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Nuevos Clientes</span>
              <h2 className="stat-value">18</h2>
              <span className="stat-change positive">+5 hoy</span>
            </div>
          </div>

          {/* PRODUCT TABLE */}
          <div className="table-container">
            <div className="table-header">
              <h3>Inventario Reciente</h3>
              <a href="#">Ver todo</a>
            </div>
            <table className="products-table">
              <thead>
                <tr>
                  <th>Producto</th>
                  <th>Categoría</th>
                  <th>Precio</th>
                  <th>Stock</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {products.map(prod => (
                  <tr key={prod.id}>
                    <td>{prod.name}</td>
                    <td><span className="cat-badge">{prod.category}</span></td>
                    <td>BS. {prod.price}</td>
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
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;