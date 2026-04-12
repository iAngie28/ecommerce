import axios from 'axios';
import { getApiUrl } from '../utils/domain';

// ========================================================================
// CONFIGURACIÓN DINÁMICA DE API BASEURL
// ========================================================================
const hostname = window.location.hostname;
const backendPort = process.env.REACT_APP_API_PORT || '8001';
const API_BASE_URL = getApiUrl(hostname, backendPort);

console.log(`API Base URL: ${API_BASE_URL}`);

// ========================================================================
// INSTANCIA PRINCIPAL DE AXIOS
// ========================================================================
const api = axios.create({
    baseURL: API_BASE_URL,
    withCredentials: true,
});

// ========================================================================
// INTERCEPTOR REQUEST: Inyectar Token JWT
// ========================================================================
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// ========================================================================
// INTERCEPTOR RESPONSE: Refresh automático en 401
// ========================================================================
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    });
    failedQueue = [];
};

const redirectToLogin = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_full_name');
    // Redirigir al login del dominio base
    const baseDomain = process.env.REACT_APP_BASE_DOMAIN || window.location.hostname;
    const port = window.location.port ? `:${window.location.port}` : '';
    const protocol = window.location.protocol;
    window.location.href = `${protocol}//${baseDomain}${port}/login`;
};

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Solo intentar refresh si es 401 y no es la propia llamada de refresh
        if (
            error.response?.status === 401 &&
            !originalRequest._retry &&
            !originalRequest.url?.includes('/token/refresh/')
        ) {
            if (isRefreshing) {
                // Encolar mientras se refresca
                return new Promise((resolve, reject) => {
                    failedQueue.push({ resolve, reject });
                }).then(token => {
                    originalRequest.headers.Authorization = `Bearer ${token}`;
                    return api(originalRequest);
                }).catch(err => Promise.reject(err));
            }

            originalRequest._retry = true;
            isRefreshing = true;

            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
                isRefreshing = false;
                redirectToLogin();
                return Promise.reject(error);
            }

            try {
                const res = await axios.post(`${API_BASE_URL}/token/refresh/`, {
                    refresh: refreshToken
                });
                const newToken = res.data.access;
                localStorage.setItem('access_token', newToken);

                api.defaults.headers.common.Authorization = `Bearer ${newToken}`;
                originalRequest.headers.Authorization = `Bearer ${newToken}`;

                processQueue(null, newToken);
                return api(originalRequest);
            } catch (refreshError) {
                processQueue(refreshError, null);
                redirectToLogin();
                return Promise.reject(refreshError);
            } finally {
                isRefreshing = false;
            }
        }

        return Promise.reject(error);
    }
);

export default api;
