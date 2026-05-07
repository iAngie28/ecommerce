import { useState } from 'react';
import { AlertCircle, CheckCircle } from 'lucide-react';
import AppView from 'shared/widgets/AppView/AppView';
import PerfilHeader from '../components/PerfilHeader';
import PerfilForm from '../components/PerfilForm';
import { usePerfil } from '../hooks/usePerfil';
import './PerfilView.css';

export default function PerfilView() {
  const { perfil, loading, error, actualizar } = usePerfil();
  const [mensaje, setMensaje] = useState(null);

  const handleGuardarPerfil = async (datos) => {
    const resultado = await actualizar(datos);
    if (resultado.success) {
      setMensaje({ tipo: 'success', texto: 'Perfil actualizado correctamente' });
      setTimeout(() => setMensaje(null), 3000);
    } else {
      setMensaje({ tipo: 'error', texto: resultado.error });
    }
  };

  if (loading) return <AppView title="Perfil"><div>Cargando...</div></AppView>;

  return (
    <AppView title="Mi Perfil" subtitle="Gestiona tu información personal">
      {/* Mensaje de estado */}
      {mensaje && (
        <div className={`alert alert-${mensaje.tipo}`}>
          {mensaje.tipo === 'success' ? <CheckCircle size={20} /> : <AlertCircle size={20} />}
          <span>{mensaje.texto}</span>
        </div>
      )}

      {error && (
        <div className="alert alert-error">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Encabezado con foto */}
      {perfil && <PerfilHeader perfil={perfil} />}

      {/* Formulario de edición */}
      <div className="perfil-container">
        {perfil && (
          <PerfilForm
            perfil={perfil}
            onGuardar={handleGuardarPerfil}
            loading={loading}
          />
        )}
      </div>
    </AppView>
  );
}