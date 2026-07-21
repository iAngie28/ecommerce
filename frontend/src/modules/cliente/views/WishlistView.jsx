import React, { useState, useEffect, useCallback } from 'react';
import { Button } from 'shared/components';
import { Trash2, ShoppingCart, Heart } from 'lucide-react';
import api from 'core/services/api';
import { getTenantUrl, getApiUrl } from 'core/utils/domain';
import styles from './WishlistView.module.css';

const WishlistView = () => {
    const [wishlist, setWishlist] = useState(null);
    const [loading, setLoading] = useState(true);
    
    // Simple notification fallback
    const addNotification = useCallback((type, msg) => {
        if(type === 'error') alert('Error: ' + msg);
        else console.log(msg);
    }, []);

    const normalizeHost = (value) => {
        if (!value || typeof value !== 'string') return null;
        const trimmed = value.trim();
        if (!trimmed) return null;

        try {
            const parsed = new URL(trimmed.includes('://') ? trimmed : `${window.location.protocol}//${trimmed}`);
            return parsed.hostname;
        } catch (_) {
            return trimmed.split('/')[0] || null;
        }
    };

    const getItemTenantSchema = (item) => {
        const schema = normalizeHost(item.tienda_schema);
        if (schema) return schema.split('.')[0];

        const host = normalizeHost(item.tienda_host);
        return host ? host.split('.')[0] : null;
    };

    const getItemTenantUrl = (item) => {
        const host = normalizeHost(item.tienda_host);
        const port = window.location.port ? `:${window.location.port}` : '';
        if (host && host.includes('.')) {
            return `${window.location.protocol}//${host}${port}`;
        }

        const schema = getItemTenantSchema(item);
        return schema ? getTenantUrl(schema) : null;
    };

    const getWishlistActionUrl = (item, action) => {
        const tenantUrl = getItemTenantUrl(item);
        if (!tenantUrl) return `/wishlist/${action}/${item.producto.id}/`;

        const tenantHostname = new URL(tenantUrl).hostname;
        return `${getApiUrl(tenantHostname)}/wishlist/${action}/${item.producto.id}/`;
    };

    const fetchWishlist = useCallback(async () => {
        try {
            setLoading(true);
            const res = await api.get('/wishlist/');
            setWishlist(res.data);
        } catch (error) {
            console.error('Error fetching wishlist:', error);
            addNotification('error', 'Error al cargar tu lista de deseos');
        } finally {
            setLoading(false);
        }
    }, [addNotification]);

    useEffect(() => {
        fetchWishlist();
    }, [fetchWishlist]);

    const removeFromWishlist = async (item) => {
        try {
            await api.delete(getWishlistActionUrl(item, 'eliminar'));
            addNotification('success', 'Producto eliminado de la lista de deseos');
            fetchWishlist();
        } catch (error) {
            console.error('Error removing from wishlist:', error);
            addNotification('error', 'No se pudo eliminar el producto');
        }
    };

    const addToCartAndRemove = async (item) => {
        try {
            await api.post(getWishlistActionUrl(item, 'mover-al-carrito'));
            addNotification('success', 'Producto movido al carrito');
            fetchWishlist();
            
            // Dispatch a custom event to update cart counter in the header
            window.dispatchEvent(new Event('cart-updated'));
        } catch (error) {
            console.error('Error adding to cart:', error);
            addNotification('error', 'No se pudo mover al carrito');
        }
    };

    const visitStore = (item) => {
        const tenantUrl = getItemTenantUrl(item);
        if (!tenantUrl) {
            addNotification('error', 'No se pudo abrir la tienda');
            return;
        }
        window.location.href = `${tenantUrl}/catalogo`;
    };

    if (loading) {
        return <div className={styles.loading}>Cargando tu lista de deseos...</div>;
    }

    if (!wishlist || !wishlist.items || wishlist.items.length === 0) {
        return (
            <div className={`${styles.card} ${styles.emptyCard}`}>
                <div className={styles.emptyState}>
                    <Heart size={64} className={styles.emptyIcon} />
                    <h2>Tu lista de deseos está vacía</h2>
                    <p>Explora nuestro catálogo y guarda los productos que más te interesan para el futuro.</p>
                    <Button onClick={() => window.location.href = '/catalogo'}>Explorar catálogo</Button>
                </div>
            </div>
        );
    }

    return (
        <div className={styles.wishlistContainer}>
            <div className={styles.header}>
                <h1>Mi Lista de Deseos</h1>
                <p>Tienes {wishlist.items.length} productos guardados</p>
            </div>

            <div className={styles.grid}>
                {wishlist.items.map((item) => (
                    <div key={item.id} className={`${styles.card} ${styles.itemCard}`}>
                        <div className={styles.itemImage}>
                            {item.producto.imagen_url ? (
                                <img src={item.producto.imagen_url} alt={item.producto.nombre} />
                            ) : (
                                <div className={styles.noImage}>Sin Imagen</div>
                            )}
                        </div>
                        <div className={styles.itemInfo}>
                            <h3>{item.producto.nombre}</h3>
                            <div className={styles.price}>Bs. {parseFloat(item.producto.precio).toFixed(2)}</div>
                            
                            {item.tienda_nombre && (
                                <div style={{ fontSize: '0.85rem', color: '#666', marginBottom: '10px' }}>
                                    Tienda: {item.tienda_nombre}
                                </div>
                            )}

                            <div className={styles.actions} style={{ flexWrap: 'wrap' }}>
                                {!item.tienda_nombre && (
                                    <Button 
                                        variant="primary" 
                                        className={styles.cartBtn}
                                        onClick={() => addToCartAndRemove(item)}
                                        disabled={item.producto.stock <= 0}
                                        style={{ flex: 1, minWidth: '120px' }}
                                    >
                                        <ShoppingCart size={16} /> 
                                        {item.producto.stock <= 0 ? 'Agotado' : 'Mover al carrito'}
                                    </Button>
                                )}
                                
                                {item.tienda_nombre && (
                                    <Button 
                                        variant="outline" 
                                        onClick={() => visitStore(item)}
                                        title="Visitar Tienda"
                                    >
                                        Visitar
                                    </Button>
                                )}
                                
                                <Button 
                                    variant="danger" 
                                    className={styles.removeBtn}
                                    onClick={() => removeFromWishlist(item)}
                                    title="Eliminar de la lista"
                                >
                                    <Trash2 size={16} />
                                    Eliminar
                                </Button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default WishlistView;
