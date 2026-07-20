import React, { useEffect, useState } from 'react';
// import { Link } from 'react-router-dom'; // Asumiendo uso de react-router
import useWishlist from '../../hooks/useWishlist';
import './WishlistPage.css';

const WishlistPage = () => {
    const { 
        wishlistItems, 
        loading, 
        error, 
        fetchWishlist, 
        vaciarWishlist, 
        moverAlCarrito, 
        eliminarProducto 
    } = useWishlist();

    const [modalConfirmacion, setModalConfirmacion] = useState(false);

    useEffect(() => {
        fetchWishlist();
    }, [fetchWishlist]);

    const handleVaciar = async () => {
        await vaciarWishlist();
        setModalConfirmacion(false);
    };

    if (loading && wishlistItems.length === 0) {
        return <div className="wishlist-loading">Cargando tu lista de deseos...</div>;
    }

    if (error) {
        return <div className="wishlist-error">Error: {error}</div>;
    }

    return (
        <div className="wishlist-page">
            <div className="wishlist-header">
                <h2>Mi Lista de Deseos</h2>
                <div className="wishlist-meta">
                    <span className="wishlist-count">
                        {wishlistItems.length} {wishlistItems.length === 1 ? 'producto' : 'productos'}
                    </span>
                    {wishlistItems.length > 0 && (
                        <button 
                            className="btn-vaciar"
                            onClick={() => setModalConfirmacion(true)}
                        >
                            Vaciar Lista
                        </button>
                    )}
                </div>
            </div>

            {wishlistItems.length === 0 ? (
                <div className="wishlist-empty">
                    <div className="empty-icon">💔</div>
                    <h3>Tu lista de deseos está vacía</h3>
                    <p>Explora nuestro catálogo y guarda los productos que más te gusten.</p>
                    {/* <Link to="/productos" className="btn-explorar">Explorar Productos</Link> */}
                    <a href="/productos" className="btn-explorar">Explorar Productos</a>
                </div>
            ) : (
                <div className="wishlist-grid">
                    {wishlistItems.map((item) => (
                        <div key={item.id} className="wishlist-item-card">
                            <div className="item-image-container">
                                {/* placeholder imagen si no hay real */}
                                <img 
                                    src={item.producto.imagen || 'https://via.placeholder.com/300x200?text=Sin+Imagen'} 
                                    alt={item.producto.nombre} 
                                    className="item-image"
                                />
                                <button 
                                    className="btn-remove-item"
                                    onClick={() => eliminarProducto(item.producto.id)}
                                    title="Eliminar"
                                >
                                    ✕
                                </button>
                            </div>
                            <div className="item-details">
                                <h4 className="item-name">{item.producto.nombre}</h4>
                                <div className="item-price-row">
                                    <span className="item-price">${item.producto.precio}</span>
                                    {!item.producto.activo && (
                                        <span className="item-badge out-of-stock">Agotado</span>
                                    )}
                                </div>
                                <button 
                                    className="btn-mover-carrito"
                                    disabled={!item.producto.activo}
                                    onClick={() => moverAlCarrito(item.producto.id)}
                                >
                                    {item.producto.activo ? 'Mover al Carrito' : 'No disponible'}
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {modalConfirmacion && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h3>¿Estás seguro?</h3>
                        <p>Esta acción eliminará todos los productos de tu lista de deseos.</p>
                        <div className="modal-actions">
                            <button className="btn-cancel" onClick={() => setModalConfirmacion(false)}>Cancelar</button>
                            <button className="btn-confirm" onClick={handleVaciar}>Sí, vaciar</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default WishlistPage;
