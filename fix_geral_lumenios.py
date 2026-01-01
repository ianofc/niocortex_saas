import os

# ==============================================================================
# CONFIGURAÇÕES DO PROJETO
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, 'lumenios', 'pedagogico')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'lumenios', 'templates', 'pedagogico')

# ==============================================================================
# 1. ATUALIZAR VIEWS.PY (Adicionar Lógica CRUD Completa)
# ==============================================================================
def update_views():
    print("🐍 Injetando lógica completa no 'views.py'...")
    views_path = os.path.join(APP_DIR, 'views.py')
    
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Novas funções para adicionar
    new_code = """

# --- CRUD ALUNOS (Adicionado pelo Script Geral) ---

@login_required
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    if request.method == 'POST':
        aluno.nome = request.POST.get('nome')
        aluno.matricula_id = request.POST.get('matricula')
        # Adicione outros campos aqui conforme necessário
        aluno.save()
        return redirect('pedagogico:detalhar_turma', turma_id=aluno.turma.id)
    
    return render(request, 'pedagogico/alunos/editar_aluno.html', {'aluno': aluno})

@login_required
def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    turma_id = aluno.turma.id
    
    if request.method == 'POST':
        aluno.delete()
        return redirect('pedagogico:detalhar_turma', turma_id=turma_id)
        
    return render(request, 'pedagogico/alunos/confirmar_exclusao.html', {'obj': aluno, 'tipo': 'Aluno'})

# --- CRUD TURMAS (Complementar) ---

@login_required
def excluir_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == 'POST':
        turma.delete()
        return redirect('pedagogico:listar_turmas')
    return render(request, 'pedagogico/turmas/confirmar_exclusao.html', {'obj': turma, 'tipo': 'Turma'})

"""
    # Verifica o que falta e adiciona
    append_code = ""
    if "def editar_aluno" not in content: append_code += new_code
    
    if append_code:
        with open(views_path, 'a', encoding='utf-8') as f:
            f.write(append_code)
        print("   ✅ Views de Edição e Exclusão adicionadas.")
    else:
        print("   ℹ️  Views já parecem estar completas.")

# ==============================================================================
# 2. ATUALIZAR URLS.PY (Registrar Rotas UUID)
# ==============================================================================
def update_urls():
    print("\n🔗 Atualizando 'urls.py' com todas as rotas necessárias...")
    urls_path = os.path.join(APP_DIR, 'urls.py')
    
    with open(urls_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Rotas para garantir
    routes_to_add = [
        "    path('alunos/<uuid:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),",
        "    path('alunos/<uuid:aluno_id>/excluir/', views.excluir_aluno, name='excluir_aluno'),",
        "    path('turmas/<uuid:turma_id>/excluir/', views.excluir_turma, name='excluir_turma'),",
        # Garante que editar_turma esteja correto caso o script anterior não tenha rodado
        "    path('turmas/<uuid:turma_id>/editar/', views.editar_turma, name='editar_turma')," 
    ]
    
    new_routes_str = ""
    for route in routes_to_add:
        # Extrai o nome da rota para verificar se já existe
        route_name = route.split("name='")[1].split("'")[0]
        if route_name not in content:
            new_routes_str += route + "\n"
    
    if new_routes_str:
        # Insere antes do fechamento da lista urlpatterns
        content = content.replace("]", f"{new_routes_str}]")
        with open(urls_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ Rotas adicionadas:\n{new_routes_str}")
    else:
        print("   ℹ️  Todas as rotas já existem.")

# ==============================================================================
# 3. CRIAR TEMPLATES GENÉRICOS (Para não dar TemplateDoesNotExist)
# ==============================================================================
def create_templates():
    print("\n📝 Gerando templates que faltam...")
    
    # 3.1 Template de Edição de Aluno
    path_edit_aluno = os.path.join(TEMPLATES_DIR, 'alunos', 'editar_aluno.html')
    os.makedirs(os.path.dirname(path_edit_aluno), exist_ok=True)
    
    html_edit = """
{% extends 'layouts/base_app.html' %}
{% block title %}Editar Aluno{% endblock %}
{% block content %}
<div class="max-w-md p-6 mx-auto mt-10 bg-white border shadow-sm rounded-xl">
    <h2 class="mb-4 text-xl font-bold">Editar Aluno</h2>
    <form method="POST">
        {% csrf_token %}
        <label class="block mb-2 text-sm font-bold text-gray-700">Nome</label>
        <input type="text" name="nome" value="{{ aluno.nome }}" class="w-full p-2 mb-4 border rounded-lg">
        
        <label class="block mb-2 text-sm font-bold text-gray-700">Matrícula</label>
        <input type="text" name="matricula" value="{{ aluno.matricula_id|default:'' }}" class="w-full p-2 mb-6 border rounded-lg">
        
        <div class="flex justify-end gap-2">
            <a href="javascript:history.back()" class="px-4 py-2 text-gray-600">Cancelar</a>
            <button type="submit" class="px-4 py-2 font-bold text-white bg-blue-600 rounded-lg">Salvar</button>
        </div>
    </form>
</div>
{% endblock %}
"""
    if not os.path.exists(path_edit_aluno):
        with open(path_edit_aluno, 'w', encoding='utf-8') as f:
            f.write(html_edit.strip())
        print("   ✅ Template 'editar_aluno.html' criado.")

    # 3.2 Template Genérico de Confirmação de Exclusão (Serve para Aluno e Turma)
    # Criamos em 'alunos' e 'turmas' para garantir, ou um genérico.
    # Vamos criar específicos para evitar erro de caminho
    
    confirm_html = """
{% extends 'layouts/base_app.html' %}
{% block title %}Confirmar Exclusão{% endblock %}
{% block content %}
<div class="max-w-md p-6 mx-auto mt-10 bg-white border border-red-100 shadow-sm rounded-xl">
    <div class="text-center">
        <i class="mb-4 text-4xl text-red-500 fas fa-exclamation-triangle"></i>
        <h2 class="mb-2 text-xl font-bold text-gray-800">Excluir {{ tipo }}?</h2>
        <p class="mb-6 text-gray-600">Tem certeza que deseja remover <strong>"{{ obj.nome }}"</strong>? Esta ação não pode ser desfeita.</p>
        
        <form method="POST" class="flex justify-center gap-3">
            {% csrf_token %}
            <a href="javascript:history.back()" class="px-5 py-2 font-bold text-gray-700 bg-gray-100 rounded-lg">Cancelar</a>
            <button type="submit" class="px-5 py-2 font-bold text-white bg-red-600 rounded-lg hover:bg-red-700">Confirmar Exclusão</button>
        </form>
    </div>
</div>
{% endblock %}
"""
    # Salva para alunos
    path_del_aluno = os.path.join(TEMPLATES_DIR, 'alunos', 'confirmar_exclusao.html')
    if not os.path.exists(path_del_aluno):
        with open(path_del_aluno, 'w', encoding='utf-8') as f: f.write(confirm_html.strip())
        print("   ✅ Template exclusão alunos criado.")

    # Salva para turmas
    path_del_turma = os.path.join(TEMPLATES_DIR, 'turmas', 'confirmar_exclusao.html')
    if not os.path.exists(path_del_turma):
        with open(path_del_turma, 'w', encoding='utf-8') as f: f.write(confirm_html.strip())
        print("   ✅ Template exclusão turmas criado.")
        
    # 3.3 Template Editar Turma (Básico)
    path_edit_turma = os.path.join(TEMPLATES_DIR, 'turmas', 'editar.html')
    if not os.path.exists(path_edit_turma):
        with open(path_edit_turma, 'w', encoding='utf-8') as f:
            f.write(html_edit.replace('Aluno', 'Turma').replace('aluno.', 'turma.').strip())
        print("   ✅ Template edição turma criado.")

# ==============================================================================
# EXECUÇÃO
# ==============================================================================
if __name__ == "__main__":
    print("🚀 INICIANDO CORREÇÃO GERAL DO MÓDULO PEDAGÓGICO...\n")
    update_views()
    update_urls()
    create_templates()
    print("\n✨ PROCESSO CONCLUÍDO! O sistema deve estar estável agora.")
    print("👉 Atualize a página e teste os botões de editar e excluir.")