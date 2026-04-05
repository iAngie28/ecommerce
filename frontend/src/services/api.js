import axios from 'axios';

// ========================================================================
// CONFIGURACIÓN DINÁMICA DE API BASEURL
// Lee desde .env (REACT_APP_API_URL) que es copiado desde la raíz
// ========================================================================

// Detectar dinámicamente el host del backend según el subdominio actual.
// Si estamos en empresa1.localhost:3000, la API es empresa1.localhost:8001
// Si estamos en localhost:3000 (login global), la API es localhost:8001
const hostname = window.location.hostname; // ej: empresa1.localhost
const backendPort = process.env.REACT_APP_API_PORT || '8001';
const API_BASE_URL = `http://${hostname}:${backendPort}/api`;

console.log(`API Base URL: ${API_BASE_URL}`);

// ========================================================================
// CREAR INSTANCIA DE AXIOS
// ========================================================================
const api = axios.create({
    baseURL: API_BASE_URL,
    withCredentials: true,
});

// ========================================================================
// INTERCEPTOR: Inyectar Token JWT en cada petición
// ========================================================================
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// ========================================================================
// INTERCEPTOR: Manejo de errores (especialmente 401)
// ========================================================================
api.interceptors.response.use(
    (response) => response,
    (error) => {
        // Si el token expiró (401), limpiar localStorage y redirigir a login
        if (error.response && error.response.status === 401) {
            console.warn('⚠️ Token expirado o inválido');
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            // Redirigir a login (ajusta según tu routing)
            // window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;
