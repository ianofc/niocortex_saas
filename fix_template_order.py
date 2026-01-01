import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'lumenios', 'templates', 'professor', 'dashboard.html')

def fix_order():
    print(f"🔧 Corrigindo ordem das tags em: {TEMPLATE_PATH}")
    
    if not os.path.exists(TEMPLATE_PATH):
        print("❌ Arquivo não encontrado!")
        return

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    extends_line = ""
    load_lines = []
    other_lines = []

    # Separa as linhas importantes
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("{% extends"):
            extends_line = line
        elif stripped.startswith("{% load"):
            load_lines.append(line)
        else:
            other_lines.append(line)

    # Reconstrói na ordem certa: 1. extends, 2. loads, 3. resto
    if extends_line:
        new_lines.append(extends_line)
    
    for load in load_lines:
        new_lines.append(load)
        
    new_lines.extend(other_lines)

    # Salva o arquivo corrigido
    with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("✅ Ordem corrigida: {% extends %} agora é a primeira linha.")

if __name__ == "__main__":
    fix_order()
    print("\n🚀 Tente recarregar a página do Dashboard agora.")