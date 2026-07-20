import React, { useState, useEffect } from 'react';
import StarRating from '../../components/StarRating/StarRating';
import ReseñaCard from '../../components/ReseñaCard/ReseñaCard';
import './SeccionReseñas.css';

const SeccionReseñas = ({ productoId, usuarioAutenticado }) => {
    const [reseñas, setReseñas] = useState([]);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);
    
    // Estado del formulario
    const [nuevaCalificacion, setNuevaCalificacion] = useState(0);
    const [nuevoComentario, setNuevoComentario] = useState('');
    const [enviando, setEnviando] = useState(false);
    const [mensajeFormulario, setMensajeFormulario] = useState({ tipo: '', texto: '' });

    // Mock de carga de reseñas (hasta que el backend esté conectado)
    useEffect(() => {
        const fetchReseñas = async () => {
            setCargando(true);
            try {
                // TODO: Reemplazar por llamada real a la API: api.get(`/api/productos/${productoId}/reseñas/`)
                // Para efectos de UI, usamos un timeout mockeado
                setTimeout(() => {
                    setReseñas([
                        {
                            id: 1,
                            cliente_nombre: 'Ana García',
                            calificacion: 5,
                            comentario: '¡Excelente producto! Superó mis expectativas por completo. La calidad de los materiales es muy buena.',
                            fecha_creacion: '2026-06-15T10:30:00Z'
                        },
                        {
                            id: 2,
                            cliente_nombre: 'Carlos López',
                            calificacion: 4,
                            comentario: 'Buen producto en general, pero el envío tardó un poco más de lo esperado.',
                            fecha_creacion: '2026-07-02T14:15:00Z'
                        }
                    ]);
                    setCargando(false);
                }, 800);
            } catch (err) {
                setError('Hubo un problema al cargar las reseñas.');
                setCargando(false);
            }
        };

        if (productoId) {
            fetchReseñas();
        }
    }, [productoId]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (nuevaCalificacion === 0) {
            setMensajeFormulario({ tipo: 'error', texto: 'Por favor, selecciona una calificación.' });
            return;
        }

        setEnviando(true);
        setMensajeFormulario({ tipo: '', texto: '' });

        try {
            // TODO: Reemplazar por llamada real: api.post('/api/reseñas/', { producto_id: productoId, ... })
            setTimeout(() => {
                setMensajeFormulario({ 
                    tipo: 'exito', 
                    texto: '¡Gracias por tu reseña! Ha sido enviada y está pendiente de moderación.' 
                });
                setNuevaCalificacion(0);
                setNuevoComentario('');
                setEnviando(false);
            }, 1000);
        } catch (err) {
            setMensajeFormulario({ tipo: 'error', texto: 'Ocurrió un error al enviar tu reseña. Inténtalo de nuevo.' });
            setEnviando(false);
        }
    };

    // Calcular promedios (idealmente esto viene del backend)
    const promedio = reseñas.length > 0 
        ? (reseñas.reduce((acc, curr) => acc + curr.calificacion, 0) / reseñas.length).toFixed(1) 
        : 0;

    return (
        <div className="seccion-reseñas">
            <h3 className="reseñas-titulo">Reseñas de Clientes</h3>
            
            <div className="reseñas-resumen">
                <div className="resumen-promedio">
                    <span className="promedio-numero">{promedio}</span>
                    <StarRating rating={Math.round(promedio)} readOnly={true} />
                    <span className="total-opiniones">{reseñas.length} opinión{reseñas.length !== 1 ? 'es' : ''}</span>
                </div>
            </div>

            {/* Formulario de reseña (solo si está autenticado, idealmente validando si compró) */}
            {usuarioAutenticado ? (
                <div className="reseñas-formulario-box">
                    <h4>Escribe una reseña</h4>
                    {mensajeFormulario.texto && (
                        <div className={`mensaje-formulario ${mensajeFormulario.tipo}`}>
                            {mensajeFormulario.texto}
                        </div>
                    )}
                    <form onSubmit={handleSubmit} className="formulario-reseña">
                        <div className="form-group">
                            <label>Tu calificación:</label>
                            <StarRating 
                                rating={nuevaCalificacion} 
                                onRatingChange={setNuevaCalificacion} 
                            />
                        </div>
                        <div className="form-group">
                            <label>Tu comentario (opcional):</label>
                            <textarea 
                                value={nuevoComentario}
                                onChange={(e) => setNuevoComentario(e.target.value)}
                                placeholder="¿Qué te pareció este producto?"
                                rows="4"
                                maxLength="1000"
                            ></textarea>
                            <small>{nuevoComentario.length}/1000</small>
                        </div>
                        <button type="submit" className="btn-enviar-reseña" disabled={enviando}>
                            {enviando ? 'Enviando...' : 'Enviar Reseña'}
                        </button>
                    </form>
                </div>
            ) : (
                <div className="reseñas-login-prompt">
                    <p>Inicia sesión para compartir tu experiencia sobre este producto.</p>
                </div>
            )}

            {/* Lista de reseñas */}
            <div className="reseñas-lista">
                {cargando ? (
                    <p className="reseñas-loading">Cargando reseñas...</p>
                ) : error ? (
                    <p className="reseñas-error">{error}</p>
                ) : reseñas.length === 0 ? (
                    <p className="reseñas-vacias">Aún no hay reseñas para este producto. ¡Sé el primero!</p>
                ) : (
                    reseñas.map((reseña) => (
                        <ReseñaCard key={reseña.id} reseña={reseña} />
                    ))
                )}
            </div>
        </div>
    );
};

export default SeccionReseñas;
