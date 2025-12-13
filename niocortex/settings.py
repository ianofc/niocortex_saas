# niocortex_saas/niocortex/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv 
import dj_database_url 

# Carrega o .env na raiz do projeto
load_dotenv() 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------
# CONFIGURAÇÃO DE SEGURANÇA E DEBUG (AJUSTE CONFORME AMBIENTE)
# ----------------------------------------------------

SECRET_KEY = os.getenv('SECRET_KEY', 'your-fallback-secret-key-for-dev')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# ----------------------------------------------------
# INSTALLED APPS
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
    'core.apps.CoreConfig',          # Core: Autenticação, Tenancy (CRÍTICO)
    'pedagogical.apps.PedagogicalConfig', # Pedagógico: Turma, Aluno, Planos (DADOS)
    # Futuros: 'financial', 'crm_sales', etc.
]

# ----------------------------------------------------
# BANCO DE DADOS (PostgreSQL/Supabase)
# ----------------------------------------------------

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600 # Reutiliza conexões ativas
    )
}

# 🚨 CUSTOM USER MODEL (CRÍTICO)
# Diz ao Django para usar o modelo CustomUser do nosso app 'core'
AUTH_USER_MODEL = 'core.CustomUser'

# ----------------------------------------------------
# OUTRAS CONFIGURAÇÕES
# ----------------------------------------------------

# Templates (Jinja2 compatível)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Pasta templates global
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
# Adicione a pasta 'static' na raiz de cada app
STATICFILES_DIRS = [
    BASE_DIR / "static", 
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'