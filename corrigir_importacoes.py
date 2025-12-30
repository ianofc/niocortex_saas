import os

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mapa de substituições (Antigo -> Novo)
REPLACEMENTS = {
    "from lumenios.pedagogico": "from lumenios.pedagogico",
    "import lumenios.pedagogico": "import lumenios.pedagogico",
    "app_name = 'pedagogico'": "app_name = 'pedagogico'",
    "path('lumenios/pedagogico/',": "path('lumenios/pedagogico/',",
}

# Extensões de arquivos a serem verificados
EXTENSIONS = ['.py', '.html']

# Pastas a ignorar (para não perder tempo ou alterar backups)
IGNORE_DIRS = [
    '__pycache__', 
    '.git', 
    '.venv', 
    'venv', 
    'pedagogical_BACKUP',
    'pedagogical_BACKUP_LEGADO'
]

# ==============================================================================
# EXECUÇÃO
# ==============================================================================

def corrigir_projeto():
    print("🚀 Iniciando varredura e correção de importações...\n")
    files_changed = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        # Remove pastas ignoradas da busca
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if not any(file.endswith(ext) for ext in EXTENSIONS):
                continue
                
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                changed = False
                
                for old, new in REPLACEMENTS.items():
                    if old in content:
                        content = content.replace(old, new)
                        changed = True
                        print(f"   🔧 Corrigindo '{old}' em: {os.path.relpath(file_path, BASE_DIR)}")
                
                if changed:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    files_changed += 1
                    
            except Exception as e:
                print(f"   ❌ Erro ao ler {file}: {e}")

    print(f"\n✅ Concluído! {files_changed} arquivos foram atualizados.")
    print("⚠️  Verifique se o servidor sobe normalmente agora.")

if __name__ == "__main__":
    corrigir_projeto()