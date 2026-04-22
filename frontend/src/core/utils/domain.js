/**
 * Utilidades para manejo de dominios y subdominios en entornos Multi-Tenant (MiQhatu).
 * Migrado desde src/utils/domain.js → src/core/utils/domain.js
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

  // Extraer el puerto original de REACT_APP_API_URL si existe
  let apiPort = port;
  if (process.env.REACT_APP_API_URL) {
    const match = process.env.REACT_APP_API_URL.match(/:(\d+)\//);
    if (match) {
      apiPort = match[1];
    }
  }

  const protocol = window.location.protocol;
  return `${protocol}//${hostname}:${apiPort}/api`;
};
