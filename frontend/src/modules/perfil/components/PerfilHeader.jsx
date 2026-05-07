import { User, Link as LinkIcon, Copy } from 'lucide-react';
import './PerfilHeader.css';

export default function PerfilHeader({ perfil }) {
  const handleCopiarURL = () => {
    if (perfil?.tenant_info?.url) {
      navigator.clipboard.writeText(perfil.tenant_info.url);
      alert('URL copiada al portapapeles');
    }
  };

  return (
    <div className="perfil-header">
      <div className="perfil-foto-container">
        {perfil?.foto_perfil ? (
          <img src={perfil.foto_perfil} alt="Perfil" className="perfil-foto" />
        ) : (
          <div className="perfil-foto-placeholder">
            <User size={48} />
          </div>
        )}
      </div>

      <div className="perfil-info">
        <h1>{perfil?.first_name} {perfil?.last_name}</h1>
        <p className="email">{perfil?.email}</p>
        <span className="rol-badge">{perfil?.rol?.nombre || 'Vendedor'}</span>

        {/* Mostrar info del tenant solo si es admin */}
        {perfil?.tenant_info && (
          <div className="tenant-info">
            <h3>Información de tu Tienda</h3>
            <div className="tenant-details">
              <div className="tenant-item">
                <span className="label">Nombre:</span>
                <span className="value">{perfil.tenant_info.nombre_tienda}</span>
              </div>
              <div className="tenant-item">
                <span className="label">Schema:</span>
                <code>{perfil.tenant_info.schema}</code>
              </div>
              <div className="tenant-item">
                <span className="label">Dominio:</span>
                <span className="value">{perfil.tenant_info.dominio}</span>
              </div>
              {perfil.tenant_info.url && (
                <div className="tenant-item url-item">
                  <span className="label">
                    <LinkIcon size={16} />
                    Acceso
                  </span>
                  <div className="url-container">
                    <a 
                      href={perfil.tenant_info.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="tenant-link"
                    >
                      {perfil.tenant_info.url}
                    </a>
                    <button 
                      className="copy-btn"
                      onClick={handleCopiarURL}
                      title="Copiar URL"
                    >
                      <Copy size={16} />
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}