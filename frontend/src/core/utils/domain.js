/**
 * Utilidades para manejo de dominios y subdominios en entornos Multi-Tenant (MiQhatu).
 */

/**
 * Obtiene el dominio raíz (IP o dominio base) de forma robusta.
 * Si estamos en tienda1.157.173.102.129.nip.io, debe devolver 157.173.102.129.nip.io
 */
export const getBaseDomain = (hostname) => {
  // 1. Prioridad absoluta a la variable de entorno
  if (process.env.REACT_APP_DOMAIN_MAIN && process.env.REACT_APP_DOMAIN_MAIN !== 'localhost') {
    return process.env.REACT_APP_DOMAIN_MAIN;
  }

  // 2. Manejo de IPs y localhost
  const isIp = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/.test(hostname);
  if (isIp || hostname === 'localhost' || hostname === '127.0.0.1' || hostname.endsWith('.localhost')) {
    return hostname.endsWith('.localhost') ? 'localhost' : hostname;
  }

  // 3. Lógica para nip.io (muy común en desarrollo/VPS)
  if (hostname.includes('nip.io')) {
    const parts = hostname.split('.');
    // El formato estándar es [subdominio].IP.nip.io
    // La base (IP.nip.io) siempre son las últimas 6 partes si es IPv4
    if (parts.length >= 6) {
      return parts.slice(-6).join('.');
    }
    return hostname;
  }

  // 4. Fallback genérico para dominios normales (ej: tienda.miqhatu.com -> miqhatu.com)
  const parts = hostname.split('.');
  if (parts.length > 2) {
    return parts.slice(-2).join('.');
  }

  return hostname;
};

/**
 * Construye la URL base del API según el modo de ejecución.
 */
export const getApiUrl = (hostname, port = '8001') => {
  const apiPort = process.env.REACT_APP_DJANGO_PORT || port;
  const protocol = window.location.protocol;
  // IMPORTANTE: El API siempre se consulta al hostname actual para que el 
  // middleware de Django detecte el Tenant correctamente.
  return `${protocol}//${hostname}:${apiPort}/api`;
};

/**
 * Determina si el hostname actual es el dominio principal (esquema public)
 */
export const isBaseDomain = (hostname) => {
    if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1') {
        return true;
    }
    if (hostname.endsWith('.localhost')) {
        return false;
    }
    return hostname === getBaseDomain(hostname);
};

/**
 * Obtiene la URL completa de una tienda (tenant) basándose en su subdominio o schema_name.
 * Soporta nip.io para IPs, subdominios para producción y localhost.
 */
export const getTenantUrl = (subdomainStr, currentProtocol = null, currentPort = null) => {
  const domainMain = process.env.REACT_APP_DOMAIN_MAIN || window.location.hostname;
  const protocol = currentProtocol || window.location.protocol;
  const port = currentPort || window.location.port;
  const portSuffix = port ? `:${port}` : '';

  const isIp = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/.test(domainMain);

  let suffix = '';
  if (domainMain === 'localhost' || domainMain === '127.0.0.1') {
      suffix = '.localhost';
  } else if (isIp || domainMain.includes('nip.io')) {
      const ip = isIp ? domainMain : getBaseDomain(domainMain);
      suffix = `.${ip}.nip.io`;
  } else {
      // Producción normal: tienda1.miqhatu.com
      suffix = `.${getBaseDomain(domainMain)}`;
  }

  return `${protocol}//${subdomainStr}${suffix}${portSuffix}`;
};
