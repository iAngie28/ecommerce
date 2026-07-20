import { useState, useCallback } from 'react';

// MOCK API - A reemplazar por instancia de Axios real cuando la BD de Django esté viva
const mockApi = {
    get: async (url) => {
        if (url.includes('/configuracion/')) {
            return { data: { PUNTOS_POR_BS: 0.1, VALOR_BS_POR_PUNTO: 0.05 } };
        }
        if (url.includes('/mi-cuenta/')) {
            return { 
                data: {
                    id: 1,
                    cliente_nombre: 'Usuario Demo',
                    saldo_actual: 450,
                    puntos_historicos: 1200,
                    fecha_actualizacion: new Date().toISOString(),
                    historial: [
                        { id: 101, tipo_operacion: 'ACUMULACION', monto_puntos: 150, referencia: 'Pedido #5021', fecha: new Date(Date.now() - 86400000).toISOString() },
                        { id: 102, tipo_operacion: 'CANJE', monto_puntos: -200, referencia: 'Canje en Pedido #5020', fecha: new Date(Date.now() - 172800000).toISOString() },
                        { id: 103, tipo_operacion: 'ACUMULACION', monto_puntos: 500, referencia: 'Pedido #4900', fecha: new Date(Date.now() - 259200000).toISOString() }
                    ]
                }
            };
        }
        return { data: [] };
    },
    post: async (url, data) => {
        if (url.includes('/canjear/')) {
            return {
                data: {
                    mensaje: 'Canje exitoso',
                    descuento_bs: data.puntos * 0.05,
                    cuenta: { saldo_actual: 450 - data.puntos } // Simulación rápida
                }
            };
        }
    }
};

export const useFidelizacion = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [cuenta, setCuenta] = useState(null);
    const [configuracion, setConfiguracion] = useState({ PUNTOS_POR_BS: 0.1, VALOR_BS_POR_PUNTO: 0.05 });

    const fetchCuenta = useCallback(async () => {
        setLoading(true);
        try {
            // const response = await api.get('/api/fidelizacion/mi-cuenta/');
            const response = await mockApi.get('/api/fidelizacion/mi-cuenta/');
            setCuenta(response.data);
            setError(null);
        } catch (err) {
            setError(err.message || 'Error al cargar la cuenta de puntos.');
        } finally {
            setLoading(false);
        }
    }, []);

    const fetchConfiguracion = useCallback(async () => {
        try {
            // const response = await api.get('/api/fidelizacion/configuracion/');
            const response = await mockApi.get('/api/fidelizacion/configuracion/');
            setConfiguracion(response.data);
        } catch (err) {
            console.error('Error cargando configuración:', err);
        }
    }, []);

    const canjearPuntos = async (puntosACanjear) => {
        setLoading(true);
        try {
            // const response = await api.post('/api/fidelizacion/canjear/', { puntos: puntosACanjear });
            const response = await mockApi.post('/api/fidelizacion/canjear/', { puntos: puntosACanjear });
            
            // Actualizamos la cuenta local optimísticamente si mock, o con la data del server
            if (response.data.cuenta) {
                setCuenta(prev => ({ ...prev, ...response.data.cuenta }));
            }
            
            return response.data; // { mensaje, descuento_bs, cuenta }
        } catch (err) {
            const errorMsg = err.response?.data?.detail || 'Error al canjear puntos';
            setError(errorMsg);
            throw new Error(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    return {
        cuenta,
        configuracion,
        loading,
        error,
        fetchCuenta,
        fetchConfiguracion,
        canjearPuntos
    };
};

export default useFidelizacion;
