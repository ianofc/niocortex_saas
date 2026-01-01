import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos dos arquivos a serem corrigidos
URLS_PATH = os.path.join(BASE_DIR, 'lumenios', 'pedagogico', 'urls.py')
VIEWS_PATH = os.path.join(BASE_DIR, 'lumenios', 'pedagogico', 'views.py')

def corrigir_urls():
    print("🔗 Adicionando rota em 'lumenios/pedagogico/urls.py'...")
    try:
        with open(URLS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se a rota já existe
        if "name='gerador_planejamentos'" in content:
            print("   ℹ️ Rota 'gerador_planejamentos' já existe.")
        else:
            # Adiciona a linha antes do fechamento da lista ]
            new_line = "    path('ferramentas/planejamento/', views.gerador_planejamentos, name='gerador_planejamentos'),"
            content = content.replace("]", f"{new_line}\n]")
            
            with open(URLS_PATH, 'w', encoding='utf-8') as f:
                f.write(content)
            print("   ✅ Rota adicionada com sucesso.")
            
    except Exception as e:
        print(f"   ❌ Erro ao editar urls.py: {e}")

def corrigir_views():
    print("\n🐍 Adicionando view em 'lumenios/pedagogico/views.py'...")
    try:
        with open(VIEWS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verifica se a view já existe
        if "def gerador_planejamentos" in content:
            print("   ℹ️ View 'gerador_planejamentos' já existe.")
        else:
            # Adiciona a função da view no final do arquivo
            new_view = """

@login_required
def gerador_planejamentos(request):
    return render(request, 'pedagogico/ferramentas/gerador_planejamentos.html')
"""
            with open(VIEWS_PATH, 'a', encoding='utf-8') as f: # Modo 'a' para append
                f.write(new_view)
            print("   ✅ View adicionada com sucesso.")

    except Exception as e:
        print(f"   ❌ Erro ao editar views.py: {e}")

if __name__ == "__main__":
    print("🚀 Corrigindo Erro de Rota 'gerador_planejamentos'...\n")
    corrigir_urls()
    corrigir_views()
    print("\n✨ Correção concluída! Tente recarregar a página do Dashboard.")