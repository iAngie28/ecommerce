import { useState, useEffect } from 'react';
import './PerfilForm.css';

export default function PerfilForm({ perfil, onGuardar, loading }) {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
  });

  useEffect(() => {
    if (perfil) {
      setFormData({
        first_name: perfil.first_name || '',
        last_name: perfil.last_name || '',
        email: perfil.email || '',
        password: '',
      });
    }
  }, [perfil]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const dataToSubmit = { ...formData };
    if (!dataToSubmit.password) {
      delete dataToSubmit.password;
    }
    onGuardar(dataToSubmit);
  };

  return (
    <form className="perfil-form" onSubmit={handleSubmit}>
      <div className="form-row">
        <div>
          <label htmlFor="first_name">Nombre</label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            placeholder="Tu nombre"
            disabled={loading}
          />
        </div>
        <div>
          <label htmlFor="last_name">Apellidos</label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            placeholder="Tus apellidos"
            disabled={loading}
          />
        </div>
      </div>

      <div>
        <label htmlFor="email">Correo Electrónico</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="tu@email.com"
          disabled={loading}
          autoComplete="username"
        />
      </div>

      <div>
        <label htmlFor="password">Nueva Contraseña (opcional)</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Dejar en blanco para no cambiar"
          disabled={loading}
          autoComplete="new-password"
        />
      </div>

      <div className="form-actions">
        <button type="submit" disabled={loading}>
          {loading ? 'Guardando...' : 'Guardar Cambios'}
        </button>
      </div>
    </form>
  );
}
