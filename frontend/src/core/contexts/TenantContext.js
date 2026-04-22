import React, { createContext, useContext } from 'react';

export const TenantContext = createContext(null);

export const TenantProvider = ({ children }) => {
  const hostname = window.location.hostname;
  // extrae el subdominio → 'cliente1.localhost' => 'cliente1'
  //                      → 'localhost' => 'localhost'
  const parts  = hostname.split('.');
  const tenant = parts.length > 1 && parts[0] !== 'www' ? parts[0] : 'público';

  return (
    <TenantContext.Provider value={tenant}>
      {children}
    </TenantContext.Provider>
  );
};

export const useTenantContext = () => useContext(TenantContext);
