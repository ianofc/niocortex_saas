import os

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pasta onde estão os templates com erro (Rede Social / Professor)
TARGET_DIR = os.path.join(BASE_DIR, 'templates', 'professor')

# Substituições a fazer (Errado -> Certo)
REPLACEMENTS = {
    "'pedagogical:": "'pedagogico:",
    '"pedagogical:': '"pedagogico:',
    "'pedagógico:": "'pedagogico:",
    '"pedagógico:': '"pedagogico:',
    
    # Caso haja links para o dashboard antigo
    "'dashboard_professor'": "'lumenios:dashboard_professor'",
    
    # Correção de typo CSS que vi no seu log
    "round-lg": "rounded-lg" 
}

def corrigir_templates():
    print(f"🔧 Iniciando correção de namespaces em: {TARGET_DIR}")
    
    files_fixed = 0
    
    if not os.path.exists(TARGET_DIR):
        print(f"❌ Pasta não encontrada: {TARGET_DIR}")
        return

    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if not file.endswith(".html"):
                continue
                
            path = os.path.join(root, file)
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                for wrong, correct in REPLACEMENTS.items():
                    if wrong in content:
                        content = content.replace(wrong, correct)
                
                if content != original_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"   ✅ Corrigido: {file}")
                    files_fixed += 1
                    
            except Exception as e:
                print(f"   ❌ Erro ao ler {file}: {e}")

    print(f"\n✨ Concluído! {files_fixed} arquivos foram atualizados.")
    print("👉 Tente recarregar a página do Dashboard agora.")

if __name__ == "__main__":
    corrigir_templates()