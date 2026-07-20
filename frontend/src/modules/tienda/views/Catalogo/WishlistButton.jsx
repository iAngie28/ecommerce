import React, { useState, useEffect } from 'react';
import useWishlist from '../../hooks/useWishlist';
import './WishlistButton.css';

const WishlistButton = ({ productoId, className = '' }) => {
    const { verificarSiContiene, toggleProducto } = useWishlist();
    const [enWishlist, setEnWishlist] = useState(false);
    const [cargando, setCargando] = useState(true);

    useEffect(() => {
        let isMounted = true;
        
        const checkStatus = async () => {
            setCargando(true);
            const status = await verificarSiContiene(productoId);
            if (isMounted) {
                setEnWishlist(status);
                setCargando(false);
            }
        };

        if (productoId) {
            checkStatus();
        }

        return () => {
            isMounted = false;
        };
    }, [productoId, verificarSiContiene]);

    const handleClick = async (e) => {
        e.preventDefault(); // Por si está dentro de un Link al producto
        e.stopPropagation();
        
        if (cargando) return;
        
        // Optimistic update
        setEnWishlist(!enWishlist);
        
        try {
            await toggleProducto(productoId);
        } catch (error) {
            // Revert on failure
            setEnWishlist(!enWishlist);
        }
    };

    return (
        <button 
            className={`wishlist-button ${enWishlist ? 'active' : ''} ${className}`}
            onClick={handleClick}
            disabled={cargando}
            aria-label={enWishlist ? 'Quitar de lista de deseos' : 'Añadir a lista de deseos'}
            title={enWishlist ? 'Quitar de lista de deseos' : 'Añadir a lista de deseos'}
        >
            <svg 
                xmlns="http://www.w3.org/2000/svg" 
                viewBox="0 0 24 24" 
                fill={enWishlist ? "currentColor" : "none"} 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                className="heart-icon"
            >
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
        </button>
    );
};

export default WishlistButton;
