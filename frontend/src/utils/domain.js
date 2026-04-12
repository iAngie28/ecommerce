/**
 * Utilidades para manejo de dominios y subdominios en entornos Multi-Tenant (MiQhatu).
 */

/**
 * Obtiene la IP base o el dominio raíz de forma robusta.
 * Ejemplo: gerlex.157.173.102.129.nip.io -> 157.173.102.129
 * Ejemplo: cliente.localhost -> localhost
 */
export const getBaseDomain = (hostname) => {
    if (!hostname) return 'localhost';
    
    // 1. Caso IP robusta (soporta nip.io y acceso directo)
    const ipMatch = hostname.match(/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/);
    if (ipMatch) {
        return ipMatch[0];
    }
    
    // 2. Caso Localhost
    if (hostname.endsWith('.localhost') || hostname === 'localhost') {
        return 'localhost';
    }
    
    // 3. Caso Dominio Real (ej: tienda.miqhatu.com)
    const parts = hostname.split('.');
    if (parts.length > 2) {
        // Retornamos los últimos dos segmentos (ej: miqhatu.com)
        return parts.slice(-2).join('.');
    }
    
    return hostname;
};

/**
 * Construye la URL base del API dinámicamente según el hostname.
 */
export const getApiUrl = (hostname, port = '8001') => {
    // Si estamos en localhost (desarrollo directo), usamos el puerto explícito
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return `http://${hostname}:${port}/api`;
    }
    
    // En producción (VPS), usamos rutas RELATIVAS.
    // Esto obliga al navegador a usar el mismo HOST y PUERTO (80) por el que entró,
    // permitiendo que Nginx intercepte el prefijo /api/ y lo redireccione internamente.
    return '/api';
};
