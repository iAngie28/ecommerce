# ========================================================================
# CONFIGURACIÓN LOCAL DE SETTINGS.PY
# ========================================================================
# Este archivo mantiene la lógica de configuración dinámica basada en
# variables de entorno. Se importa en settings.py para mantener 
# las configuraciones separadas.
# ========================================================================

import os
import socket
from pathlib import Path
from decouple import config
from dotenv import load_dotenv

# Forzar encoding UTF-8 para evitar errores de decodificación en Windows con locales en español
os.environ['PGCLIENTENCODING'] = 'UTF-8'

# BASE_DIR es backend/, PROJECT_ROOT es el raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

# ========================================================================
# CARGAR .ENV DESDE LA RAÍZ DEL PROYECTO
# ========================================================================
ENV_FILE = PROJECT_ROOT / '.env'
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    # Error fatal si no existe el .env central
    raise FileNotFoundError(f"Archivo .env no encontrado en la raíz: {ENV_FILE}")

# ========================================================================
# 1. DETECTAR ENTORNO
# ========================================================================
ENVIRONMENT = config('ENVIRONMENT', default='development')
DEBUG = config('DEBUG', default=True, cast=bool)

# ========================================================================
# 2. CONFIGURACIÓN DE DOMINIOS (MUY IMPORTANTE)
# ========================================================================
DOMAIN_MAIN = config('DOMAIN_MAIN', default='localhost')

# Obtener hostname del dispositivo
DEVICE_HOSTNAME = socket.gethostname()

# Basado en el entorno, configurar ALLOWED_HOSTS
if ENVIRONMENT == 'development':
    # Leer hosts adicionales del .env
    additional_hosts = config(
        'DOMAIN_ALLOWED_HOSTS',
        default='',
        cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
    )
    
    # Construir lista de hosts permitidos
    ALLOWED_HOSTS = [
        '*',              # Permitir cualquier host en entorno de desarrollo
        'localhost',
        '127.0.0.1',
        DEVICE_HOSTNAME,  # Hostname del dispositivo (ej: DESKTOP-ABC123)
        '.localhost',     # ← Wildcard correcto para *.localhost (empresa1, empresa2, etc.)
    ]
    # Agregar hosts adicionales del .env
    ALLOWED_HOSTS.extend(additional_hosts)
    
    # En desarrollo permitimos todos los orígenes
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
    
    # No necesitamos CORS_ALLOWED_ORIGINS estricto ya que CORS_ALLOW_ALL_ORIGINS = True
    
elif ENVIRONMENT == 'production':
    ALLOWED_HOSTS = config(
        'DOMAIN_ALLOWED_HOSTS',
        default='localhost,.localhost',
        cast=lambda v: [s.strip() for s in v.split(',')]
    )
    # En producción, ser específico con CORS
    CORS_ALLOWED_ORIGINS = config(
        'CORS_ALLOWED_ORIGINS',
        default=f'https://{DOMAIN_MAIN},https://*.{DOMAIN_MAIN}',
        cast=lambda v: [s.strip() for s in v.split(',')]
    )
    CORS_ALLOW_ALL_ORIGINS = False

# ========================================================================
# 3. SECRET KEY (CAMBIAR EN PRODUCCIÓN)
# ========================================================================
SECRET_KEY = config(
    'DJANGO_SECRET_KEY',
    default='django-insecure-8dl7kzt3gurd5j=)2(7=6kkf-vfp(5qq=46*8(w)g_)9q8*t^*'
)

# ========================================================================
# 4. BASE DE DATOS
# ========================================================================
DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE', default='django_tenants.postgresql_backend'),
        'NAME': config('DATABASE_NAME', default='mi_saas_db'),
        'USER': config('DATABASE_USER', default='postgres'),
        'PASSWORD': config('DATABASE_PASSWORD', default='adm123'),
        'HOST': config('DATABASE_HOST', default='127.0.0.1'),
        'PORT': config('DATABASE_PORT', default='5432'),
        'OPTIONS': {
            'options': '-c lc_messages=en_US.UTF-8'
        }
    }
}

# ========================================================================
# 5. JWT TOKENS
# ========================================================================
JWT_ALGORITHM = config('JWT_ALGORITHM', default='HS256')
JWT_EXPIRATION_MINUTES = config('JWT_EXPIRATION_MINUTES', default=60, cast=int)

# ========================================================================
# 6. CONFIGURACIÓN DE CORREO
# ========================================================================
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# ========================================================================
# 7. ARCHIVOS ESTÁTICOS Y MEDIA
# ========================================================================
STATIC_URL = config('STATIC_URL', default='/static/')
STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(BASE_DIR, 'staticfiles'))

MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = config('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media'))

# ========================================================================
# 7. SECURITY EN PRODUCCIÓN
# ========================================================================
if ENVIRONMENT == 'production':
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
