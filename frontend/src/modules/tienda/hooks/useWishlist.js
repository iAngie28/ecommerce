import { useState, useCallback } from 'react';
// import api from '../../../core/api'; // Suponiendo que hay una instancia de axios configurada

// MOCK API - A reemplazar cuando el backend esté encendido
const mockApi = {
    get: async (url) => {
        if (url.includes('/contiene/')) {
            return { data: { en_wishlist: Math.random() > 0.5 } };
        }
        return { data: { resultados: [] } };
    },
    post: async (url, data) => {
        if (url.includes('/toggle/')) {
            return { data: { accion: 'toggled' } };
        }
        if (url.includes('/mover-al-carrito/')) {
            return { data: { message: 'Movido exitosamente' } };
        }
        return { data: {} };
    },
    delete: async (url) => {
        return { data: { message: 'Eliminado exitosamente' } };
    }
};

export const useWishlist = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [wishlistItems, setWishlistItems] = useState([]);

    const fetchWishlist = useCallback(async () => {
        setLoading(true);
        try {
            // const response = await api.get('/api/wishlist/');
            const response = await mockApi.get('/api/wishlist/');
            setWishlistItems(response.data.resultados || []);
            setError(null);
        } catch (err) {
            setError(err.message || 'Error al cargar la wishlist');
        } finally {
            setLoading(false);
        }
    }, []);

    const toggleProducto = async (productoId) => {
        try {
            // const response = await api.post(`/api/wishlist/toggle/${productoId}/`);
            const response = await mockApi.post(`/api/wishlist/toggle/${productoId}/`);
            return response.data;
        } catch (err) {
            console.error('Error toggling wishlist item:', err);
            throw err;
        }
    };

    const verificarSiContiene = async (productoId) => {
        try {
            // const response = await api.get(`/api/wishlist/contiene/${productoId}/`);
            const response = await mockApi.get(`/api/wishlist/contiene/${productoId}/`);
            return response.data.en_wishlist;
        } catch (err) {
            console.error('Error checking wishlist:', err);
            return false;
        }
    };

    const moverAlCarrito = async (productoId) => {
        setLoading(true);
        try {
            // const response = await api.post(`/api/wishlist/mover-al-carrito/${productoId}/`);
            const response = await mockApi.post(`/api/wishlist/mover-al-carrito/${productoId}/`);
            // Actualizar el estado local removiendo el item
            setWishlistItems(prev => prev.filter(item => item.producto.id !== productoId));
            return response.data;
        } catch (err) {
            setError(err.message || 'Error al mover al carrito');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const vaciarWishlist = async () => {
        setLoading(true);
        try {
            // await api.delete('/api/wishlist/vaciar/');
            await mockApi.delete('/api/wishlist/vaciar/');
            setWishlistItems([]);
        } catch (err) {
            setError(err.message || 'Error al vaciar la wishlist');
            throw err;
        } finally {
            setLoading(false);
        }
    };
    
    const eliminarProducto = async (productoId) => {
        try {
            // await api.delete(`/api/wishlist/eliminar/${productoId}/`);
            await mockApi.delete(`/api/wishlist/eliminar/${productoId}/`);
            setWishlistItems(prev => prev.filter(item => item.producto.id !== productoId));
        } catch (err) {
            console.error('Error al eliminar producto', err);
            throw err;
        }
    }

    return {
        wishlistItems,
        loading,
        error,
        fetchWishlist,
        toggleProducto,
        verificarSiContiene,
        moverAlCarrito,
        vaciarWishlist,
        eliminarProducto
    };
};

export default useWishlist;
