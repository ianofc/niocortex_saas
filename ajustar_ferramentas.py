import os
import shutil

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos dos Arquivos
SRC_FILE = os.path.join(BASE_DIR, 'lumenios', 'templates', 'pedagogico', 'atividades', 'gerador_provas.html')
DST_DIR = os.path.join(BASE_DIR, 'lumenios', 'templates', 'pedagogico', 'ferramentas')
DST_FILE = os.path.join(DST_DIR, 'gerador_provas.html')

VIEWS_PATH = os.path.join(BASE_DIR, 'lumenios', 'pedagogico', 'views.py')
URLS_PATH = os.path.join(BASE_DIR, 'lumenios', 'pedagogico', 'urls.py')

# ==============================================================================
# FUNÇÕES
# ==============================================================================

def mover_template():
    print("📦 Movendo template...")
    
    # Verifica se o diretório de destino existe
    if not os.path.exists(DST_DIR):
        os.makedirs(DST_DIR)
        print(f"   Criado diretório: {DST_DIR}")

    # Verifica se o arquivo de origem existe
    if os.path.exists(SRC_FILE):
        shutil.move(SRC_FILE, DST_FILE)
        print(f"   ✅ Movido de 'atividades' para 'ferramentas/gerador_provas.html'")
        
        # Tenta remover a pasta antiga se estiver vazia
        old_dir = os.path.dirname(SRC_FILE)
        if not os.listdir(old_dir):
            os.rmdir(old_dir)
            print("   🗑️ Pasta 'atividades' removida (estava vazia).")
    elif os.path.exists(DST_FILE):
        print("   ℹ️ O arquivo já está no local correto.")
    else:
        # Se não existir em nenhum lugar, cria um placeholder para não dar erro
        with open(DST_FILE, 'w', encoding='utf-8') as f:
            f.write("<h1>Gerador de Provas</h1><p>Template movido com sucesso.</p>")
        print("   ⚠️ Arquivo de origem não encontrado. Criado placeholder em 'ferramentas'.")

def atualizar_views():
    print("\n🐍 Atualizando Views (lumenios/pedagogico/views.py)...")
    
    with open(VIEWS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Código da view correta
    view_code = """
@login_required
def gerador_provas(request):
    return render(request, 'pedagogico/ferramentas/gerador_provas.html')
"""

    if "def gerador_provas" in content:
        # Se já existe, verificamos se o template está certo
        if "pedagogico/atividades/gerador_provas.html" in content:
            content = content.replace("pedagogico/atividades/gerador_provas.html", "pedagogico/ferramentas/gerador_provas.html")
            print("   ✅ Caminho do template corrigido na view existente.")
        else:
            print("   ℹ️ View já parece estar correta.")
    else:
        # Se não existe, adiciona no final
        content += "\n" + view_code
        print("   ✅ View 'gerador_provas' adicionada.")

    with open(VIEWS_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

def atualizar_urls():
    print("\n🔗 Atualizando URLs (lumenios/pedagogico/urls.py)...")
    
    with open(URLS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    url_line = "    path('ferramentas/provas/', views.gerador_provas, name='gerador_provas'),"

    if "name='gerador_provas'" in content:
        print("   ℹ️ URL já configurada.")
    else:
        # Insere antes do fechamento da lista urlpatterns
        if "urlpatterns = [" in content:
            content = content.replace("]", url_line + "\n]")
            print("   ✅ URL 'ferramentas/provas/' adicionada.")
        else:
            print("   ❌ Não foi possível encontrar a lista urlpatterns.")

    with open(URLS_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

# ==============================================================================
# EXECUÇÃO
# ==============================================================================

if __name__ == "__main__":
    print("🚀 Ajustando Estrutura do Gerador de Provas...\n")
    mover_template()
    atualizar_views()
    atualizar_urls()
    print("\n✨ Concluído! Acesse: http://127.0.0.1:8000/lumenios/pedagogico/ferramentas/provas/")