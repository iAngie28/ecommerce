import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

export default function ResetPassword() {
  const { uid, token } = useParams();
  const navigate = useNavigate();
  const [newPassword, setNewPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (newPassword !== confirm) {
      setMessage("Las contraseñas no coinciden.");
      return;
    }
    try {
      await axios.post("http://localhost:8001/api/password-reset/confirm/", {
        uid,
        token,
        new_password: newPassword,
      });
      setMessage("¡Contraseña actualizada! Redirigiendo...");
      setTimeout(() => navigate("/login"), 2000);
    } catch {
      setMessage("Token inválido o expirado.");
    }
  };

  return (
    <div>
      <h2>Nueva contraseña</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          placeholder="Nueva contraseña"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Confirmar contraseña"
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
          required
        />
        <button type="submit">Cambiar contraseña</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}