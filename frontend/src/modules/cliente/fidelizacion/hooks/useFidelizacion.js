import { useState, useCallback } from 'react';
import {
    FIDELIZACION_CONFIG_DEFAULT,
    calcularDescuentoPorPuntos,
    calcularPuntosPorMonto,
    fidelizacionApi,
    getFidelizacionErrorMessage,
} from '../services/fidelizacionApi';

export const useFidelizacion = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [cuenta, setCuenta] = useState(null);
    const [configuracion, setConfiguracion] = useState(FIDELIZACION_CONFIG_DEFAULT);

    const fetchCuenta = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await fidelizacionApi.obtenerMiCuenta();
            setCuenta(data);
            return data;
        } catch (err) {
            const message = getFidelizacionErrorMessage(err, 'Error al cargar la cuenta de puntos.');
            setError(message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const fetchConfiguracion = useCallback(async ({ silent = true } = {}) => {
        try {
            const data = await fidelizacionApi.obtenerConfiguracion();
            setConfiguracion(data);
            return data;
        } catch (err) {
            if (!silent) {
                setError(getFidelizacionErrorMessage(err, 'Error al cargar la configuración de puntos.'));
            }
            return FIDELIZACION_CONFIG_DEFAULT;
        }
    }, []);

    const canjearPuntos = useCallback(async (puntosACanjear, referencia = 'Canje desde la App') => {
        setLoading(true);
        setError(null);
        try {
            const data = await fidelizacionApi.canjearPuntos({
                puntos: puntosACanjear,
                referencia,
            });

            if (data.cuenta) {
                setCuenta(data.cuenta);
            }

            return data;
        } catch (err) {
            const errorMsg = getFidelizacionErrorMessage(err, 'Error al canjear puntos.');
            setError(errorMsg);
            throw new Error(errorMsg);
        } finally {
            setLoading(false);
        }
    }, []);

    return {
        cuenta,
        configuracion,
        loading,
        error,
        fetchCuenta,
        fetchConfiguracion,
        canjearPuntos,
        calcularDescuento: (puntos) => calcularDescuentoPorPuntos(puntos, configuracion),
        calcularPuntosGanados: (monto) => calcularPuntosPorMonto(monto, configuracion),
    };
};

export default useFidelizacion;
