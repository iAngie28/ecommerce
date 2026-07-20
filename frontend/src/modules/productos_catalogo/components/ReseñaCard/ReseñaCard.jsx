import React from 'react';
import StarRating from '../StarRating/StarRating';
import './ReseñaCard.css';

const ReseñaCard = ({ reseña }) => {
    // Formatear la fecha para que sea legible (ej. 15 de julio, 2026)
    const formatearFecha = (fechaStr) => {
        if (!fechaStr) return '';
        const fecha = new Date(fechaStr);
        return fecha.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    return (
        <div className="reseña-card">
            <div className="reseña-header">
                <div className="reseña-author-info">
                    <div className="reseña-avatar">
                        {reseña.cliente_nombre ? reseña.cliente_nombre.charAt(0).toUpperCase() : 'U'}
                    </div>
                    <div>
                        <h4 className="reseña-author">{reseña.cliente_nombre || 'Usuario Anónimo'}</h4>
                        <span className="reseña-date">{formatearFecha(reseña.fecha_creacion)}</span>
                    </div>
                </div>
                <div className="reseña-rating-badge">
                    <StarRating rating={reseña.calificacion} readOnly={true} />
                </div>
            </div>
            
            {reseña.comentario && (
                <div className="reseña-body">
                    <p className="reseña-comment">{reseña.comentario}</p>
                </div>
            )}
        </div>
    );
};

export default ReseñaCard;
