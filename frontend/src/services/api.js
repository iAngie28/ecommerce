import axios from 'axios';

const api = axios.create({
    // Configura la URL base usando el subdominio actual (ej: cliente1.localhost:8000)
    baseURL: `${window.location.protocol}//${window.location.hostname}:8000/api`
});

// Interceptor para pegar el token en cada llamada
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;