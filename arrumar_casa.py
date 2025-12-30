import os
import shutil

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pastas que devem ser "desativadas" na raiz para não conflitar com o Lumenios
CONFLITOS = ['professor', 'aluno', 'extras'] 

# ==============================================================================
# 1. CONTEÚDO DOS NOVOS ARQUIVOS (LUMENIOS)
# ==============================================================================

base_professor_html = """{% load static %}
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Lumenio Docente{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Outfit:wght@400;500;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: { extend: { fontFamily: { sans: ['Plus Jakarta Sans'], display: ['Outfit'] } } }
        }
    </script>
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; }
        .glass-nav { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(226, 232, 240, 0.8); }
    </style>
</head>
<body class="text-slate-600">
    <nav class="fixed top-0 z-50 w-full glass-nav h-[70px] flex items-center justify-between px-6">
        <div class="flex items-center gap-10">
            <a href="{% url 'lumenios:dashboard_professor' %}" class="flex items-center gap-2 group">
                <div class="flex items-center justify-center w-8 h-8 text-white transition rounded-lg bg-gradient-to-br from-indigo-600 to-purple-600 group-hover:scale-105">
                    <i class="fas fa-chalkboard-teacher"></i>
                </div>
                <span class="text-xl font-bold tracking-tight text-slate-800 font-display">Lumenio <span class="text-indigo-600">Pro</span></span>
            </a>
            <div class="hidden gap-6 md:flex">
                <a href="{% url 'lumenios:dashboard_professor' %}" class="text-sm font-bold text-slate-500 hover:text-indigo-600">Dashboard</a>
                <a href="#" class="text-sm font-bold text-slate-500 hover:text-indigo-600">Minhas Turmas</a>
                <a href="#" class="text-sm font-bold text-slate-500 hover:text-indigo-600">Banco de Questões</a>
            </div>
        </div>
        <div class="flex items-center gap-4">
            <a href="{% url 'lumenios:criar_curso' %}" class="flex items-center gap-2 px-4 py-2 text-xs font-bold text-white transition bg-indigo-600 rounded-full shadow-md hover:bg-indigo-700 shadow-indigo-200">
                <i class="fas fa-plus"></i> Novo Conteúdo
            </a>
            <div class="w-px h-6 bg-slate-200"></div>
            <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-700">{{ user.first_name }}</span>
                <div class="flex items-center justify-center w-8 h-8 text-indigo-600 bg-indigo-100 rounded-full"><i class="fas fa-user"></i></div>
            </div>
        </div>
    </nav>
    <main class="pt-24 pb-12 px-6 max-w-[1600px] mx-auto">
        {% block content %}{% endblock %}
    </main>
</body>
</html>"""

dashboard_professor_html = """{% extends 'professor/base_professor.html' %}
{% block content %}
<div class="space-y-8">
    <div class="flex flex-col gap-6 md:flex-row">
        <div class="flex-1 p-8 bg-white border border-slate-200 rounded-[2rem] shadow-sm relative overflow-hidden group">
            <div class="absolute top-0 right-0 w-64 h-64 -mt-10 -mr-10 rounded-full bg-indigo-50 blur-3xl"></div>
            <div class="relative z-10">
                <h1 class="text-3xl font-bold font-display text-slate-800">Olá, Prof. {{ user.last_name|default:user.username }} 👋</h1>
                <p class="max-w-md mt-2 text-slate-500">Bem-vindo ao seu ambiente de gestão pedagógica.</p>
            </div>
        </div>
        <div class="flex gap-4 md:w-1/3">
            <div class="flex-1 p-6 bg-white border border-slate-200 rounded-[2rem] shadow-sm flex flex-col justify-center items-center">
                <span class="text-3xl font-bold text-slate-800">{{ stats.alunos }}</span>
                <span class="text-xs font-bold uppercase text-slate-400">Alunos</span>
            </div>
            <div class="flex-1 p-6 bg-white border border-slate-200 rounded-[2rem] shadow-sm flex flex-col justify-center items-center">
                <span class="text-3xl font-bold text-slate-800">{{ stats.cursos }}</span>
                <span class="text-xs font-bold uppercase text-slate-400">Turmas</span>
            </div>
        </div>
    </div>

    <div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
        <div class="space-y-6 lg:col-span-2">
            <div class="flex items-end justify-between">
                <h3 class="text-xl font-bold text-slate-800">Minhas Turmas</h3>
                <a href="{% url 'lumenios:criar_curso' %}" class="text-sm font-bold text-indigo-600 hover:underline">Criar Nova</a>
            </div>
            <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
                {% for curso in cursos %}
                <div class="relative p-4 overflow-hidden transition bg-white border border-slate-200 rounded-2xl hover:shadow-md group">
                    <div class="absolute top-0 left-0 w-1 h-full bg-indigo-500"></div>
                    <div class="pl-4">
                        <span class="px-2 py-1 bg-indigo-50 text-indigo-700 text-[10px] font-bold uppercase rounded-md tracking-wider">{{ curso.categoria }}</span>
                        <h4 class="mt-2 mb-1 text-lg font-bold text-slate-800 line-clamp-1">{{ curso.titulo }}</h4>
                        <p class="mb-4 text-xs text-slate-500">{{ curso.modulos.count }} Módulos</p>
                        <a href="{% url 'lumenios:gerenciar_curso' curso.id %}" class="inline-flex items-center gap-2 text-xs font-bold text-indigo-600 hover:text-indigo-800">
                            Gerenciar Conteúdo <i class="fas fa-arrow-right"></i>
                        </a>
                    </div>
                </div>
                {% empty %}
                <div class="py-12 text-center border-2 border-dashed col-span-full border-slate-200 rounded-2xl">
                    <p class="font-medium text-slate-500">Nenhuma turma encontrada.</p>
                    <a href="{% url 'lumenios:criar_curso' %}" class="block mt-2 text-sm font-bold text-indigo-600">Criar primeira turma</a>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="space-y-6">
            <div class="bg-white border border-slate-200 rounded-[2rem] p-6 shadow-sm">
                <h4 class="mb-4 font-bold text-slate-800">Acesso Rápido</h4>
                <div class="space-y-2">
                    <a href="#" class="block p-3 text-sm font-bold transition rounded-xl bg-slate-50 hover:bg-indigo-50 text-slate-600 hover:text-indigo-600">📝 Corrigir Provas</a>
                    <a href="#" class="block p-3 text-sm font-bold transition rounded-xl bg-slate-50 hover:bg-indigo-50 text-slate-600 hover:text-indigo-600">📅 Diário de Classe</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

placeholder_html = """{% extends 'professor/base_professor.html' %}
{% block content %}
<div class="p-10 text-center">
    <h1 class="text-2xl font-bold text-slate-800">🚧 Em Construção</h1>
    <p class="text-slate-500">Funcionalidade do AVA Lumenios em desenvolvimento.</p>
    <a href="{% url 'lumenios:dashboard_professor' %}" class="inline-block mt-4 font-bold text-indigo-600 hover:underline">Voltar</a>
</div>
{% endblock %}"""

views_py = """from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Curso, Matricula, Conteudo
from .forms import CursoForm

# --- PROFESSOR (AVA) ---
@login_required
def dashboard_professor(request):
    cursos = Curso.objects.filter(professor=request.user)
    stats = {'alunos': Matricula.objects.filter(curso__in=cursos).count(), 'cursos': cursos.count()}
    return render(request, 'professor/dashboard.html', {'cursos': cursos, 'stats': stats})

@login_required
def gerenciar_curso(request, curso_id):
    try: curso = get_object_or_404(Curso, id=curso_id)
    except: return redirect('lumenios:dashboard_professor')
    return render(request, 'professor/gerenciar_curso.html', {'curso': curso})

@login_required
def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.professor = request.user
            curso.save()
            return redirect('lumenios:dashboard_professor')
    else: form = CursoForm()
    return render(request, 'professor/criar_conteudo.html', {'form': form})

@login_required
def editor_conteudo(request, curso_id):
    return render(request, 'professor/editor_conteudo.html', {'curso_id': curso_id})

# --- ALUNO (MANTIDO PARA NÃO QUEBRAR O SISTEMA) ---
@login_required
def dashboard_aluno(request):
    return render(request, 'aluno/dashboard.html', {'matriculas': Matricula.objects.filter(aluno=request.user)})
@login_required
def perfil_aluno(request): return render(request, 'aluno/dashboard.html')
@login_required
def disciplinas_aluno(request): return render(request, 'extras/disciplina.html', {'matriculas': Matricula.objects.filter(aluno=request.user)})
@login_required
def sala_de_aula(request, conteudo_id=None): return render(request, 'extras/sala_de_aula.html') # Simplificado para focar no prof
@login_required
def sala_de_aula_demo(request): return redirect('lumenios:dashboard_aluno')
@login_required
def biblioteca_aluno(request): return render(request, 'extras/biblioteca.html')
@login_required
def ensino_complementar(request): return render(request, 'extras/complementar.html')
@login_required
def avaliacoes_aluno(request): return render(request, 'extras/avaliacoes.html')
@login_required
def conscios_investigate(request): return render(request, 'extras/conscios.html')
@login_required
def desempenho_analytics(request): return render(request, 'aluno/desempenho.html')
"""

urls_py = """from django.urls import path
from . import views

app_name = 'lumenios'

urlpatterns = [
    # PROFESSOR
    path('professor/dashboard/', views.dashboard_professor, name='dashboard_professor'),
    path('professor/criar-curso/', views.criar_curso, name='criar_curso'),
    path('professor/curso/<int:curso_id>/', views.gerenciar_curso, name='gerenciar_curso'),
    path('professor/editor/<int:curso_id>/', views.editor_conteudo, name='editor_conteudo'),

    # ALUNO (Mantidos)
    path('aluno/home/', views.dashboard_aluno, name='dashboard_aluno'),
    path('aluno/perfil/', views.perfil_aluno, name='perfil_aluno'),
    path('aluno/disciplinas/', views.disciplinas_aluno, name='disciplinas'),
    path('aluno/aula/demo/', views.sala_de_aula_demo, name='sala_de_aula_demo'),
    path('aluno/aula/<int:conteudo_id>/', views.sala_de_aula, name='sala_de_aula'),
    path('aluno/biblioteca/', views.biblioteca_aluno, name='biblioteca'),
    path('aluno/complementar/', views.ensino_complementar, name='complementar'),
    path('aluno/avaliacoes/', views.avaliacoes_aluno, name='avaliacoes'),
    path('aluno/desempenho/', views.desempenho_analytics, name='desempenho'),
    path('aluno/conscios/', views.conscios_investigate, name='conscios'),
]"""

# ==============================================================================
# 2. FUNÇÕES DO SCRIPT
# ==============================================================================

def criar_arquivo(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ [CRIADO] {path}")

def resolver_conflitos():
    print("\n🧹 Verificando conflitos na pasta raiz 'templates'...")
    templates_root = os.path.join(BASE_DIR, 'templates')
    
    if not os.path.exists(templates_root):
        print("ℹ️ Pasta templates raiz não encontrada. Sem conflitos.")
        return

    for pasta in CONFLITOS:
        origem = os.path.join(templates_root, pasta)
        destino_backup = os.path.join(templates_root, f"{pasta}_BACKUP_LEGADO")
        
        if os.path.exists(origem):
            try:
                # Se o backup já existir, remove ele antes pra não dar erro
                if os.path.exists(destino_backup):
                    shutil.rmtree(destino_backup)
                
                os.rename(origem, destino_backup)
                print(f"⚠️ [RESOLVIDO] Pasta conflitante '{pasta}' movida para '{pasta}_BACKUP_LEGADO'")
            except Exception as e:
                print(f"❌ Erro ao mover {pasta}: {e}")
        else:
            print(f"✔️ Sem conflito para: {pasta}")

# ==============================================================================
# 3. EXECUÇÃO
# ==============================================================================

def main():
    print("🚀 Iniciando Organização do Ambiente LUMENIOS (AVA)...\n")
    
    # 1. Criar Arquivos Certos no Lumenios
    arquivos = {
        "lumenios/templates/professor/base_professor.html": base_professor_html,
        "lumenios/templates/professor/dashboard.html": dashboard_professor_html,
        "lumenios/templates/professor/criar_conteudo.html": placeholder_html,
        "lumenios/templates/professor/gerenciar_curso.html": placeholder_html,
        "lumenios/templates/professor/editor_conteudo.html": placeholder_html,
        "lumenios/plataforma/views.py": views_py,
        "lumenios/plataforma/urls.py": urls_py,
    }
    
    for path, content in arquivos.items():
        criar_arquivo(path, content)

    # 2. Desativar Conflitos na Raiz
    resolver_conflitos()

    print("\n✨ Tudo pronto! O ambiente do Professor está isolado em 'lumenios'.")
    print("👉 Acesse: http://127.0.0.1:8000/lumenios/professor/dashboard/")

if __name__ == "__main__":
    main()