import os

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'lumenios', 'templates', 'professor', 'dashboard.html')

# ==============================================================================
# NOVO TEMPLATE (Visual Aluno + Ferramentas Professor)
# ==============================================================================
html_content = """
{% extends 'layouts/base_app.html' %}
{% load static %}

{% block title %}Sala dos Professores | NioCortex{% endblock %}

{% block content %}
<div class="max-w-[1600px] mx-auto px-6 space-y-8 pb-20">

    <section class="relative rounded-[2.5rem] overflow-hidden shadow-2xl h-[340px] group bg-slate-900 border border-slate-800">
        <div class="absolute inset-0 overflow-hidden">
            <img src="https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=1600&q=80" 
                 class="w-full h-full object-cover transition-transform duration-[5s] ease-in-out group-hover:scale-110 opacity-40"
                 alt="Sala dos Professores">
        </div>
        
        <div class="absolute inset-0 bg-gradient-to-r from-indigo-900/95 via-blue-900/80 to-transparent mix-blend-multiply"></div>
        <div class="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/40 to-transparent"></div>

        <div class="absolute inset-0 flex items-center px-8 md:px-16 lg:px-20">
            <div class="relative z-10 w-full max-w-4xl">
                <div class="flex flex-col items-end justify-between gap-6 md:flex-row">
                    <div class="space-y-4">
                        <div class="animate-fade-in-up" style="animation-delay: 0.1s;">
                            <span class="inline-flex items-center gap-2 px-3 py-1.5 text-xs font-bold tracking-wider text-blue-200 uppercase border rounded-full shadow-lg bg-white/10 backdrop-blur-md border-white/20">
                                <i class="fas fa-chalkboard-teacher"></i> Painel Docente
                            </span>
                        </div>
                        
                        <div class="animate-fade-in-up" style="animation-delay: 0.2s;">
                            <h1 class="text-4xl font-bold leading-tight text-white md:text-5xl lg:text-6xl font-display drop-shadow-xl">
                                Olá, Prof. <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-300 via-indigo-300 to-cyan-300">{{ user.first_name }}</span>.
                            </h1>
                            <p class="mt-2 text-lg font-medium text-blue-100/80">
                                Você tem <strong class="text-white">{{ stats.total_turmas }} turmas</strong> ativas e <strong class="text-white">{{ stats.aulas_hoje }} aulas</strong> hoje.
                            </p>
                        </div>
                    </div>

                    <div class="flex gap-3 animate-fade-in-up" style="animation-delay: 0.3s;">
                        <a href="{% url 'pedagogico:form_turmas' %}" 
                           class="flex items-center gap-2 px-6 py-3 font-bold text-white transition-all bg-indigo-600 shadow-xl rounded-2xl hover:bg-indigo-500 hover:shadow-indigo-500/40 hover:-translate-y-1">
                            <i class="fas fa-plus"></i> Nova Turma
                        </a>
                        <button onclick="alert('Funcionalidade de Grade em breve!')" 
                           class="flex items-center gap-2 px-6 py-3 font-bold text-indigo-100 transition-all border shadow-xl bg-white/10 backdrop-blur-md border-white/20 rounded-2xl hover:bg-white/20 hover:text-white hover:-translate-y-1">
                            <i class="fas fa-calendar-alt"></i> Grade
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="relative z-20 grid grid-cols-1 gap-6 px-4 -mt-12 md:grid-cols-3">
        <div class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl p-6 rounded-[2rem] shadow-lg border border-white/50 dark:border-slate-700 flex items-center gap-5 hover:-translate-y-1 transition-transform duration-300">
            <div class="flex items-center justify-center text-white shadow-lg w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-400 to-teal-500 shadow-emerald-500/30">
                <i class="text-2xl fas fa-user-graduate"></i>
            </div>
            <div>
                <p class="text-sm font-bold tracking-wide uppercase text-slate-500 dark:text-slate-400">Total de Alunos</p>
                <h3 class="text-3xl font-black text-slate-800 dark:text-white">{{ stats.total_alunos }}</h3>
            </div>
        </div>

        <div class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl p-6 rounded-[2rem] shadow-lg border border-white/50 dark:border-slate-700 flex items-center gap-5 hover:-translate-y-1 transition-transform duration-300">
            <div class="flex items-center justify-center text-white shadow-lg w-14 h-14 rounded-2xl bg-gradient-to-br from-orange-400 to-red-500 shadow-orange-500/30">
                <i class="text-2xl fas fa-fire"></i>
            </div>
            <div>
                <p class="text-sm font-bold tracking-wide uppercase text-slate-500 dark:text-slate-400">Pendências</p>
                <h3 class="text-3xl font-black text-slate-800 dark:text-white">{{ atividades|length }}</h3>
            </div>
        </div>

        <div class="bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl p-6 rounded-[2rem] shadow-lg border border-white/50 dark:border-slate-700 flex items-center gap-5 hover:-translate-y-1 transition-transform duration-300">
            <div class="flex items-center justify-center text-white shadow-lg w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-indigo-600 shadow-purple-500/30">
                <i class="text-2xl fas fa-layer-group"></i>
            </div>
            <div>
                <p class="text-sm font-bold tracking-wide uppercase text-slate-500 dark:text-slate-400">Planejamentos</p>
                <h3 class="text-3xl font-black text-slate-800 dark:text-white">Ativo</h3>
            </div>
        </div>
    </section>

    <div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
        
        <div class="space-y-6 lg:col-span-2">
            <div class="flex items-center justify-between">
                <h2 class="flex items-center gap-3 text-2xl font-bold text-slate-800 dark:text-white">
                    <span class="w-2 h-8 bg-indigo-600 rounded-full"></span>
                    Minhas Turmas
                </h2>
                <a href="{% url 'pedagogico:listar_turmas' %}" class="text-sm font-bold text-indigo-600 transition-colors hover:text-indigo-800">Ver todas <i class="ml-1 fas fa-arrow-right"></i></a>
            </div>

            {% if turmas %}
            <div class="grid grid-cols-1 gap-5 md:grid-cols-2">
                {% for turma in turmas %}
                <div class="group relative bg-white dark:bg-slate-800 rounded-[2rem] p-6 shadow-sm border border-slate-100 dark:border-slate-700 hover:shadow-xl hover:border-indigo-100 dark:hover:border-slate-600 transition-all duration-300 hover:-translate-y-1">
                    
                    <div class="flex items-start justify-between mb-6">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 rounded-2xl flex items-center justify-center text-white font-bold text-lg shadow-md
                                {% if forloop.counter|divisibleby:2 %} bg-gradient-to-br from-purple-500 to-pink-500
                                {% else %} bg-gradient-to-br from-blue-500 to-indigo-600 {% endif %}">
                                {{ turma.nome|slice:":1" }}
                            </div>
                            <div>
                                <h3 class="text-lg font-bold transition-colors text-slate-800 dark:text-white group-hover:text-indigo-600">{{ turma.nome }}</h3>
                                <div class="flex items-center gap-2 text-xs font-medium text-slate-500">
                                    <span class="bg-slate-100 dark:bg-slate-700 px-2 py-0.5 rounded text-slate-600 dark:text-slate-300">{{ turma.ano_letivo }}</span>
                                    <span>• {{ turma.alunos.count }} Alunos</span>
                                </div>
                            </div>
                        </div>
                        <div class="relative">
                            <button class="transition-colors text-slate-300 hover:text-slate-600 dark:hover:text-white"><i class="fas fa-ellipsis-h"></i></button>
                        </div>
                    </div>

                    <div class="grid grid-cols-3 gap-2 mb-6">
                        <a href="{% url 'pedagogico:gradebook' %}?turma_id={{ turma.id }}" 
                           class="flex flex-col items-center justify-center p-2 transition-colors rounded-xl bg-slate-50 dark:bg-slate-700/50 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 group/btn">
                            <i class="mb-1 text-lg fas fa-clipboard-list text-slate-400 group-hover/btn:text-indigo-500"></i>
                            <span class="text-[10px] font-bold text-slate-500 group-hover/btn:text-indigo-600">Notas</span>
                        </a>
                        <a href="#" class="flex flex-col items-center justify-center p-2 transition-colors rounded-xl bg-slate-50 dark:bg-slate-700/50 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 group/btn">
                            <i class="mb-1 text-lg fas fa-check-circle text-slate-400 group-hover/btn:text-emerald-500"></i>
                            <span class="text-[10px] font-bold text-slate-500 group-hover/btn:text-emerald-600">Freq.</span>
                        </a>
                        <a href="#" class="flex flex-col items-center justify-center p-2 transition-colors rounded-xl bg-slate-50 dark:bg-slate-700/50 hover:bg-blue-50 dark:hover:bg-blue-900/20 group/btn">
                            <i class="mb-1 text-lg fas fa-book-open text-slate-400 group-hover/btn:text-blue-500"></i>
                            <span class="text-[10px] font-bold text-slate-500 group-hover/btn:text-blue-600">Diário</span>
                        </a>
                    </div>

                    <a href="{% url 'pedagogico:detalhar_turma' turma.id %}" 
                       class="flex items-center justify-center w-full py-3 text-sm font-bold transition-all rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:bg-indigo-600 hover:text-white hover:shadow-lg hover:shadow-indigo-200">
                        Gerenciar Turma
                    </a>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <div class="py-20 text-center border-2 border-dashed bg-slate-50/50 dark:bg-gray-800 rounded-[2.5rem] border-slate-200 dark:border-slate-700">
                <div class="inline-flex p-6 mb-6 bg-white rounded-full shadow-md dark:bg-slate-700">
                    <i class="text-4xl fas fa-school text-slate-300"></i>
                </div>
                <h3 class="text-xl font-bold text-slate-700 dark:text-white">Nenhuma turma encontrada</h3>
                <p class="max-w-md mx-auto mt-2 mb-8 text-slate-500">Você ainda não foi vinculado a nenhuma turma escolar. Crie uma nova para começar.</p>
                <a href="{% url 'pedagogico:form_turmas' %}" class="px-8 py-4 font-bold text-white transition bg-indigo-600 shadow-lg rounded-2xl hover:bg-indigo-700 shadow-indigo-200">
                    Criar Primeira Turma
                </a>
            </div>
            {% endif %}
        </div>

        <div class="space-y-8">
            
            <div class="bg-white dark:bg-slate-800 p-6 rounded-[2rem] shadow-sm border border-slate-100 dark:border-slate-700 relative overflow-hidden">
                <div class="flex items-center justify-between mb-6">
                    <h3 class="flex items-center gap-2 text-lg font-bold text-slate-800 dark:text-white">
                        <i class="text-yellow-500 fas fa-sticky-note"></i> Lembretes
                    </h3>
                    <button class="flex items-center justify-center w-8 h-8 transition rounded-full bg-slate-100 dark:bg-slate-700 text-slate-500 hover:bg-indigo-100 hover:text-indigo-600">
                        <i class="text-xs fas fa-plus"></i>
                    </button>
                </div>
                
                <div class="space-y-3">
                    <div class="flex items-start gap-3 p-3 border border-yellow-100 bg-yellow-50 dark:bg-yellow-900/10 dark:border-yellow-900/30 rounded-xl group">
                        <div class="mt-0.5">
                            <i class="text-yellow-400 cursor-pointer far fa-square group-hover:text-yellow-600"></i>
                        </div>
                        <p class="text-xs font-medium leading-relaxed text-slate-600 dark:text-slate-300">
                            Lançar notas do 3º Bimestre até sexta-feira.
                        </p>
                    </div>
                    <div class="flex items-start gap-3 p-3 border bg-slate-50 dark:bg-slate-700/30 border-slate-100 dark:border-slate-700 rounded-xl group opacity-60">
                        <div class="mt-0.5">
                            <i class="far fa-check-square text-slate-400"></i>
                        </div>
                        <p class="text-xs font-medium line-through text-slate-500">
                            Reunião pedagógica às 14h.
                        </p>
                    </div>
                </div>
                
                <div class="absolute -bottom-10 -right-10 w-32 h-32 bg-yellow-100 rounded-full blur-[60px] opacity-50 pointer-events-none"></div>
            </div>

            <div class="bg-gradient-to-br from-indigo-900 to-slate-900 p-8 rounded-[2.5rem] text-white shadow-2xl relative overflow-hidden group cursor-pointer hover:shadow-indigo-900/30 transition-all hover:-translate-y-1">
                <div class="relative z-10">
                    <div class="inline-flex items-center gap-2 px-3 py-1 mb-4 text-[10px] font-bold text-indigo-200 uppercase bg-white/10 rounded-lg border border-white/10 backdrop-blur-md">
                        <i class="fas fa-play-circle"></i> Conteúdo AVA
                    </div>
                    <h3 class="mb-2 text-2xl font-bold font-display">Biblioteca de Cursos</h3>
                    <p class="mb-6 text-sm font-medium text-indigo-200">Acesse materiais complementares e cursos institucionais.</p>
                    
                    <div class="flex mb-6 -space-x-3">
                        {% for curso in cursos|slice:":3" %}
                        <div class="relative w-10 h-10 overflow-hidden border-2 border-indigo-900 rounded-full bg-slate-700" title="{{ curso.titulo }}">
                            {% if curso.imagem_capa %}
                            <img src="{{ curso.imagem_capa.url }}" class="object-cover w-full h-full">
                            {% else %}
                            <div class="flex items-center justify-center w-full h-full bg-slate-600 text-[10px]">{{ curso.titulo|slice:":1" }}</div>
                            {% endif %}
                        </div>
                        {% endfor %}
                        {% if cursos|length > 3 %}
                        <div class="flex items-center justify-center w-10 h-10 text-xs font-bold text-white bg-indigo-600 border-2 border-indigo-900 rounded-full">
                            +{{ cursos|length|add:"-3" }}
                        </div>
                        {% endif %}
                    </div>

                    <a href="#" class="inline-flex items-center gap-2 text-sm font-bold text-white transition-colors hover:text-indigo-200">
                        Explorar Catálogo <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
                
                <div class="absolute -right-10 top-10 w-40 h-40 bg-indigo-500 rounded-full blur-[80px] opacity-40 group-hover:opacity-60 transition-opacity"></div>
            </div>

        </div>
    </div>
</div>
{% endblock %}
"""

def apply_template():
    print("🎨 Aplicando novo design ao Dashboard do Professor...")
    
    if not os.path.exists(os.path.dirname(TEMPLATE_PATH)):
        os.makedirs(os.path.dirname(TEMPLATE_PATH))
        
    with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Sucesso! O arquivo foi atualizado em:", TEMPLATE_PATH)

if __name__ == "__main__":
    apply_template()