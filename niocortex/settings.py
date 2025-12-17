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

    # 🚨 NOSSOS APPS/SERVIÇOS (Ordem de dependência importa)
    'core.apps.CoreConfig',             # Core: Autenticação, Tenancy, Base
    'pedagogical.apps.PedagogicalConfig', # Pedagógico: Alunos, Turmas, Notas
    'financial',                        # Financeiro: Contratos, Boletos, Compras, Patrimônio
    'crm_sales',                        # CRM: Captação de Alunos, Funil
    'hr',                               # RH: Funcionários, Departamentos, Cargos
    'secretariat',                      # Secretariado: Atendimento, Agendamentos, Documentos
]

# ----------------------------------------------------
# 4. MIDDLEWARE
# ----------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Recomendado para servir estáticos em produção
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
        'DIRS': [BASE_DIR / 'templates'], # Pasta global de templates
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
        default=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3'), # Fallback para SQLite se não houver URL
        conn_max_age=600,
        ssl_require=os.getenv('DB_SSL', 'False') == 'True' # Ajuste para True em Prod
    )
}

# ----------------------------------------------------
# 7. AUTENTICAÇÃO E MODELO DE USUÁRIO
# ----------------------------------------------------

AUTH_USER_MODEL = 'core.CustomUser'

# Validadores de senha padrão
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

# CSS, JavaScript, Images
STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / "static" ]
STATIC_ROOT = BASE_DIR / "staticfiles" # Onde o collectstatic junta os arquivos

# Uploads de Usuário (Fotos, Documentos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------------------------------------
# 10. CONFIGURAÇÕES ADICIONAIS
# ----------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração de Login
LOGIN_URL = 'core:login'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'core:login'