import os

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VIEWS_PATH = os.path.join(BASE_DIR, 'lumenios', 'pedagogico', 'views.py')
URLS_PATH = os.path.join(BASE_DIR, 'lumenios', 'pedagogico', 'urls.py')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'lumenios', 'templates', 'pedagogico', 'turmas', 'adicionar_aluno.html')

# ==============================================================================
# 1. CRIAR TEMPLATE (adicionar_aluno.html)
# ==============================================================================
html_content = """
{% extends 'layouts/base_app.html' %}

{% block title %}Adicionar Aluno | NioCortex{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto mt-10">
    <div class="overflow-hidden bg-white border border-gray-200 shadow-sm rounded-2xl">
        <div class="flex items-center justify-between p-6 border-b border-gray-100 bg-gray-50">
            <h2 class="text-xl font-bold text-gray-800">
                <i class="mr-2 text-indigo-600 fas fa-user-plus"></i> Adicionar Aluno
            </h2>
            <span class="text-sm font-medium text-gray-500">{{ turma.nome }}</span>
        </div>
        
        <form method="POST" class="p-6 space-y-6">
            {% csrf_token %}
            
            <div>
                <label class="block mb-2 text-sm font-bold text-gray-700">Nome Completo</label>
                <input type="text" name="nome" required 
                       class="w-full px-4 py-3 transition border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                       placeholder="Ex: João da Silva">
            </div>

            <div>
                <label class="block mb-2 text-sm font-bold text-gray-700">Matrícula (Opcional)</label>
                <input type="text" name="matricula" 
                       class="w-full px-4 py-3 transition border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                       placeholder="Ex: 2025001">
            </div>

            <div class="flex justify-end gap-3 pt-4">
                <a href="{% url 'pedagogico:detalhar_turma' turma.id %}" 
                   class="px-5 py-2.5 rounded-xl text-gray-600 font-bold hover:bg-gray-100 transition">
                    Cancelar
                </a>
                <button type="submit" 
                        class="px-6 py-2.5 rounded-xl bg-indigo-600 text-white font-bold hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition">
                    Salvar Aluno
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
"""

def create_template():
    print("📝 Criando template 'adicionar_aluno.html'...")
    os.makedirs(os.path.dirname(TEMPLATE_PATH), exist_ok=True)
    with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content.strip())
    print("   ✅ Template criado.")

# ==============================================================================
# 2. ATUALIZAR VIEWS (views.py)
# ==============================================================================
def update_views():
    print("🐍 Atualizando views.py...")
    with open(VIEWS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    if "def adicionar_aluno" not in content:
        new_view = """
@login_required
def adicionar_aluno(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        matricula = request.POST.get('matricula')
        
        if nome:
            Aluno.objects.create(
                nome=nome,
                matricula_id=matricula,
                turma=turma,
                tenant_id=turma.tenant_id
            )
            return redirect('pedagogico:detalhar_turma', turma_id=turma.id)
            
    return render(request, 'pedagogico/turmas/adicionar_aluno.html', {'turma': turma})
"""
        with open(VIEWS_PATH, 'a', encoding='utf-8') as f:
            f.write(new_view)
        print("   ✅ View 'adicionar_aluno' adicionada.")
    else:
        print("   ℹ️  View 'adicionar_aluno' já existe.")

# ==============================================================================
# 3. ATUALIZAR URLS (urls.py)
# ==============================================================================
def update_urls():
    print("🔗 Atualizando urls.py...")
    with open(URLS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    if "name='adicionar_aluno'" not in content:
        # Usa UUID porque corrigimos isso no passo anterior
        new_route = "    path('turmas/<uuid:turma_id>/adicionar-aluno/', views.adicionar_aluno, name='adicionar_aluno'),"
        
        content = content.replace("]", f"{new_route}\n]")
        
        with open(URLS_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print("   ✅ Rota 'adicionar_aluno' adicionada.")
    else:
        print("   ℹ️  Rota 'adicionar_aluno' já existe.")

# ==============================================================================
# EXECUÇÃO
# ==============================================================================
if __name__ == "__main__":
    create_template()
    update_views()
    update_urls()
    print("\n✨ Funcionalidade 'Adicionar Aluno' implementada! Tente recarregar a página.")