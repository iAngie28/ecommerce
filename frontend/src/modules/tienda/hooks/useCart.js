import { useState, useEffect } from 'react';

export const useCart = () => {
    const [cart, setCart] = useState(() => {
        try {
            const saved = localStorage.getItem('miqhatu_cart');
            const parsed = saved ? JSON.parse(saved) : [];
            return Array.isArray(parsed) ? parsed : [];
        } catch (e) {
            return [];
        }
    });

    useEffect(() => {
        try {
            localStorage.setItem('miqhatu_cart', JSON.stringify(cart));
        } catch (e) {
            console.error("Error persistiendo el carrito:", e);
        }
    }, [cart]);

    const addToCart = (product) => {
        if (!product || !product.id) return;
        setCart(prev => {
            const exists = prev.find(item => item.id === product.id);
            if (exists) {
                if (exists.quantity >= product.stock) {
                    alert(`No puedes agregar más. El stock máximo es ${product.stock}.`);
                    return prev;
                }
                return prev.map(item => 
                    item.id === product.id 
                    ? { ...item, quantity: item.quantity + 1 } 
                    : item
                );
            }
            if (product.stock <= 0) {
                alert("Este producto está agotado.");
                return prev;
            }
            return [...prev, { ...product, quantity: 1 }];
        });
    };

    const removeFromCart = (id) => {
        setCart(prev => prev.filter(item => item.id !== id));
    };

    const updateQuantity = (id, delta) => {
        setCart(prev => prev.map(item => {
            if (item.id === id) {
                const newQty = Math.max(1, item.quantity + delta);
                if (newQty > item.stock) {
                    alert(`El stock máximo disponible es ${item.stock}.`);
                    return { ...item, quantity: item.stock };
                }
                return { ...item, quantity: newQty };
            }
            return item;
        }));
    };

    const clearCart = () => setCart([]);

    const total = cart.reduce((acc, item) => acc + (item.precio * item.quantity), 0);

    return {
        cart,
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
        total
    };
};
