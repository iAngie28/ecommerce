import api from 'core/services/api';

const BASE = '/bitacora';

export const bitacoraApi = {
  listar: (params) => api.get(BASE + '/', { params }),
};