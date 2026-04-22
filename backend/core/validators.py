from core.exceptions import UsuarioNoActivoException

class AuthValidator:
    @staticmethod
    def validar_credenciales(email, password):
        """Valida que los campos no estén vacíos y tengan el formato básico."""
        if not email or not password:
            raise ValueError("Email/usuario y contraseña son requeridos.")
    
    @staticmethod
    def validar_usuario_activo(usuario):
        """Valida que el usuario no esté bloqueado."""
        if not usuario.is_active:
            raise UsuarioNoActivoException("Este usuario está inactivo.")