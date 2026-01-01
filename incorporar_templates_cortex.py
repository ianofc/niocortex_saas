import os
import shutil
import re

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Origem (Onde estão seus templates soltos)
SOURCE_DIR = os.path.join(BASE_DIR, 'templates-cortex')

# Destino (Onde vamos instalar no Django)
# Focando em 'plataforma' pois você disse que Lumenios é o AVA
APP_NAME = 'plataforma' 
APP_PATH = os.path.join(BASE_DIR, 'lumenios', APP_NAME)
TEMPLATES_DEST = os.path.join(BASE_DIR, 'lumenios', 'templates', APP_NAME, 'importados')

# Arquivos de Backend
VIEWS_PATH = os.path.join(APP_PATH, 'views.py')
URLS_PATH = os.path.join(APP_PATH, 'urls.py')

def setup_directories():
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Erro: Pasta '{SOURCE_DIR}' não encontrada. Crie a pasta e coloque os HTMLs lá.")
        return False
    
    if not os.path.exists(TEMPLATES_DEST):
        os.makedirs(TEMPLATES_DEST)
        print(f"✅ Pasta de destino criada: {TEMPLATES_DEST}")
    
    return True

def clean_filename(filename):
    """Transforma 'Meus Cursos.html' em 'meus_cursos'"""
    name = os.path.splitext(filename)[0]
    name = name.lower().replace(' ', '_').replace('-', '_')
    # Remove caracteres especiais
    name = re.sub(r'[^a-z0-9_]', '', name)
    return name

def analyze_html(content):
    """Tenta adivinhar o que a página precisa baseado no HTML"""
    hints = []
    if '<form' in content:
        hints.append("POST Request (Formulário detectado)")
    if '<table' in content or 'grid' in content:
        hints.append("Listagem de dados (QuerySet necessário)")
    if 'id=' in content and ('user' in content or 'aluno' in content):
        hints.append("Pode precisar de autenticação ou ID específico")
    return hints

def djangoify_html(content, view_name):
    """Envolve o HTML cru no layout base do sistema se parecer uma página completa"""
    if '<html' in content or '<body' in content:
        # Remove tags estruturais básicas para injetar no bloco
        body_content = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        if body_content:
            inner_html = body_content.group(1)
        else:
            inner_html = content # Fallback
            
        return f"""
{{% extends 'layouts/base_app.html' %}}

{{% block title %}}{view_name.replace('_', ' ').title()} | Lumenios{{% endblock %}}

{{% block content %}}
{inner_html}
{{% endblock %}}
"""
    return content

def register_view(view_name, hints):
    """Adiciona a função no views.py se não existir"""
    with open(VIEWS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if f"def {view_name}" in content:
        print(f"   ℹ️  View '{view_name}' já existe. Pulando.")
        return

    hints_str = "\n    # ".join(hints) if hints else "Renderização simples"
    
    new_view = f"""

@login_required
def {view_name}(request):
    # TODO: Implementar lógica importada de templates-cortex
    # Sugestões baseadas no HTML:
    # {hints_str}
    return render(request, '{APP_NAME}/importados/{view_name}.html')
"""
    with open(VIEWS_PATH, 'a', encoding='utf-8') as f:
        f.write(new_view)
    print(f"   ✅ View '{view_name}' criada.")

def register_url(view_name):
    """Adiciona a rota no urls.py se não existir"""
    with open(URLS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if f"name='{view_name}'" in content:
        print(f"   ℹ️  URL '{view_name}' já existe. Pulando.")
        return

    # Procura onde inserir (antes do fechamento ])
    new_route = f"    path('importados/{view_name.replace('_', '-')}/', views.{view_name}, name='{view_name}'),"
    
    # Inserção segura
    if "urlpatterns = [" in content:
        content = content.replace("]", f"{new_route}\n]")
        with open(URLS_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ URL '{view_name}' registrada.")
    else:
        print(f"   ❌ Erro: Não encontrei 'urlpatterns' em {URLS_PATH}")

def process_files():
    print("🚀 INICIANDO INCORPORAÇÃO DE TEMPLATES (CORTEX -> LUMENIOS AVA)...\n")
    
    if not setup_directories(): return

    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.html')]
    
    if not files:
        print("⚠️  Nenhum arquivo .html encontrado em 'templates-cortex'.")
        return

    for filename in files:
        view_name = clean_filename(filename)
        src_path = os.path.join(SOURCE_DIR, filename)
        dest_path = os.path.join(TEMPLATES_DEST, f"{view_name}.html")
        
        print(f"\n📂 Processando: {filename} -> {view_name}")
        
        # 1. Ler e Analisar HTML
        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                raw_html = f.read()
            
            hints = analyze_html(raw_html)
            
            # 2. Converter para Template Django (Extends)
            django_html = djangoify_html(raw_html, view_name)
            
            # 3. Salvar no Destino
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(django_html)
            print("   ✅ Template convertido e movido.")
            
            # 4. Criar Backend
            register_view(view_name, hints)
            register_url(view_name)
            
        except Exception as e:
            print(f"   ❌ Erro ao processar {filename}: {e}")

if __name__ == "__main__":
    process_files()
    print("\n✨ FIM DA IMPORTAÇÃO!")
    print(f"👉 Os arquivos estão acessíveis em: /lumenios/{APP_NAME}/importados/NOME_DA_VIEW/")