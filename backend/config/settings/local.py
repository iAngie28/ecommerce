"""
config/settings/local.py
Configuración para desarrollo local y producción.
Extiende base.py con variables de entorno del .env central.
Reemplaza el antiguo config/settings_local.py
"""
import os
import re
import socket
from pathlib import Path
from decouple import config
from dotenv import load_dotenv

from .base import *  # noqa: F401,F403

# Forzar encoding UTF-8
os.environ['PGCLIENTENCODING'] = 'UTF-8'

BASE_DIR = Path(__file__).resolve().parent.parent.parent   # backend/
PROJECT_ROOT = BASE_DIR.parent                             # raíz del proyecto

# ── CARGAR .ENV ───────────────────────────────────────────────────────────────
ENV_FILE = PROJECT_ROOT / '.env'
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    raise FileNotFoundError(f"Archivo .env no encontrado en la raíz: {ENV_FILE}")

# ── ENTORNO ───────────────────────────────────────────────────────────────────
ENVIRONMENT = config('ENVIRONMENT', default='development')
DEBUG = config('DEBUG', default=True, cast=bool)

# ── DOMINIOS ──────────────────────────────────────────────────────────────────
DOMAIN_MAIN = config('DOMAIN_MAIN', default='localhost')

if DOMAIN_MAIN in ('localhost', '127.0.0.1'):
    TENANT_DOMAIN_SUFFIX = '.localhost'
else:
    TENANT_DOMAIN_SUFFIX = f".{DOMAIN_MAIN}.nip.io"

DEVICE_HOSTNAME = socket.gethostname()

if ENVIRONMENT == 'development':
    additional_hosts = config(
        'DOMAIN_ALLOWED_HOSTS',
        default='',
        cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
    )
    ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', DEVICE_HOSTNAME, '.localhost']
    ALLOWED_HOSTS.extend(additional_hosts)
    if TENANT_DOMAIN_SUFFIX not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(TENANT_DOMAIN_SUFFIX)

    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^http://.*\.localhost(:\d+)?$",
        r"^http://localhost(:\d+)?$",
        r"^http://.*" + re.escape(TENANT_DOMAIN_SUFFIX) + r"(:\d+)?$",
    ]
    CORS_ALLOW_HEADERS = [
        "accept", "accept-encoding", "authorization", "content-type",
        "dnt", "origin", "user-agent", "x-csrftoken", "x-requested-with",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost",
        "http://127.0.0.1",
        f"http://{DOMAIN_MAIN}",
        f"http://{DOMAIN_MAIN}:8001",
        f"http://*{TENANT_DOMAIN_SUFFIX}",
    ]

elif ENVIRONMENT == 'production':
    ALLOWED_HOSTS = ['*']
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^http://.*" + re.escape(TENANT_DOMAIN_SUFFIX) + r"$",
        r"^http://" + re.escape(DOMAIN_MAIN) + r"$",
    ]
    CSRF_TRUSTED_ORIGINS = [
        f"http://{DOMAIN_MAIN}",
        f"http://{DEVICE_HOSTNAME}",
        "http://*.nip.io",
        f"http://*{TENANT_DOMAIN_SUFFIX}",
    ]
    if f"http://{DOMAIN_MAIN}" not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(f"http://{DOMAIN_MAIN}")

# ── SECRET KEY ────────────────────────────────────────────────────────────────
SECRET_KEY = config(
    'DJANGO_SECRET_KEY',
    default='django-insecure-8dl7kzt3gurd5j=)2(7=6kkf-vfp(5qq=46*8(w)g_)9q8*t^*'
)

# ── BASE DE DATOS ─────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE', default='django_tenants.postgresql_backend'),
        'NAME': config('DATABASE_NAME', default='mi_saas_db'),
        'USER': config('DATABASE_USER', default='postgres'),
        'PASSWORD': config('DATABASE_PASSWORD', default='123456789'),
        'HOST': config('DATABASE_HOST', default='127.0.0.1'),
        'PORT': config('DATABASE_PORT', default='5432'),
    }
}

# ── JWT ───────────────────────────────────────────────────────────────────────
JWT_ALGORITHM = config('JWT_ALGORITHM', default='HS256')
JWT_EXPIRATION_MINUTES = config('JWT_EXPIRATION_MINUTES', default=1440, cast=int)
JWT_REFRESH_EXPIRATION_DAYS = config('JWT_REFRESH_EXPIRATION_DAYS', default=7, cast=int)

# ── CORREO ────────────────────────────────────────────────────────────────────
EMAIL_HOST_USER     = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_BACKEND   = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST      = 'smtp.gmail.com'
EMAIL_PORT      = 587
EMAIL_USE_TLS   = True
EMAIL_USE_SSL   = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ── ARCHIVOS ESTÁTICOS Y MEDIA ────────────────────────────────────────────────
STATIC_URL  = config('STATIC_URL', default='/static/')
STATIC_ROOT = config('STATIC_ROOT', default=str(BASE_DIR / 'staticfiles'))
MEDIA_URL   = config('MEDIA_URL', default='/media/')
MEDIA_ROOT  = config('MEDIA_ROOT', default=str(BASE_DIR / 'media'))

# ── SEGURIDAD ─────────────────────────────────────────────────────────────────
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
