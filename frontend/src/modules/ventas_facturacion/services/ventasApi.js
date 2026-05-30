import api from 'core/services/api';

const BASE_PEDIDOS = '/pedidos';

export const ventasApi = {
  listarPedidos: (params) => api.get(BASE_PEDIDOS + '/', { params }),
  obtenerPedido: (id) => api.get(`${BASE_PEDIDOS}/${id}/`),
  cambiarEstado: (id, estado) => api.post(`${BASE_PEDIDOS}/${id}/cambiar-estado/`, { estado }),
};
