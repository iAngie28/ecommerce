import api from 'core/services/api';

const productosService = {
  getProductos: async (params = {}) => {
    const response = await api.get('/productos/', {
      params: {
        page_size: params.page_size || 50,
        page: params.page || 1,
      },
    });
    return response.data;
  },
};

export default productosService;
