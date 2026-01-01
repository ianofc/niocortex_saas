import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Definir onde o filtro vai morar (app 'core' é um bom lugar central)
TAGS_DIR = os.path.join(BASE_DIR, 'core', 'templatetags')
TAGS_FILE = os.path.join(TAGS_DIR, 'custom_filters.py')
INIT_FILE = os.path.join(TAGS_DIR, '__init__.py')

# 2. Conteúdo do Filtro
filter_code = """
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
"""

# 3. Caminho do Template que está falhando
TEMPLATE_PATH = os.path.join(BASE_DIR, 'lumenios', 'templates', 'professor', 'dashboard.html')

def create_filters():
    print("🔧 Criando filtros de template customizados...")
    
    if not os.path.exists(TAGS_DIR):
        os.makedirs(TAGS_DIR)
        print(f"   📂 Pasta criada: {TAGS_DIR}")
    
    # Cria __init__.py se não existir
    if not os.path.exists(INIT_FILE):
        with open(INIT_FILE, 'w') as f: pass
        
    # Cria o arquivo do filtro
    with open(TAGS_FILE, 'w', encoding='utf-8') as f:
        f.write(filter_code)
    print("   ✅ Filtro 'get_item' registrado em core/templatetags/custom_filters.py")

def update_template():
    print("📝 Atualizando template para carregar os filtros...")
    
    if not os.path.exists(TEMPLATE_PATH):
        print(f"   ❌ Erro: Template não encontrado em {TEMPLATE_PATH}")
        return

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verifica se já carrega
    if "{% load custom_filters %}" in content:
        print("   ℹ️  Template já carrega os filtros.")
        return

    # Adiciona o load logo após o extends ou no início
    if "{% extends" in content:
        # Insere na segunda linha
        lines = content.splitlines()
        lines.insert(1, "{% load custom_filters %}")
        new_content = "\n".join(lines)
    else:
        new_content = "{% load custom_filters %}\n" + content
        
    with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("   ✅ Template atualizado com {% load custom_filters %}")

if __name__ == "__main__":
    create_filters()
    update_template()
    print("\n🚀 Correção aplicada! O servidor deve reiniciar automaticamente.")
    print("   Se der erro, reinicie o servidor manualmente: python manage.py runserver")