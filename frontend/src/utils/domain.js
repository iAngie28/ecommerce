/**
 * Utilidades para manejo de dominios y subdominios en entornos Multi-Tenant (MiQhatu).
 */

/**
 * Obtiene la IP base o el dominio raíz de forma robusta.
 */
export const getBaseDomain = (hostname) => {
    if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname.endsWith('.localhost')) {
        return process.env.REACT_APP_BASE_DOMAIN === 'localhost' || !process.env.REACT_APP_BASE_DOMAIN
            ? 'localhost'
            : process.env.REACT_APP_BASE_DOMAIN;
    }
    return process.env.REACT_APP_BASE_DOMAIN || hostname;
};

/**
 * Construye la URL base del API según el modo de ejecución asegurando
 * que el Host header enviado coincida con el tenant en el que estamos.
 */
export const getApiUrl = (hostname, port = '8001') => {
    // Si estamos en Nginx (producción real), usamos proxy inverso
    if (process.env.REACT_APP_API_URL === '/api') {
        return '/api';
    }

    // El servidor Django necesita el subdominio en la cabecera Host.
    // Si REACT_APP_API_URL tiene una IP hardcoreada (ej. http://192.168.1.1:8001/api),
    // django-tenants no sabrá qué tenant es y usará el schema "public" (0 productos).
    // Por eso SIEMPRE enviamos la petición al mismo `hostname` (subdominio nip.io incluido)
    // que la URL de la barra del navegador, apuntando al puerto del API.
    
    // Extraer el puerto original de REACT_APP_API_URL si existe, si no, usar fallback
    let apiPort = port;
    if (process.env.REACT_APP_API_URL) {
        const match = process.env.REACT_APP_API_URL.match(/:(\d+)\//);
        if (match) {
            apiPort = match[1]; // ej: '8001'
        }
    }

    const protocol = window.location.protocol;
    return `${protocol}//${hostname}:${apiPort}/api`;
};
