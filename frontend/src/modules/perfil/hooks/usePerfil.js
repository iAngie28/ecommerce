import { useState, useEffect, useCallback } from 'react';
import { perfilService } from '../services/perfilService';

export const usePerfil = () => {
  const [perfil, setPerfil] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Cargar datos del perfil
  useEffect(() => {
    const cargarPerfil = async () => {
      try {
        setLoading(true);
        const datos = await perfilService.obtenerPerfil();
        setPerfil(datos);
      } catch (err) {
        setError(err.response?.data?.detail || 'Error al cargar perfil');
      } finally {
        setLoading(false);
      }
    };

    cargarPerfil();
  }, []);

  // Actualizar perfil
  const actualizar = useCallback(async (datos) => {
    try {
      const actualizado = await perfilService.actualizarPerfil(datos);
      setPerfil(actualizado);
      return { success: true };
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Error al actualizar';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    }
  }, []);

  return { perfil, loading, error, actualizar };
};
