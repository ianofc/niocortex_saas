import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, 'lumenios', 'pedagogico')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'lumenios', 'templates', 'pedagogico')

# ==============================================================================
# 1. CRIAR FORMS.PY (Definição dos Formulários com Estilo)
# ==============================================================================
def create_forms():
    print("📝 Criando 'forms.py' com widgets estilizados...")
    forms_path = os.path.join(APP_DIR, 'forms.py')
    
    content = """
from django import forms
from .models import Turma, Aluno

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'ano_letivo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 text-gray-900 focus:ring-2 focus:ring-yellow-500 focus:border-transparent transition-all outline-none',
                'placeholder': 'Ex: 3º Ano A'
            }),
            'ano_letivo': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 text-gray-900 focus:ring-2 focus:ring-yellow-500 focus:border-transparent transition-all outline-none',
                'placeholder': '2025'
            }),
        }

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'matricula_id', 'email', 'telefone_responsavel']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none',
                'placeholder': 'Nome Completo'
            }),
            'matricula_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none',
                'placeholder': 'Matrícula (Opcional)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none',
                'placeholder': 'email@exemplo.com'
            }),
            'telefone_responsavel': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none',
                'placeholder': '(XX) 9XXXX-XXXX'
            }),
        }
"""
    with open(forms_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("   ✅ forms.py criado com sucesso.")

# ==============================================================================
# 2. ATUALIZAR VIEWS.PY (Usar os Forms Criados)
# ==============================================================================
def update_views():
    print("🐍 Atualizando 'views.py' para usar ModelForms...")
    views_path = os.path.join(APP_DIR, 'views.py')
    
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adiciona importação
    if "from .forms import" not in content:
        content = "from .forms import TurmaForm, AlunoForm\n" + content

    # Substitui a lógica de editar_turma
    new_editar_turma = """
@login_required
def editar_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return redirect('pedagogico:detalhar_turma', turma_id=turma.id)
    else:
        form = TurmaForm(instance=turma)
    
    return render(request, 'pedagogico/turmas/editar.html', {'form': form, 'turma': turma})
"""
    # Substitui ou adiciona
    if "def editar_turma" in content:
        # Modo preguiçoso: remove a função antiga manual e coloca a nova (regex seria melhor, mas aqui vai replace simples se o formato for conhecido)
        # Como é difícil substituir bloco exato, vamos anexar a versão correta no final e comentar que o python usa a última definição
        content += "\n" + new_editar_turma
    else:
        content += "\n" + new_editar_turma

    # Substitui a lógica de editar_aluno
    new_editar_aluno = """
@login_required
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('pedagogico:detalhar_turma', turma_id=aluno.turma.id)
    else:
        form = AlunoForm(instance=aluno)
    
    return render(request, 'pedagogico/alunos/editar_aluno.html', {'form': form, 'aluno': aluno})
"""
    content += "\n" + new_editar_aluno

    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("   ✅ Views atualizadas com lógica de formulário.")

# ==============================================================================
# 3. CORRIGIR TEMPLATES (Sintaxe Django)
# ==============================================================================
def fix_templates():
    print("html Corrigindo templates para sintaxe Django...")
    
    # 3.1 Editar Turma
    path_edit_turma = os.path.join(TEMPLATES_DIR, 'turmas', 'editar.html')
    html_turma = """
{% extends 'layouts/base_app.html' %}
{% block title %}Editar Turma{% endblock %}
{% block content %}
<div class="max-w-2xl mx-auto mt-10">
    <div class="p-8 bg-white border border-gray-100 shadow-lg rounded-2xl">
        <div class="mb-6">
            <h1 class="text-2xl font-bold text-gray-800">Editar Turma</h1>
            <p class="text-gray-500">Editando: {{ turma.nome }}</p>
        </div>

        <form method="POST" class="space-y-6">
            {% csrf_token %}
            
            {% for field in form %}
            <div>
                <label class="block mb-2 text-sm font-bold text-gray-700">{{ field.label }}</label>
                {{ field }}
                {% if field.errors %}
                    <p class="mt-1 text-xs text-red-500">{{ field.errors.0 }}</p>
                {% endif %}
            </div>
            {% endfor %}

            <div class="flex justify-end gap-3 pt-4">
                <a href="{% url 'pedagogico:detalhar_turma' turma.id %}" class="px-5 py-2.5 rounded-xl text-gray-600 font-bold hover:bg-gray-100">Cancelar</a>
                <button type="submit" class="px-6 py-2.5 rounded-xl bg-yellow-500 text-white font-bold hover:bg-yellow-600 shadow-lg">Salvar Alterações</button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
"""
    os.makedirs(os.path.dirname(path_edit_turma), exist_ok=True)
    with open(path_edit_turma, 'w', encoding='utf-8') as f:
        f.write(html_turma.strip())

    # 3.2 Editar Aluno
    path_edit_aluno = os.path.join(TEMPLATES_DIR, 'alunos', 'editar_aluno.html')
    html_aluno = """
{% extends 'layouts/base_app.html' %}
{% block title %}Editar Aluno{% endblock %}
{% block content %}
<div class="max-w-2xl mx-auto mt-10">
    <div class="p-8 bg-white border border-gray-100 shadow-lg rounded-2xl">
        <div class="mb-6">
            <h1 class="text-2xl font-bold text-gray-800">Editar Aluno</h1>
            <p class="text-gray-500">{{ aluno.nome }}</p>
        </div>

        <form method="POST" class="space-y-6">
            {% csrf_token %}
            
            {% for field in form %}
            <div>
                <label class="block mb-2 text-sm font-bold text-gray-700">{{ field.label }}</label>
                {{ field }}
                {% if field.errors %}
                    <p class="mt-1 text-xs text-red-500">{{ field.errors.0 }}</p>
                {% endif %}
            </div>
            {% endfor %}

            <div class="flex justify-end gap-3 pt-4">
                <a href="javascript:history.back()" class="px-5 py-2.5 rounded-xl text-gray-600 font-bold hover:bg-gray-100">Cancelar</a>
                <button type="submit" class="px-6 py-2.5 rounded-xl bg-indigo-600 text-white font-bold hover:bg-indigo-700 shadow-lg">Salvar Aluno</button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
"""
    os.makedirs(os.path.dirname(path_edit_aluno), exist_ok=True)
    with open(path_edit_aluno, 'w', encoding='utf-8') as f:
        f.write(html_aluno.strip())
        
    print("   ✅ Templates recriados com sintaxe correta.")

if __name__ == "__main__":
    print("🚀 INICIANDO CORREÇÃO DEFINITIVA (FORMS & TEMPLATES)...\n")
    create_forms()
    update_views()
    fix_templates()
    print("\n✨ TUDO PRONTO! Pode testar a edição de turmas e alunos.")