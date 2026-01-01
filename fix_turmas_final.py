import os

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VIEWS_PATH = os.path.join(BASE_DIR, 'lumenios', 'pedagogico', 'views.py')
URLS_PATH = os.path.join(BASE_DIR, 'lumenios', 'pedagogico', 'urls.py')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'lumenios', 'templates', 'pedagogico', 'turmas')

# ==============================================================================
# 1. CORRIGIR VIEWS.PY (Adicionar editar_turma)
# ==============================================================================
def fix_views():
    print("🐍 Atualizando views.py...")
    with open(VIEWS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    if "def editar_turma" not in content:
        new_view = """
@login_required
def editar_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    # Lógica de edição futura aqui
    return render(request, 'pedagogico/turmas/editar.html', {'turma': turma})
"""
        with open(VIEWS_PATH, 'a', encoding='utf-8') as f:
            f.write(new_view)
        print("   ✅ View 'editar_turma' adicionada.")
    else:
        print("   ℹ️  View 'editar_turma' já existe.")

# ==============================================================================
# 2. CORRIGIR URLS.PY (Adicionar rota editar_turma)
# ==============================================================================
def fix_urls():
    print("\n🔗 Atualizando urls.py...")
    with open(URLS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    if "name='editar_turma'" not in content:
        # Insere a nova rota antes da rota de detalhar
        new_route = "    path('turmas/editar/<int:turma_id>/', views.editar_turma, name='editar_turma'),"
        
        # Encontra um ponto de inserção seguro (ex: antes de detalhar_turma)
        if "name='detalhar_turma'" in content:
            content = content.replace(
                "path('turmas/<int:turma_id>/', views.detalhar_turma, name='detalhar_turma'),",
                f"{new_route}\n    path('turmas/<int:turma_id>/', views.detalhar_turma, name='detalhar_turma'),"
            )
        else:
            # Fallback: adiciona no final da lista
            content = content.replace("]", f"{new_route}\n]")

        with open(URLS_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print("   ✅ Rota 'editar_turma' adicionada.")
    else:
        print("   ℹ️  Rota 'editar_turma' já existe.")

# ==============================================================================
# 3. CORRIGIR TEMPLATE (detalhe_turma -> detalhar_turma)
# ==============================================================================
def fix_templates():
    print("\nhtml Corrigindo templates...")
    if not os.path.exists(TEMPLATE_DIR):
        print(f"❌ Pasta de templates não encontrada: {TEMPLATE_DIR}")
        return

    for filename in os.listdir(TEMPLATE_DIR):
        if not filename.endswith('.html'): continue
        
        filepath = os.path.join(TEMPLATE_DIR, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Corrige o nome da rota que costuma dar erro
        if "pedagogico:detalhe_turma" in content:
            content = content.replace("pedagogico:detalhe_turma", "pedagogico:detalhar_turma")
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ Corrigido 'detalhe_turma' em: {filename}")

# ==============================================================================
# EXECUÇÃO
# ==============================================================================
if __name__ == "__main__":
    fix_views()
    fix_urls()
    fix_templates()
    print("\n✨ Correções aplicadas! Tente recarregar a página.")