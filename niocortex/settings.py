# niocortex/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# ----------------------------------------------------
# 1. CARREGAMENTO DE VARIÁVEIS DE AMBIENTE
# ----------------------------------------------------
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------
# 2. SEGURANÇA E DEBUG
# ----------------------------------------------------

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-change-in-prod')

# Nunca deixar True em produção sem os devidos cuidados
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# Importante para Webhooks (Ngrok) e Produção
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 
    'http://localhost:8000,https://*.ngrok-free.app,https://*.ngrok-free.dev'
).split(',')

# ----------------------------------------------------
# 3. INSTALLED APPS (MÓDULOS DO SISTEMA)
# ----------------------------------------------------

INSTALLED_APPS = [
    # Apps Padrão do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 🚨 NOSSOS APPS/SERVIÇOS
    'core.apps.CoreConfig',           # Autenticação, Tenancy, Base
    'lumenios.pedagogico', # Alunos, Turmas, Notas
    'finexio',                      # Contratos, Boletos, Mercado Pago
    'vionex',                      # Captação de Alunos, Funil
    'humaniox',                             # RH: Funcionários
    'cognios',                    # Secretaria
    'lumenios.plataforma',             # Documentos
]

# ----------------------------------------------------
# 4. MIDDLEWARE
# ----------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Servir estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'niocortex.urls'

# ----------------------------------------------------
# 5. TEMPLATES E FRONTEND
# ----------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'lumenios/templates'], # Pasta global de templates
        
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'niocortex.wsgi.application'

# ----------------------------------------------------
# 6. BANCO DE DADOS (PostgreSQL / Supabase)
# ----------------------------------------------------

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
        ssl_require=os.getenv('DB_SSL', 'False') == 'True'
    )
}

# ----------------------------------------------------
# 7. AUTENTICAÇÃO E MODELO DE USUÁRIO
# ----------------------------------------------------

AUTH_USER_MODEL = 'core.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# ----------------------------------------------------
# 8. INTERNACIONALIZAÇÃO (PT-BR)
# ----------------------------------------------------

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------
# 9. ARQUIVOS ESTÁTICOS E MÍDIA
# ----------------------------------------------------

STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / "static" ]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Configuração do Whitenoise para produção
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------------------------------------
# 10. INTEGRAÇÕES EXTERNAS (Pagamento & Email)
# ----------------------------------------------------

# Mercado Pago
MERCADO_PAGO_ACCESS_TOKEN = os.getenv('MERCADO_PAGO_ACCESS_TOKEN')

# E-mail (SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# Para teste local (imprime no terminal se não tiver SMTP configurado)
if DEBUG and not EMAIL_HOST_USER:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ----------------------------------------------------
# 11. CONFIGURAÇÕES GERAIS
# ----------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'core:login'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'core:login'