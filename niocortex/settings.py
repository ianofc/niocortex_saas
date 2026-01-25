from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# Carrega variáveis de ambiente
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-chave-padrao-dev')

# Mantenha True para desenvolvimento
DEBUG = True

ALLOWED_HOSTS = ['*']

# ==============================================================================
# SEGURANÇA E CSRF (CORREÇÃO DO ERRO 403)
# ==============================================================================
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

# Em desenvolvimento (HTTP), isso deve ser False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# ==============================================================================
# APLICAÇÕES INSTALADAS
# ==============================================================================
INSTALLED_APPS = [
    'daphne',  # <--- OBRIGATÓRIO: Deve ser o primeiro para ASGI/Channels funcionar bem
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Bibliotecas de Terceiros
    'channels',  # Para WebSockets (TalkIO)

    # Módulos do Projeto (Arquitetura Modular)
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
            BASE_DIR / 'templates-cortex',
            BASE_DIR / 'lumenios' / 'templates',
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

# Configuração ASGI para suportar WebSockets e HTTP assíncrono
ASGI_APPLICATION = 'niocortex.asgi.application'
WSGI_APPLICATION = 'niocortex.wsgi.application'

# ==============================================================================
# BANCO DE DADOS (SUPABASE / POSTGRESQL)
# ==============================================================================

# Tenta pegar do arquivo .env
database_url = os.getenv('DATABASE_URL')

# FALLBACK: Se o .env falhar, usa a URL direta (Modo de Segurança)
if not database_url:
    database_url = "postgresql://postgres:2511CorteXEduc@db.qnknyonohlorjfhzkkpz.supabase.co:5432/postgres"

if database_url and "postgres" in database_url:
    DATABASES = {
        'default': dj_database_url.parse(database_url)
    }
else:
    # Trava o sistema se não tiver Supabase configurado (Evita SQLite fantasma)
    raise Exception("❌ ERRO CRÍTICO: DATABASE_URL inválida! O sistema exige conexão com o Supabase.")

# ==============================================================================
# CANAIS E WEBSOCKETS (TALKIO)
# ==============================================================================
CHANNEL_LAYERS = {
    'default': {
        # 'InMemoryChannelLayer' é ótimo para desenvolvimento rápido.
        # Para produção, use 'channels_redis.core.RedisChannelLayer'
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# ==============================================================================
# AUTENTICAÇÃO E USUÁRIOS
# ==============================================================================
AUTH_USER_MODEL = 'core.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# URLs de Login/Logout
LOGIN_REDIRECT_URL = 'yourlife_social:home'
LOGOUT_REDIRECT_URL = 'yourlife_social:login'
LOGIN_URL = 'yourlife_social:login'

# ==============================================================================
# INTERNACIONALIZAÇÃO E ARQUIVOS ESTÁTICOS
# ==============================================================================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (Uploads de usuários)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações Extras
MERCADO_PAGO_ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN', '00000000-0000-0000-0000-000000000000')