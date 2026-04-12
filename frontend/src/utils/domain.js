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
 * Construye la URL base del API según el modo de ejecución.
 *
 * Modos:
 *  - localhost/desarrollo : http://localhost:8001/api
 *  - IP directa (red/VPS) : http://192.168.x.x:8001/api  (env actualizado por run_services.py)
 *  - Nginx producción    : /api  (relativo, Nginx hace el proxy)
 */
export const getApiUrl = (hostname, port = '8001') => {
    // 1. Usar la variable de entorno si está definida (actualizada por run_services.py al elegir modo)
    if (process.env.REACT_APP_API_URL) {
        return process.env.REACT_APP_API_URL;
    }

    // 2. Cualquier variante de localhost (incluyendo subdominios como tienda.localhost)
    if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname.endsWith('.localhost')) {
        return `http://localhost:${port}/api`;
    }

    // 3. Modo IP directa: usar REACT_APP_BASE_DOMAIN si está definido con una IP real
    const baseDomain = process.env.REACT_APP_BASE_DOMAIN;
    if (baseDomain && baseDomain !== 'localhost') {
        return `http://${baseDomain}:${port}/api`;
    }

    // 4. Producción con Nginx: ruta relativa (nginx hace el proxy al puerto interno)
    return '/api';
};
