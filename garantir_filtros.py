import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Caminho para o app 'core'
TAGS_DIR = os.path.join(BASE_DIR, 'core', 'templatetags')
INIT_FILE = os.path.join(TAGS_DIR, '__init__.py')
FILTERS_FILE = os.path.join(TAGS_DIR, 'custom_filters.py')

def fix_filters():
    print(f"🔧 Configurando Filtros de Template em: {TAGS_DIR}")

    # 1. Cria a pasta se não existir
    if not os.path.exists(TAGS_DIR):
        os.makedirs(TAGS_DIR)
        print("   ✅ Pasta 'templatetags' criada.")

    # 2. Cria o __init__.py (Essencial para o Python reconhecer como pacote)
    with open(INIT_FILE, 'w') as f:
        pass # Arquivo vazio
    print("   ✅ Arquivo '__init__.py' verificado.")

    # 3. Escreve o código do filtro
    code = """from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary:
        return dictionary.get(key)
    return None
"""
    with open(FILTERS_FILE, 'w', encoding='utf-8') as f:
        f.write(code)
    print("   ✅ Arquivo 'custom_filters.py' gravado com sucesso.")

if __name__ == "__main__":
    fix_filters()
    print("\n" + "="*60)
    print("⚠️  AÇÃO NECESSÁRIA: REINICIAR SERVIDOR")
    print("="*60)
    print("O Django não reconhece novas pastas de tags sem reiniciar.")
    print("1. Vá no terminal onde o servidor está rodando.")
    print("2. Aperte 'Ctrl + C' para parar.")
    print("3. Rode novamente: python manage.py runserver")
    print("="*60)