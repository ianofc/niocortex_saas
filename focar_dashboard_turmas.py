import os

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIEW_PATH = os.path.join(BASE_DIR, 'lumenios', 'plataforma', 'views.py')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'lumenios', 'templates', 'professor', 'dashboard.html')

# ==============================================================================
# 1. REESCREVER A VIEW (Foco em Turmas)
# ==============================================================================
def rewrite_view():
    print("🐍 Ajustando 'views.py' para priorizar Turmas Escolares...")
    
    # Lógica nova da View
    new_view_code = """
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from lumenios.plataforma.models import Curso, Matricula, Conteudo, Modulo
from lumenios.pedagogico.models import Turma, Aluno, DiarioClasse, Atividade
from django.db.models import Count
from django.utils import timezone

@login_required
def dashboard_professor(request):
    # ---------------------------------------------------------
    # 1. FOCO PRINCIPAL: TURMAS (Gestão Escolar)
    # ---------------------------------------------------------
    if request.user.is_superuser:
        turmas = Turma.objects.all().order_by('nome')
    else:
        turmas = Turma.objects.filter(professor_regente=request.user).order_by('nome')

    # Estatísticas Rápidas das Turmas
    total_alunos = Aluno.objects.filter(turma__in=turmas).count()
    aulas_hoje = DiarioClasse.objects.filter(professor=request.user, data=timezone.now()).count()
    
    # ---------------------------------------------------------
    # 2. COMPLEMENTO: CURSOS (Biblioteca do Sistema)
    # ---------------------------------------------------------
    # Mostra cursos disponíveis no sistema (sem professor específico, pois é institucional)
    cursos_disponiveis = Curso.objects.all()[:5]  # Pega os 5 primeiros como destaque

    # ---------------------------------------------------------
    # 3. AGENDA / PENDÊNCIAS
    # ---------------------------------------------------------
    atividades_recentes = Atividade.objects.filter(turma__in=turmas).order_by('-data_aplicacao')[:3]

    return render(request, 'professor/dashboard.html', {
        'turmas': turmas,
        'cursos': cursos_disponiveis,
        'stats': {
            'total_alunos': total_alunos,
            'total_turmas': turmas.count(),
            'aulas_hoje': aulas_hoje
        },
        'atividades': atividades_recentes,
        'hoje': timezone.now()
    })

# Mantenha as outras views abaixo...
"""
    
    # Lê o arquivo atual para preservar o resto
    with open(VIEW_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Substitui a função dashboard_professor antiga
    # Vamos ser agressivos e reescrever o início do arquivo até a próxima função
    # (Assumindo que dashboard_professor é a primeira ou importações estão no topo)
    
    # Estratégia segura: Ler tudo, remover a dashboard antiga e inserir a nova
    lines = content.splitlines()
    new_lines = []
    skip = False
    
    # Adiciona imports necessários se não existirem
    imports_needed = [
        "from lumenios.pedagogico.models import Turma, Aluno, DiarioClasse, Atividade",
        "from django.utils import timezone",
        "from django.db.models import Count"
    ]
    
    # Injeta imports no topo
    for imp in imports_needed:
        if imp not in content:
            new_lines.append(imp)
            
    for line in lines:
        if line.strip().startswith("def dashboard_professor(request):"):
            skip = True
            new_lines.append(new_view_code.split("def dashboard_professor")[0]) # Pega imports extras se houver no bloco string
            # Extrai apenas o corpo da função da string acima
            func_body = new_view_code.split("@login_required")[1] 
            new_lines.append("@login_required" + func_body)
        
        if skip and line.strip().startswith("@login_required") and "def dashboard_professor" not in line:
            skip = False
        
        if not skip:
            new_lines.append(line)

    # Salva
    with open(VIEW_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_lines))
    print("   ✅ View atualizada.")

# ==============================================================================
# 2. REESCREVER O TEMPLATE (Visual Focado na Escola)
# ==============================================================================
def rewrite_template():
    print("\nhtml Recriando 'dashboard.html' com foco em Turmas...")
    
    html_content = """
{% extends 'layouts/base_app.html' %}
{% load static %}

{% block title %}Sala dos Professores | NioCortex{% endblock %}

{% block content %}
<div class="mx-auto max-w-7xl">
    
    <div class="flex flex-col items-center justify-between gap-4 mb-8 md:flex-row animate-fade-in-down">
        <div>
            <h1 class="text-3xl font-black tracking-tight text-slate-800 dark:text-white">
                Olá, Professor(a) <span class="text-indigo-600">{{ user.first_name }}</span>!
            </h1>
            <p class="mt-1 text-slate-500 dark:text-slate-400">
                Aqui está o resumo das suas turmas hoje, {{ hoje|date:"l, d/m" }}.
            </p>
        </div>
        <div class="flex gap-3">
            <a href="{% url 'pedagogico:form_turmas' %}" class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-bold shadow-lg shadow-indigo-200 transition flex items-center gap-2">
                <i class="fas fa-plus"></i> Nova Turma
            </a>
        </div>
    </div>

    <div class="grid grid-cols-1 gap-6 mb-10 md:grid-cols-3 animate-fade-in-down" style="animation-delay: 0.1s;">
        <div class="flex items-center gap-4 p-6 bg-white border shadow-sm dark:bg-gray-800 rounded-2xl border-slate-100 dark:border-gray-700">
            <div class="p-4 text-blue-600 bg-blue-50 dark:bg-blue-900/20 rounded-xl">
                <i class="text-2xl fas fa-chalkboard-teacher"></i>
            </div>
            <div>
                <p class="text-sm font-medium text-slate-500">Minhas Turmas</p>
                <h3 class="text-2xl font-black text-slate-800 dark:text-white">{{ stats.total_turmas }}</h3>
            </div>
        </div>

        <div class="flex items-center gap-4 p-6 bg-white border shadow-sm dark:bg-gray-800 rounded-2xl border-slate-100 dark:border-gray-700">
            <div class="p-4 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 rounded-xl">
                <i class="text-2xl fas fa-user-graduate"></i>
            </div>
            <div>
                <p class="text-sm font-medium text-slate-500">Total de Alunos</p>
                <h3 class="text-2xl font-black text-slate-800 dark:text-white">{{ stats.total_alunos }}</h3>
            </div>
        </div>

        <div class="flex items-center gap-4 p-6 bg-white border shadow-sm dark:bg-gray-800 rounded-2xl border-slate-100 dark:border-gray-700">
            <div class="p-4 text-purple-600 bg-purple-50 dark:bg-purple-900/20 rounded-xl">
                <i class="text-2xl fas fa-clock"></i>
            </div>
            <div>
                <p class="text-sm font-medium text-slate-500">Aulas Hoje</p>
                <h3 class="text-2xl font-black text-slate-800 dark:text-white">{{ stats.aulas_hoje }}</h3>
            </div>
        </div>
    </div>

    <div class="mb-10 animate-fade-in-down" style="animation-delay: 0.2s;">
        <div class="flex items-center justify-between mb-6">
            <h2 class="flex items-center gap-2 text-xl font-bold text-slate-800 dark:text-white">
                <i class="text-indigo-500 fas fa-layer-group"></i> Gestão de Turmas
            </h2>
        </div>

        {% if turmas %}
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {% for turma in turmas %}
            <div class="p-6 transition-all duration-300 bg-white border shadow-sm dark:bg-gray-800 rounded-2xl border-slate-200 dark:border-gray-700 hover:shadow-lg hover:-translate-y-1 group">
                <div class="flex items-start justify-between mb-4">
                    <div class="flex items-center gap-3">
                        <div class="flex items-center justify-center w-10 h-10 text-lg font-bold text-indigo-600 rounded-lg bg-indigo-50">
                            {{ turma.nome|slice:":1" }}
                        </div>
                        <div>
                            <h3 class="text-lg font-bold transition text-slate-800 dark:text-white group-hover:text-indigo-600">{{ turma.nome }}</h3>
                            <span class="text-xs font-bold tracking-wide uppercase text-slate-400">{{ turma.ano_letivo }}</span>
                        </div>
                    </div>
                    <div class="relative">
                        <button class="text-slate-400 hover:text-indigo-600"><i class="fas fa-ellipsis-v"></i></button>
                    </div>
                </div>

                <div class="grid grid-cols-3 gap-2 mb-6 text-center">
                    <a href="{% url 'pedagogico:gradebook' %}?turma_id={{ turma.id }}" class="p-2 transition rounded-lg hover:bg-slate-50 group/icon">
                        <i class="mb-1 text-xl fas fa-clipboard-list text-slate-300 group-hover/icon:text-indigo-500"></i>
                        <p class="text-[10px] font-bold text-slate-500">Notas</p>
                    </a>
                    <a href="#" class="p-2 transition rounded-lg hover:bg-slate-50 group/icon">
                        <i class="mb-1 text-xl fas fa-check-circle text-slate-300 group-hover/icon:text-emerald-500"></i>
                        <p class="text-[10px] font-bold text-slate-500">Freq.</p>
                    </a>
                    <a href="#" class="p-2 transition rounded-lg hover:bg-slate-50 group/icon">
                        <i class="mb-1 text-xl fas fa-book-open text-slate-300 group-hover/icon:text-blue-500"></i>
                        <p class="text-[10px] font-bold text-slate-500">Diário</p>
                    </a>
                </div>

                <a href="{% url 'pedagogico:detalhar_turma' turma.id %}" class="block w-full py-3 font-bold text-center transition-colors rounded-xl bg-slate-50 dark:bg-gray-700 text-slate-600 dark:text-gray-300 hover:bg-indigo-600 hover:text-white">
                    Acessar Turma
                </a>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="py-16 text-center border-2 border-dashed bg-slate-50 dark:bg-gray-800 rounded-2xl border-slate-200">
            <div class="inline-flex p-4 mb-4 bg-white rounded-full shadow-sm">
                <i class="text-3xl fas fa-school text-slate-300"></i>
            </div>
            <h3 class="text-lg font-bold text-slate-700">Nenhuma turma encontrada</h3>
            <p class="max-w-md mx-auto mb-6 text-slate-500">Você ainda não foi vinculado a nenhuma turma escolar. Crie uma nova ou solicite à coordenação.</p>
            <a href="{% url 'pedagogico:form_turmas' %}" class="px-6 py-3 font-bold text-white transition bg-indigo-600 rounded-xl hover:bg-indigo-700">
                Criar Primeira Turma
            </a>
        </div>
        {% endif %}
    </div>

    <div class="pt-8 mt-12 transition-opacity border-t border-slate-200 dark:border-gray-700 opacity-80 hover:opacity-100">
        <h2 class="flex items-center gap-2 mb-6 text-lg font-bold text-slate-600 dark:text-gray-300">
            <i class="fas fa-video text-slate-400"></i> Cursos Complementares (Institucional)
        </h2>
        
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-4">
            {% for curso in cursos %}
            <a href="#" class="flex items-center gap-3 p-3 transition bg-white border dark:bg-gray-800 rounded-xl border-slate-100 hover:border-indigo-200 group">
                <div class="w-12 h-12 overflow-hidden bg-gray-200 rounded-lg">
                    {% if curso.imagem_capa %}
                    <img src="{{ curso.imagem_capa.url }}" class="object-cover w-full h-full">
                    {% else %}
                    <div class="flex items-center justify-center w-full h-full bg-slate-200 text-slate-400"><i class="fas fa-image"></i></div>
                    {% endif %}
                </div>
                <div>
                    <h4 class="w-32 text-sm font-bold truncate text-slate-700 group-hover:text-indigo-600">{{ curso.titulo }}</h4>
                    <span class="text-[10px] text-slate-400 uppercase font-bold">Conteúdo Extra</span>
                </div>
            </a>
            {% empty %}
            <p class="col-span-4 text-sm italic text-slate-400">Nenhum curso extra disponível no momento.</p>
            {% endfor %}
        </div>
    </div>

</div>
{% endblock %}
"""
    
    with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("   ✅ Template atualizado.")

if __name__ == "__main__":
    rewrite_view()
    rewrite_template()
    print("\n✨ DASHBOARD RECONFIGURADO!")
    print("   Agora as TURMAS (Escola) são o destaque principal.")
    print("   Os CURSOS (AVA) aparecem discretamente no rodapé.")