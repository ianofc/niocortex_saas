import os

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URLS_PATH = os.path.join(BASE_DIR, 'lumenios', 'pedagogico', 'urls.py')

def corrigir_urls_para_uuid():
    print(f"🔧 Corrigindo URLs em: {URLS_PATH}")
    
    if not os.path.exists(URLS_PATH):
        print("❌ Arquivo não encontrado!")
        return

    try:
        with open(URLS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # A Mágica: troca int por uuid
        new_content = content.replace('<int:turma_id>', '<uuid:turma_id>')
        
        # Caso haja outros IDs (como aluno_id) que também sejam UUIDs, adicione aqui se necessário
        new_content = new_content.replace('<int:aluno_id>', '<uuid:aluno_id>') 

        if content != new_content:
            with open(URLS_PATH, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✅ Sucesso! Rotas atualizadas de <int:> para <uuid:>.")
        else:
            print("ℹ️ O arquivo já parece estar usando UUID ou não encontrei padrões <int:>.")

    except Exception as e:
        print(f"❌ Erro ao editar o arquivo: {e}")

if __name__ == "__main__":
    corrigir_urls_para_uuid()
    print("\n🚀 Correção aplicada. Tente acessar a página de turmas novamente.")