import React, { createContext } from 'react';

export const TenantContext = createContext();

export const TenantProvider = ({ children }) => {
    // Lee la URL (ej: cliente1.localhost)
    const hostname = window.location.hostname;
    // Separa el nombre antes del primer punto
    const tenant = hostname.split('.')[0]; 

    return (
        <TenantContext.Provider value={tenant}>
            {children}
        </TenantContext.Provider>
    );
};