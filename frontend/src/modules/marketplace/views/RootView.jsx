import React from 'react';
import MarketplaceView from './MarketplaceView';
import CatalogoPublicoView from './CatalogoPublicoView';

/**
 * RootView - Detecta si estamos en subdomain o en main domain
 * Main domain (localhost) → Directorio de tiendas
 * Subdomain (cliente1.localhost) → Catálogo de tienda
 */
export default function RootView() {
  const hostname = window.location.hostname;
  const isSubdomain = hostname.split('.').length > 2 || 
                      (hostname.includes('.localhost') && !hostname.startsWith('localhost'));

  return isSubdomain ? <CatalogoPublicoView /> : <MarketplaceView />;
}
