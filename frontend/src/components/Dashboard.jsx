import React, { useState, useEffect, useContext } from 'react';
import { 
  Package, 
  LogOut, 
  Plus, 
  Tag, 
  BarChart2, 
  LayoutDashboard,
  ShoppingCart,
  AlertCircle,
  TrendingUp,
  MoreVertical
} from 'lucide-react';
import api from '../services/api';
import { TenantContext } from '../contexts/TenantContext';

const Dashboard = ({ onLogout }) => {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const tenant = useContext(TenantContext);

  // --- LÓGICA LIMPIA: Solo pedimos los productos al cargar ---
  useEffect(() => {
    cargarProductos();
  }, []);

  const cargarProductos = async () => {
    setLoading(true);
    try {
      // Axios ya sabe qué token usar gracias a tu interceptor
      const response = await api.get('/productos/');
      setProductos(response.data);
      setError(null);
    } catch (err) {
      console.error("Error al cargar productos:", err);
      setError("No se pudo conectar con el servidor o sesión expirada.");
    } finally {
      setLoading(false);
    }
  };

  const valorTotal = productos.reduce((acc, curr) => acc + (parseFloat(curr.precio || 0) * (curr.stock || 0)), 0);
  const stockCritico = productos.filter(p => (p.stock || 0) < 10).length;

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      {/* Navbar */}
      <nav className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="bg-blue-600 p-2 rounded-xl">
                <ShoppingCart className="text-white w-5 h-5" />
              </div>
              <div className="flex flex-col">
                <span className="font-black text-slate-800 tracking-tighter leading-none uppercase italic">SaaS Multi-tenant</span>
                <span className="text-[10px] font-bold text-blue-600 uppercase tracking-widest mt-0.5">Tienda Activa: {tenant || 'Cargando...'}</span>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <button 
                onClick={onLogout} 
                className="text-slate-400 hover:text-red-500 transition-all p-2 rounded-full hover:bg-red-50"
                title="Cerrar Sesión"
              >
                <LogOut size={20} />
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Total SKU</p>
                <h3 className="text-3xl font-black text-slate-800">{productos.length}</h3>
              </div>
              <div className="bg-blue-50 p-3 rounded-2xl text-blue-600"><Package size={24} /></div>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Valor Total</p>
                <h3 className="text-3xl font-black text-slate-800">${valorTotal.toLocaleString()}</h3>
              </div>
              <div className="bg-green-50 p-3 rounded-2xl text-green-600"><TrendingUp size={24} /></div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Stock Bajo</p>
                <h3 className="text-3xl font-black text-slate-800">{stockCritico}</h3>
              </div>
              <div className={`p-3 rounded-2xl ${stockCritico > 0 ? 'bg-orange-100 text-orange-600' : 'bg-slate-50 text-slate-300'}`}>
                <BarChart2 size={24} />
              </div>
            </div>
          </div>
        </div>

        {/* Table Section */}
        <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
          <div className="p-6 border-b border-slate-50 flex justify-between items-center">
            <h2 className="text-xl font-extrabold text-slate-800 flex items-center gap-2">
              <LayoutDashboard className="text-blue-500" size={20} />
              Inventario de {tenant}
            </h2>
            <button className="bg-slate-900 hover:bg-black text-white px-5 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 transition-all shadow-lg active:scale-95">
              <Plus size={18} /> Nuevo Producto
            </button>
          </div>

          {loading ? (
            <div className="p-24 text-center">
              <div className="animate-spin w-10 h-10 border-4 border-blue-100 border-t-blue-600 rounded-full mx-auto mb-4"></div>
              <p className="text-slate-400 font-bold text-sm tracking-widest uppercase italic">Sincronizando esquema...</p>
            </div>
          ) : error ? (
            <div className="p-20 text-center">
              <AlertCircle className="mx-auto text-red-300 mb-4" size={48} />
              <p className="text-red-500 font-bold">{error}</p>
              <button onClick={cargarProductos} className="mt-4 text-xs font-black text-blue-600 underline uppercase tracking-widest">Reintentar Conexión</button>
            </div>
          ) : productos.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="bg-slate-50/50">
                    <th className="p-5 text-[10px] font-black text-slate-400 uppercase tracking-widest">Producto</th>
                    <th className="p-5 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Disponibilidad</th>
                    <th className="p-5 text-[10px] font-black text-slate-400 uppercase tracking-widest">Precio Unitario</th>
                    <th className="p-5 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Acción</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-50">
                  {productos.map((producto) => (
                    <tr key={producto.id} className="hover:bg-blue-50/20 transition-colors group">
                      <td className="p-5">
                        <div className="flex items-center gap-4">
                          <div className="w-12 h-12 bg-slate-100 rounded-2xl flex items-center justify-center text-slate-400 group-hover:bg-blue-100 group-hover:text-blue-500 transition-all">
                            <Package size={22} />
                          </div>
                          <div>
                            <p className="font-bold text-slate-800">{producto.nombre}</p>
                            <p className="text-xs text-slate-400 truncate max-w-[200px]">{producto.descripcion || "Sin descripción disponible"}</p>
                          </div>
                        </div>
                      </td>
                      <td className="p-5 text-center">
                        <span className={`inline-flex px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-tighter ${
                          (producto.stock || 0) > 20 ? 'bg-green-100 text-green-700' : 
                          (producto.stock || 0) > 0 ? 'bg-orange-100 text-orange-600' : 'bg-red-100 text-red-600'
                        }`}>
                          {producto.stock || 0} UNIDADES
                        </span>
                      </td>
                      <td className="p-5">
                        <span className="font-black text-slate-700 text-lg">${parseFloat(producto.precio || 0).toLocaleString()}</span>
                      </td>
                      <td className="p-5 text-right">
                        <button className="text-slate-300 hover:text-blue-600 transition-colors">
                          <MoreVertical size={20} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-20 text-center">
              <Tag className="mx-auto text-slate-200 mb-4" size={56} />
              <h3 className="font-bold text-slate-800 text-xl">Sin datos</h3>
              <p className="text-slate-400 text-sm mb-8">No se encontraron productos en la base de datos de {tenant}.</p>
              <button 
                onClick={cargarProductos} 
                className="bg-blue-600 text-white px-8 py-3 rounded-xl text-xs font-bold shadow-lg shadow-blue-100 hover:bg-blue-700 transition-all"
              >
                RECARGAR
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;