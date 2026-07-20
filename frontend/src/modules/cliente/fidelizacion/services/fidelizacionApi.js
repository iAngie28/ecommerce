import api from 'core/services/api';

export const FIDELIZACION_CONFIG_DEFAULT = Object.freeze({
  PUNTOS_POR_BS: 0.1,
  VALOR_BS_POR_PUNTO: 0.05,
});

const toNumber = (value, fallback = 0) => {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
};

export const normalizeCuentaPuntos = (data = {}) => ({
  id: data.id ?? null,
  cliente_nombre: data.cliente_nombre ?? '',
  saldo_actual: toNumber(data.saldo_actual),
  puntos_historicos: toNumber(data.puntos_historicos, toNumber(data.saldo_actual)),
  fecha_actualizacion: data.fecha_actualizacion ?? null,
  historial: Array.isArray(data.historial) ? data.historial : [],
});

export const normalizeConfiguracion = (data = {}) => ({
  PUNTOS_POR_BS: toNumber(data.PUNTOS_POR_BS, FIDELIZACION_CONFIG_DEFAULT.PUNTOS_POR_BS),
  VALOR_BS_POR_PUNTO: toNumber(
    data.VALOR_BS_POR_PUNTO,
    FIDELIZACION_CONFIG_DEFAULT.VALOR_BS_POR_PUNTO
  ),
});

export const calcularDescuentoPorPuntos = (
  puntos,
  configuracion = FIDELIZACION_CONFIG_DEFAULT
) => {
  const valorPunto = toNumber(
    configuracion.VALOR_BS_POR_PUNTO,
    FIDELIZACION_CONFIG_DEFAULT.VALOR_BS_POR_PUNTO
  );
  return Math.max(0, toNumber(puntos)) * valorPunto;
};

export const calcularPuntosPorMonto = (
  monto,
  configuracion = FIDELIZACION_CONFIG_DEFAULT
) => {
  const puntosPorBs = toNumber(
    configuracion.PUNTOS_POR_BS,
    FIDELIZACION_CONFIG_DEFAULT.PUNTOS_POR_BS
  );
  return Math.floor(Math.max(0, toNumber(monto)) * puntosPorBs);
};

export const getFidelizacionErrorMessage = (
  error,
  fallback = 'No se pudo completar la operación de fidelización.'
) => (
  error?.response?.data?.detail ||
  error?.response?.data?.error ||
  error?.message ||
  fallback
);

export const fidelizacionApi = {
  async obtenerMiCuenta() {
    const response = await api.get('/fidelizacion/mi-cuenta/');
    return normalizeCuentaPuntos(response.data);
  },

  async obtenerConfiguracion() {
    const response = await api.get('/fidelizacion/configuracion/');
    return normalizeConfiguracion(response.data);
  },

  async canjearPuntos({ puntos, referencia }) {
    const response = await api.post('/fidelizacion/canjear/', {
      puntos,
      referencia,
    });

    return {
      ...response.data,
      descuento_bs: toNumber(response.data?.descuento_bs),
      cuenta: response.data?.cuenta
        ? normalizeCuentaPuntos(response.data.cuenta)
        : null,
    };
  },
};

export default fidelizacionApi;
