import React, { useEffect } from 'react';
import useFidelizacion from '../hooks/useFidelizacion';
import './MiBilleteraPuntos.css';

const MiBilleteraPuntos = () => {
    const { 
        cuenta, 
        configuracion, 
        loading, 
        error, 
        fetchCuenta, 
        fetchConfiguracion 
    } = useFidelizacion();

    useEffect(() => {
        fetchConfiguracion();
        fetchCuenta();
    }, [fetchCuenta, fetchConfiguracion]);

    const formatDate = (dateString) => {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    if (loading && !cuenta) {
        return <div className="puntos-loading-container">Cargando tu billetera de puntos...</div>;
    }

    if (error && !cuenta) {
        return <div className="puntos-error-container">❌ {error}</div>;
    }

    return (
        <div className="billetera-puntos-container">
            <header className="billetera-header">
                <div className="header-icon">🏆</div>
                <div className="header-titles">
                    <h2>Programa de Fidelización</h2>
                    <p>Acumula puntos por tus compras y canjéalos por descuentos</p>
                </div>
            </header>

            <div className="billetera-grid">
                {/* Panel de Saldo */}
                <div className="panel-saldo-card">
                    <h3>Mi Saldo Actual</h3>
                    <div className="saldo-destacado">
                        <span className="saldo-valor">{cuenta?.saldo_actual || 0}</span>
                        <span className="saldo-unidad">pts</span>
                    </div>
                    <div className="saldo-equivalencia">
                        Equivale a <strong>${((cuenta?.saldo_actual || 0) * (configuracion.VALOR_BS_POR_PUNTO || 0)).toFixed(2)}</strong> de descuento en tu próxima compra.
                    </div>
                    
                    <div className="reglas-container">
                        <h4>¿Cómo funciona?</h4>
                        <ul>
                            <li>Ganas <strong>{configuracion.PUNTOS_POR_BS * 10} pts</strong> por cada $10 gastados.</li>
                            <li>Tus puntos se acreditan automáticamente cuando tu pedido es "ENTREGADO".</li>
                            <li>Canjéalos directamente en el Checkout antes de pagar.</li>
                        </ul>
                    </div>
                </div>

                {/* Panel de Historial */}
                <div className="panel-historial-card">
                    <h3>Historial de Movimientos</h3>
                    
                    {cuenta?.historial && cuenta.historial.length > 0 ? (
                        <ul className="historial-list">
                            {cuenta.historial.map(mov => (
                                <li key={mov.id} className="historial-item">
                                    <div className="mov-icon-container">
                                        {mov.tipo_operacion === 'ACUMULACION' ? (
                                            <span className="mov-icon gain">📈</span>
                                        ) : (
                                            <span className="mov-icon spend">🛍️</span>
                                        )}
                                    </div>
                                    <div className="mov-details">
                                        <div className="mov-title">
                                            {mov.tipo_operacion === 'ACUMULACION' ? 'Acumulación por Compra' : 'Canje por Descuento'}
                                        </div>
                                        <div className="mov-ref">{mov.referencia}</div>
                                        <div className="mov-date">{formatDate(mov.fecha)}</div>
                                    </div>
                                    <div className={`mov-amount ${mov.tipo_operacion === 'ACUMULACION' ? 'positive' : 'negative'}`}>
                                        {mov.tipo_operacion === 'ACUMULACION' ? '+' : ''}{mov.monto_puntos} pts
                                    </div>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <div className="historial-vacio">
                            <span className="icon-empty">📭</span>
                            <p>Aún no tienes movimientos.</p>
                            <p>¡Realiza tu primera compra para ganar puntos!</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default MiBilleteraPuntos;
