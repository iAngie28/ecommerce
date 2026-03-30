import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8dl7kzt3gurd5j=)2(7=6kkf-vfp(5qq=46*8(w)g_)9q8*t^*'
DEBUG = True

# 1. HOSTS CORRECTOS: Incluimos .localhost para que los tenants funcionen
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.localhost', '192.168.56.1', '*']

# 2. USUARIO GLOBAL ÚNICO
AUTH_USER_MODEL = 'customers.Usuario'

# 3. APPS MULTI-TENANT
SHARED_APPS = (
    'django_tenants',
    'customers',
    'rest_framework',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

TENANT_APPS = (
    'django.contrib.contenttypes',
    'app_negocio',
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

# 4. MIDDLEWARES
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 5. RUTAS Y ESQUEMAS (El parche anti-404)
ROOT_URLCONF = 'config.urls'
PUBLIC_SCHEMA_URLCONF = 'config.urls'  # <-- Obliga a Django a reconocer la ruta de productos

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 6. BASE DE DATOS
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'mi_saas_db',
        'USER': 'postgres',
        'PASSWORD': 'adm123',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
DATABASE_ROUTERS = ('django_tenants.routers.TenantSyncRouter',)

# 7. MODELOS DE TENANTS
TENANT_MODEL = 'customers.Client'
TENANT_DOMAIN_MODEL = 'customers.Domain'

# 8. VALIDACIONES E INTERNACIONALIZACIÓN
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'

# 9. CORS Y API (REST FRAMEWORK & JWT)
CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'TOKEN_OBTAIN_PAIR_SERIALIZER': 'customers.serializers.MyTokenObtainPairSerializer',
    'AUTH_HEADER_TYPES': ('Bearer',),
}