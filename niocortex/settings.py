from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url # Biblioteca essencial para ler a URL do Supabase

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-chave-padrao-dev')

DEBUG = True

ALLOWED_HOSTS = ['*']

# ==============================================================================
# APLICAÇÕES INSTALADAS (ARQUITETURA MODULAR)
# ==============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'yourlife.social',
    'hub.secretaria',
    'humanex.rh',
    'ledger.financeiro',
    'lumenios.pedagogico',
    'lumenios.plataforma',
    'orbit.coordenacao',
    'prioris.direcao',
    'vionex.crm',
    'stage.publico',
    'talkio.chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'niocortex.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates-cortex', BASE_DIR / 'lumenios' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'core.context_processors.module_context',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'niocortex.wsgi.application'

# ==============================================================================
# BANCO DE DADOS (SUPABASE / POSTGRESQL)
# ==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Se existir DATABASE_URL no .env, usa ela (Supabase)
# Isso substitui o SQLite automaticamente
database_url = os.getenv('DATABASE_URL')
if database_url:
    DATABASES['default'] = dj_database_url.parse(database_url)

# User Model
AUTH_USER_MODEL = 'core.CustomUser'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Navegação
LOGIN_REDIRECT_URL = 'yourlife_social:home'
LOGOUT_REDIRECT_URL = 'yourlife_social:login' 
LOGIN_URL = 'yourlife_social:login'

MERCADO_PAGO_ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN', 'seu_token_aqui')

# CONFIGURAÇÃO DJANGO CHANNELS (TALKIO REAL-TIME)
INSTALLED_APPS.insert(0, 'daphne') # Daphne precisa ser o primeiro
INSTALLED_APPS += ['channels']
ASGI_APPLICATION = 'niocortex.asgi.application'

# Layer de Comunicação (Redis ou In-Memory para Dev)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}