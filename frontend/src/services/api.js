import axios from 'axios';

// 1. Configuramos la URL base dinámica para que detecte el subdominio
const api = axios.create({
    baseURL: `${window.location.protocol}//${window.location.hostname}:8000/api`
});

// 2. Interceptor para inyectar el token guardado en cada petición
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;