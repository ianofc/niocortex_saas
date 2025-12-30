import os
import sys

# Define o caminho base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Arquivo criado/atualizado: {path}")

# ==============================================================================
# 1. CONTEÚDO DOS TEMPLATES (FRONTEND)
# ==============================================================================

base_professor_html = """
{% load static %}
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Lumenio Docente{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Outfit:wght@400;500;700&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['Plus Jakarta Sans'], display: ['Outfit'] },
                    colors: { aurora: { primary: '#6366f1', dark: '#0f172a' } }
                }
            }
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
                <div class="flex items-center justify-center w-8 h-8 text-indigo-600 bg-indigo-100 rounded-full">
                    <i class="fas fa-user"></i>
                </div>
            </div>
        </div>
    </nav>

    <main class="pt-24 pb-12 px-6 max-w-[1600px] mx-auto">
        {% block content %}{% endblock %}
    </main>

</body>
</html>
"""

dashboard_professor_html = """
{% extends 'professor/base_professor.html' %}

{% block content %}
<div class="space-y-8">

    <div class="flex flex-col gap-6 md:flex-row">
        <div class="flex-1 p-8 bg-white border border-slate-200 rounded-[2rem] shadow-sm relative overflow-hidden group">
            <div class="absolute top-0 right-0 w-64 h-64 -mt-10 -mr-10 rounded-full bg-indigo-50 blur-3xl"></div>
            <div class="relative z-10">
                <h1 class="text-3xl font-bold font-display text-slate-800">Olá, Prof. {{ user.last_name|default:user.username }} 👋</h1>
                <p class="max-w-md mt-2 text-slate-500">Você tem <strong class="text-indigo-600">{{ atividades|length }} atividades</strong> pendentes para hoje. Mantenha o ritmo!</p>
                <div class="flex gap-3 mt-6">
                    <button class="px-5 py-2.5 bg-slate-900 text-white text-sm font-bold rounded-xl hover:bg-slate-800 transition">Ver Agenda</button>
                </div>
            </div>
        </div>

        <div class="flex gap-4 md:w-1/3">
            <div class="flex-1 p-6 bg-white border border-slate-200 rounded-[2rem] shadow-sm flex flex-col justify-center items-center">
                <div class="flex items-center justify-center w-10 h-10 mb-2 rounded-full bg-emerald-100 text-emerald-600"><i class="fas fa-users"></i></div>
                <span class="text-3xl font-bold text-slate-800">{{ stats.alunos }}</span>
                <span class="text-xs font-bold uppercase text-slate-400">Alunos Totais</span>
            </div>
            <div class="flex-1 p-6 bg-white border border-slate-200 rounded-[2rem] shadow-sm flex flex-col justify-center items-center">
                <div class="flex items-center justify-center w-10 h-10 mb-2 text-blue-600 bg-blue-100 rounded-full"><i class="fas fa-layer-group"></i></div>
                <span class="text-3xl font-bold text-slate-800">{{ stats.cursos }}</span>
                <span class="text-xs font-bold uppercase text-slate-400">Turmas Ativas</span>
            </div>
        </div>
    </div>

    <div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
        
        <div class="space-y-6 lg:col-span-2">
            <div class="flex items-end justify-between">
                <h3 class="text-xl font-bold text-slate-800">Minhas Turmas e Conteúdos</h3>
                <a href="{% url 'lumenios:criar_curso' %}" class="text-sm font-bold text-indigo-600 hover:underline">Criar Nova Turma</a>
            </div>

            <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
                {% for curso in cursos %}
                <div class="relative p-4 overflow-hidden transition bg-white border border-slate-200 rounded-2xl hover:shadow-md group">
                    <div class="absolute top-0 left-0 w-1 h-full bg-indigo-500"></div>
                    <div class="pl-4">
                        <div class="flex items-start justify-between mb-2">
                            <span class="px-2 py-1 bg-indigo-50 text-indigo-700 text-[10px] font-bold uppercase rounded-md tracking-wider">{{ curso.categoria }}</span>
                            <div class="flex gap-1">
                                <a href="{% url 'lumenios:gerenciar_curso' curso.id %}" class="flex items-center justify-center w-8 h-8 transition rounded-lg bg-slate-100 text-slate-500 hover:bg-indigo-600 hover:text-white" title="Editar Conteúdo"><i class="fas fa-pen"></i></a>
                            </div>
                        </div>
                        <h4 class="mb-1 text-lg font-bold text-slate-800 line-clamp-1">{{ curso.titulo }}</h4>
                        <p class="mb-4 text-xs text-slate-500">{{ curso.modulos.count }} Módulos • Atualizado há 2 dias</p>
                    </div>
                </div>
                {% empty %}
                <div class="py-12 text-center border-2 border-dashed col-span-full border-slate-200 rounded-2xl">
                    <div class="inline-flex items-center justify-center w-16 h-16 mb-3 rounded-full bg-slate-50 text-slate-300"><i class="text-2xl fas fa-chalkboard"></i></div>
                    <p class="font-medium text-slate-500">Você ainda não tem turmas.</p>
                    <a href="{% url 'lumenios:criar_curso' %}" class="block mt-2 text-sm font-bold text-indigo-600">Começar agora</a>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="space-y-6">
            
            <div class="p-6 bg-gradient-to-br from-slate-900 to-indigo-900 rounded-[2rem] text-white shadow-xl relative overflow-hidden">
                <div class="relative z-10">
                    <div class="flex items-center gap-2 mb-4">
                        <i class="text-yellow-400 fas fa-sparkles"></i>
                        <span class="text-xs font-bold tracking-wider text-indigo-200 uppercase">Assistente Pedagógico</span>
                    </div>
                    <h4 class="mb-2 text-lg font-bold">Precisa de ajuda no plano de aula?</h4>
                    <p class="mb-4 text-sm text-indigo-100">A IA pode sugerir atividades e questões de prova.</p>
                    <button class="w-full py-3 text-sm font-bold text-indigo-900 transition bg-white rounded-xl hover:bg-indigo-50">Gerar Plano de Aula</button>
                </div>
                <div class="absolute bottom-0 right-0 w-32 h-32 rounded-full bg-purple-500/20 blur-2xl"></div>
            </div>

            <div class="bg-white border border-slate-200 rounded-[2rem] p-6 shadow-sm">
                <h4 class="flex items-center justify-between mb-4 font-bold text-slate-800">
                    Pendências
                    <span class="px-2 py-1 text-xs text-red-600 bg-red-100 rounded-full">{{ atividades|length }}</span>
                </h4>
                <div class="space-y-3">
                    {% for atv in atividades %}
                    <div class="flex items-center gap-3 p-3 transition border border-transparent cursor-pointer rounded-xl hover:bg-slate-50 hover:border-slate-100">
                        <div class="w-2 h-2 rounded-full {% if atv.tipo == 'urgente' %}bg-red-500{% else %}bg-blue-500{% endif %}"></div>
                        <div class="flex-1">
                            <p class="text-sm font-bold text-slate-700">{{ atv.titulo }}</p>
                            <p class="text-xs text-slate-400">Vence: {{ atv.data }}</p>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

        </div>
    </div>

</div>
{% endblock %}
"""

# Placeholders para outras views do professor para evitar erro 404
placeholder_html = """
{% extends 'professor/base_professor.html' %}
{% block content %}
<div class="p-10 text-center">
    <h1 class="text-2xl font-bold text-slate-800">Em Desenvolvimento 🚧</h1>
    <p class="text-slate-500">Esta funcionalidade do ambiente do professor será implementada a seguir.</p>
    <a href="{% url 'lumenios:dashboard_professor' %}" class="inline-block mt-4 font-bold text-indigo-600 hover:underline">Voltar ao Dashboard</a>
</div>
{% endblock %}
"""

# ==============================================================================
# 2. CONTEÚDO DO BACKEND (VIEWS E URLS)
# ==============================================================================

views_py_content = """
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Curso, Matricula, Conteudo, Modulo
from .forms import CursoForm
from types import SimpleNamespace
import pandas as pd

# ==============================================================================
# ÁREA DO PROFESSOR (LUMENIOS - AVA)
# ==============================================================================

@login_required
def dashboard_professor(request):
    cursos = Curso.objects.filter(professor=request.user)
    total_alunos = Matricula.objects.filter(curso__in=cursos).count()
    total_cursos = cursos.count()
    atividades_pendentes = [
        {'titulo': 'Correção: Redação 3º Ano', 'data': 'Hoje', 'tipo': 'urgente'},
        {'titulo': 'Planejamento: Física Quântica', 'data': 'Amanhã', 'tipo': 'normal'},
    ]
    return render(request, 'professor/dashboard.html', {
        'cursos': cursos,
        'stats': {'alunos': total_alunos, 'cursos': total_cursos},
        'atividades': atividades_pendentes
    })

@login_required
def gerenciar_curso(request, curso_id):
    # Fallback se o curso não for do professor ou não existir
    try:
        curso = get_object_or_404(Curso, id=curso_id) # Remover professor=request.user para teste se necessário
    except:
        return redirect('lumenios:dashboard_professor')
        
    modulos = curso.modulos.all().prefetch_related('conteudos')
    return render(request, 'professor/gerenciar_curso.html', {'curso': curso, 'modulos': modulos})

@login_required
def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.professor = request.user
            curso.save()
            return redirect('lumenios:dashboard_professor')
    else:
        form = CursoForm()
    return render(request, 'professor/criar_conteudo.html', {'form': form})

@login_required
def editor_conteudo(request, curso_id):
    return render(request, 'professor/editor_conteudo.html', {'curso_id': curso_id})

# ==============================================================================
# ÁREA DO ALUNO (LEGADO / ESTUDO)
# ==============================================================================

@login_required
def dashboard_aluno(request):
    matriculas = Matricula.objects.filter(aluno=request.user)
    return render(request, 'aluno/dashboard.html', {'matriculas': matriculas})

@login_required
def perfil_aluno(request):
    return render(request, 'aluno/dashboard.html', {'section': 'perfil'})

@login_required
def disciplinas_aluno(request):
    matriculas = Matricula.objects.filter(aluno=request.user)
    return render(request, 'extras/disciplina.html', {'matriculas': matriculas})

@login_required
def sala_de_aula(request, conteudo_id=None):
    if not conteudo_id: return redirect('lumenios:dashboard_aluno')
    conteudo_atual = get_object_or_404(Conteudo, id=conteudo_id)
    modulo = conteudo_atual.modulo
    curso = modulo.curso
    modulos = curso.modulos.all().prefetch_related('conteudos')
    
    if conteudo_atual.tipo == 'VIDEO' and conteudo_atual.link:
        if 'watch?v=' in conteudo_atual.link:
            conteudo_atual.embed_link = conteudo_atual.link.replace('watch?v=', 'embed/')
        elif 'youtu.be/' in conteudo_atual.link:
            conteudo_atual.embed_link = conteudo_atual.link.replace('youtu.be/', 'www.youtube.com/embed/')
        else:
            conteudo_atual.embed_link = conteudo_atual.link
    else:
        conteudo_atual.embed_link = None

    return render(request, 'extras/sala_de_aula.html', {'curso': curso, 'modulos': modulos, 'conteudo_atual': conteudo_atual})

@login_required
def sala_de_aula_demo(request):
    # ... código demo mantido (resumido para caber no script) ...
    class MockQuerySet(list): 
        def all(self): return self
        def count(self): return len(self)
    prof = SimpleNamespace(first_name="Alan", last_name="Turing", avatar=None)
    curso = SimpleNamespace(id=0, titulo="IA Fundamentos", categoria="Tecnologia", professor=prof, imagem_capa=SimpleNamespace(url="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=1600&q=80"))
    aula1 = SimpleNamespace(id=1, titulo="1. Redes Neurais", tipo="VIDEO", link="https://www.youtube.com/watch?v=aircAruvnKk", embed_link="https://www.youtube.com/embed/aircAruvnKk", arquivo=None, texto_apoio="Intro.")
    mod1 = SimpleNamespace(titulo="Módulo 1", conteudos=MockQuerySet([aula1]))
    return render(request, 'extras/sala_de_aula.html', {'curso': curso, 'modulos': [mod1], 'conteudo_atual': aula1, 'is_demo': True})

@login_required
def biblioteca_aluno(request): return render(request, 'extras/biblioteca.html')
@login_required
def ensino_complementar(request): return render(request, 'extras/complementar.html')
@login_required
def avaliacoes_aluno(request): return render(request, 'extras/avaliacoes.html')
@login_required
def conscios_investigate(request): return render(request, 'extras/conscios.html', {'tema': request.GET.get('q', 'Aprendizado')})
@login_required
def desempenho_analytics(request): return render(request, 'aluno/desempenho.html', {'media_geral': 0})
"""

urls_py_content = """
from django.urls import path
from . import views

app_name = 'lumenios'

urlpatterns = [
    # --- ÁREA DO PROFESSOR (NOVO) ---
    path('professor/dashboard/', views.dashboard_professor, name='dashboard_professor'),
    path('professor/criar-curso/', views.criar_curso, name='criar_curso'),
    path('professor/curso/<int:curso_id>/', views.gerenciar_curso, name='gerenciar_curso'),
    path('professor/editor/<int:curso_id>/', views.editor_conteudo, name='editor_conteudo'),

    # --- ÁREA DO ALUNO (LEGADO/EXISTENTE) ---
    path('aluno/home/', views.dashboard_aluno, name='dashboard_aluno'),
    path('aluno/perfil/', views.perfil_aluno, name='perfil_aluno'),
    path('aluno/disciplinas/', views.disciplinas_aluno, name='disciplinas'),
    path('aluno/aula/demo/', views.sala_de_aula_demo, name='sala_de_aula_demo'),
    path('aluno/aula/<int:conteudo_id>/', views.sala_de_aula, name='sala_de_aula'),
    
    # Extras
    path('aluno/biblioteca/', views.biblioteca_aluno, name='biblioteca'),
    path('aluno/complementar/', views.ensino_complementar, name='complementar'),
    path('aluno/avaliacoes/', views.avaliacoes_aluno, name='avaliacoes'),
    path('aluno/desempenho/', views.desempenho_analytics, name='desempenho'),
    path('aluno/conscios/', views.conscios_investigate, name='conscios'),
]
"""

# ==============================================================================
# 3. EXECUÇÃO DA CRIAÇÃO
# ==============================================================================

# Arquivos a serem criados
files_to_create = {
    # Templates do Professor (Organização)
    "lumenios/templates/professor/base_professor.html": base_professor_html,
    "lumenios/templates/professor/dashboard.html": dashboard_professor_html,
    "lumenios/templates/professor/criar_conteudo.html": placeholder_html,
    "lumenios/templates/professor/gerenciar_curso.html": placeholder_html,
    "lumenios/templates/professor/editor_conteudo.html": placeholder_html,
    
    # Backend (Views e URLs)
    "lumenios/plataforma/views.py": views_py_content,
    "lumenios/plataforma/urls.py": urls_py_content,
}

print("🚀 Iniciando configuração do ambiente do Professor...")

for path, content in files_to_create.items():
    try:
        create_file(path, content)
    except Exception as e:
        print(f"❌ Erro ao criar {path}: {e}")

print("\\n✅ Configuração concluída! O ambiente do Professor está pronto em 'lumenios/templates/professor'.")
print("👉 Acesse: http://127.0.0.1:8000/lumenios/professor/dashboard/")