import os

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Arquivos de Backend para corrigir
URLS_PATH = os.path.join(BASE_DIR, 'lumenios', 'pedagogico', 'urls.py')
VIEWS_PATH = os.path.join(BASE_DIR, 'lumenios', 'pedagogico', 'views.py')

# Pastas de Templates para varrer e corrigir
TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'lumenios', 'templates'),
    os.path.join(BASE_DIR, 'templates'),
]

# Substituições de Namespace (Errado -> Certo)
REPLACEMENTS = {
    "'pedagogical:": "'pedagogico:",
    '"pedagogical:': '"pedagogico:',
    "'pedagógico:": "'pedagogico:",
    '"pedagógico:': '"pedagogico:',
    "core:professor_dashboard": "lumenios:dashboard_professor", # Aponta para o dashboard certo
}

# ==============================================================================
# 1. CORRIGIR BACKEND (VIEWS E URLS)
# ==============================================================================
def fix_backend():
    print("🔧 Corrigindo Backend (Views e URLs)...")

    # 1. Adicionar Views Faltantes
    with open(VIEWS_PATH, 'r', encoding='utf-8') as f:
        content_views = f.read()
    
    new_views = ""
    if "def form_turmas" not in content_views:
        new_views += "\n@login_required\ndef form_turmas(request):\n    return render(request, 'pedagogico/turmas/form_turmas.html')\n"
    
    if "def gerador_planejamentos" not in content_views:
        new_views += "\n@login_required\ndef gerador_planejamentos(request):\n    return render(request, 'pedagogico/ferramentas/gerador_planejamentos.html')\n"

    if new_views:
        with open(VIEWS_PATH, 'a', encoding='utf-8') as f:
            f.write(new_views)
        print("   ✅ Views 'form_turmas' e 'gerador_planejamentos' adicionadas.")
    else:
        print("   ℹ️  Views já existem.")

    # 2. Adicionar URLs Faltantes
    with open(URLS_PATH, 'r', encoding='utf-8') as f:
        content_urls = f.read()
    
    # Reconstrói o urls.py para garantir que está limpo e completo
    new_urls_content = """from django.urls import path
from . import views

app_name = 'pedagogico'

urlpatterns = [
    # Alunos
    path('alunos/', views.listar_alunos, name='listar_alunos'),
    path('alunos/novo/', views.form_alunos, name='novo_aluno'),
    
    # Turmas
    path('turmas/', views.listar_turmas, name='listar_turmas'),
    path('turmas/nova/', views.form_turmas, name='form_turmas'),  # ADICIONADO
    path('turmas/<int:turma_id>/', views.detalhar_turma, name='detalhar_turma'),
    
    # Ferramentas
    path('gradebook/', views.gradebook, name='gradebook'),
    path('ferramentas/atividades/', views.gerador_atividades, name='gerador_atividades'),
    path('ferramentas/provas/', views.gerador_provas, name='gerador_provas'),
    path('ferramentas/planejamento/', views.gerador_planejamentos, name='gerador_planejamentos'), # ADICIONADO
]
"""
    with open(URLS_PATH, 'w', encoding='utf-8') as f:
        f.write(new_urls_content)
    print("   ✅ urls.py reescrito com todas as rotas.")

# ==============================================================================
# 2. CORRIGIR TEMPLATES (HTML)
# ==============================================================================
def fix_templates():
    print("\n🧹 Varrendo templates para corrigir namespaces...")
    count = 0
    
    for template_dir in TEMPLATE_DIRS:
        if not os.path.exists(template_dir): continue
        
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if not file.endswith(".html"): continue
                
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original = content
                    for wrong, correct in REPLACEMENTS.items():
                        if wrong in content:
                            content = content.replace(wrong, correct)
                    
                    if content != original:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"   ✨ Corrigido: {os.path.relpath(file_path, BASE_DIR)}")
                        count += 1
                except Exception as e:
                    print(f"   ❌ Erro em {file}: {e}")

    print(f"   Total de arquivos corrigidos: {count}")

# ==============================================================================
# EXECUÇÃO
# ==============================================================================
if __name__ == "__main__":
    fix_backend()
    fix_templates()
    print("\n🚀 TUDO PRONTO! Tente acessar o dashboard agora.")