import api from 'core/services/api';

const marketplaceService = {
  getTiendas: async (params = {}) => {
    const response = await api.get('/tiendas-publicas/', {
      params: {
        page_size: params.page_size || 12,
        page: params.page || 1,
        search: params.search,
        categoria_tienda: params.categoria_tienda,
      },
    });
    return response.data;
  },
};

export default marketplaceService;
