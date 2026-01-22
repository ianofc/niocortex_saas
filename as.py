import os

# Caminho do arquivo
file_path = os.path.join(os.getcwd(), 'yourlife', 'social', 'views', 'api.py')

def fix_imports():
    print(f"🔧 Reparando imports em {file_path}...")
    
    if not os.path.exists(file_path):
        print("❌ Arquivo não encontrado!")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Lista de imports necessários
    required_imports = [
        "from django.http import JsonResponse",
        "from django.views.decorators.csrf import csrf_exempt",
        "from django.views.decorators.http import require_POST",
        "import json",
        "from django.contrib.auth import get_user_model",
        "import random",
        "from datetime import date",
        "import time"
    ]

    # Verifica quais faltam
    missing_imports = []
    for imp in required_imports:
        if imp not in content:
            missing_imports.append(imp)

    if missing_imports:
        print("   ⚠️ Adicionando imports faltantes:")
        for imp in missing_imports:
            print(f"      + {imp}")
        
        # Adiciona os imports no topo do arquivo
        new_content = "\n".join(missing_imports) + "\n" + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("   ✅ Arquivo salvo com sucesso.")
    else:
        print("   ✅ Todos os imports já estavam presentes.")

if __name__ == "__main__":
    fix_imports()