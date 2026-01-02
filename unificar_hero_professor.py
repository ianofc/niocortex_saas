import os
import re

# Definição da Nova Arquitetura: Marca -> Responsabilidade
# A "Responsabilidade" será o nome técnico do App Django
STRUCTURE = {
    'prioris': 'direcao',       # Estratégia
    'humanex': 'rh',            # Recursos Humanos
    'ledger':  'financeiro',    # Contabilidade/Finanças
    'hub':     'secretaria',    # Atendimento/Documentação
    'orbit':   'coordenacao',   # Logística Pedagógica
    'vionex':  'crm',           # Vendas
    'yourlife':'social',        # Rede Social
    'stage':   'publico',       # Site/Landing Pages
    'core':    'base'           # Funcionalidades Comuns
}

# Lumenios mantemos separado pois já tem estrutura própria (pedagogico/plataforma)
LUMENIOS_APPS = ['lumenios.pedagogico', 'lumenios.plataforma']

def create_folders():
    print(">>> 1. CRIANDO ESTRUTURA MARCA/RESPONSABILIDADE <<<")
    
    for brand, sub in STRUCTURE.items():
        # Caminho: Marca/Responsabilidade (ex: humanex/rh)
        base_path = os.path.join(brand, sub)
        
        # Garante que a pasta existe
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            os.makedirs(os.path.join(base_path, 'migrations'))
            os.makedirs(os.path.join(base_path, 'templates', sub)) # Namespace de template
            print(f"✨ Criado: {brand}/{sub}")

        # Cria __init__.py na Marca (para ser um pacote)
        with open(os.path.join(brand, '__init__.py'), 'w') as f: f.write("")
        
        # Cria __init__.py na Subpasta
        with open(os.path.join(base_path, '__init__.py'), 'w') as f: f.write("")

        # Cria apps.py (Configuração do App)
        app_config_name = f"{brand.capitalize()}{sub.capitalize()}Config"
        app_name = f"{brand}.{sub}"
        
        with open(os.path.join(base_path, 'apps.py'), 'w') as f:
            f.write(f"""from django.apps import AppConfig

class {app_config_name}(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{app_name}'
    label = '{brand}_{sub}'  # Label único para evitar conflitos
""")

        # Cria models.py básico
        if not os.path.exists(os.path.join(base_path, 'models.py')):
            with open(os.path.join(base_path, 'models.py'), 'w') as f:
                f.write("from django.db import models\n\n# Defina seus modelos aqui\n")

        # Cria urls.py básico
        if not os.path.exists(os.path.join(base_path, 'urls.py')):
            with open(os.path.join(base_path, 'urls.py'), 'w') as f:
                f.write(f"from django.urls import path\n\napp_name = '{app_name}'\n\nurlpatterns = []\n")

def update_settings():
    print("\n>>> 2. ATUALIZANDO SETTINGS.PY (INSTALLED_APPS) <<<")
    
    settings_path = os.path.join('niocortex', 'settings.py')
    if not os.path.exists(settings_path):
        print("❌ Erro: niocortex/settings.py não encontrado.")
        return

    # Gera a nova lista de apps
    new_apps_list = "INSTALLED_APPS = [\n"
    new_apps_list += "    'django.contrib.admin',\n"
    new_apps_list += "    'django.contrib.auth',\n"
    new_apps_list += "    'django.contrib.contenttypes',\n"
    new_apps_list += "    'django.contrib.sessions',\n"
    new_apps_list += "    'django.contrib.messages',\n"
    new_apps_list += "    'django.contrib.staticfiles',\n\n"
    new_apps_list += "    # --- MÓDULOS NIOCORTEX ---\n"
    
    for brand, sub in STRUCTURE.items():
        new_apps_list += f"    '{brand}.{sub}',\n"
        
    new_apps_list += "\n    # --- LUMENIOS (LMS) ---\n"
    for app in LUMENIOS_APPS:
        new_apps_list += f"    '{app}',\n"
        
    new_apps_list += "]"

    # Lê o arquivo atual
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Substitui o bloco INSTALLED_APPS usando Regex
    # Procura por INSTALLED_APPS = [ ... ] (multiline)
    pattern = r"INSTALLED_APPS\s*=\s*\[.*?\]"
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, new_apps_list, content, flags=re.DOTALL)
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ settings.py atualizado com a nova estrutura!")
    else:
        print("⚠️  Não consegui achar o bloco INSTALLED_APPS para substituir automaticamente.")
        print("   Por favor, copie e cole isso no seu settings.py:")
        print(new_apps_list)

def update_urls_root():
    print("\n>>> 3. ATUALIZANDO URLS.PY PRINCIPAL <<<")
    urls_path = os.path.join('niocortex', 'urls.py')
    
    new_urls = """
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rotas Organizadas por Marca
    path('direcao/', include('prioris.direcao.urls')),
    path('rh/', include('humanex.rh.urls')),
    path('financeiro/', include('ledger.financeiro.urls')),
    path('secretaria/', include('hub.secretaria.urls')),
    path('coordenacao/', include('orbit.coordenacao.urls')),
    path('crm/', include('vionex.crm.urls')),
    path('social/', include('yourlife.social.urls')),
    path('', include('stage.publico.urls')), # Home/Site
    path('core/', include('core.base.urls')),
    
    # Lumenios
    path('lumenios/', include('lumenios.pedagogico.urls')),
    path('plataforma/', include('lumenios.plataforma.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(new_urls)
    print("✅ urls.py atualizado!")

if __name__ == "__main__":
    create_folders()
    update_settings()
    update_urls_root()
    
    print("\n" + "="*50)
    print("ESTRUTURA RECRIADA COM SUCESSO!")
    print("Agora execute:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("="*50)