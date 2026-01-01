import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'lumenios', 'templates', 'professor', 'dashboard.html')

html_content = """
{% extends 'layouts/base_app.html' %}
{% load static %}
{% load custom_filters %}

{% block title %}Painel do Professor | NioCortex{% endblock %}

{% block content %}
<div class="max-w-[1600px] mx-auto px-4 md:px-8 pb-20 space-y-8" x-data="{ periodo: 'manha' }">

    <div class="bg-white dark:bg-slate-800 rounded-[2rem] p-8 shadow-lg border border-slate-100 dark:border-slate-700 relative overflow-hidden animate-fade-in-down">
        <div class="absolute top-0 right-0 w-64 h-64 -translate-y-1/2 rounded-full bg-indigo-50 dark:bg-indigo-900/20 blur-3xl translate-x-1/4"></div>
        
        <div class="relative z-10 flex flex-col items-center justify-between gap-6 md:flex-row">
            <div class="flex items-center gap-6">
                <div class="flex items-center justify-center w-20 h-20 text-3xl font-bold text-white shadow-lg rounded-2xl bg-gradient-to-br from-indigo-600 to-purple-600 shadow-indigo-500/30">
                    {{ user.first_name|slice:":1" }}
                </div>
                
                <div>
                    <h1 class="text-3xl font-black tracking-tight text-slate-800 dark:text-white">
                        Olá, Prof. <span class="text-indigo-600 dark:text-indigo-400">{{ user.first_name }}</span>!
                    </h1>
                    <div class="flex items-center gap-4 mt-2 font-medium text-slate-500 dark:text-slate-400">
                        <span class="flex items-center gap-2 px-3 py-1 text-xs rounded-full bg-slate-100 dark:bg-slate-700/50">
                            <i class="text-indigo-500 fas fa-layer-group"></i> {{ stats.total_turmas }} Turmas
                        </span>
                        <span class="flex items-center gap-2 px-3 py-1 text-xs rounded-full bg-slate-100 dark:bg-slate-700/50">
                            <i class="fas fa-user-graduate text-emerald-500"></i> {{ stats.total_alunos }} Alunos
                        </span>
                        <span class="flex items-center gap-2 px-3 py-1 text-xs rounded-full bg-slate-100 dark:bg-slate-700/50">
                            <i class="text-orange-500 fas fa-clock"></i> {{ stats.aulas_hoje }} Aulas Hoje
                        </span>
                    </div>
                </div>
            </div>

            <a href="{% url 'pedagogico:form_turmas' %}" class="flex items-center gap-2 px-6 py-3 font-bold text-white transition-transform shadow-xl bg-slate-900 dark:bg-white dark:text-slate-900 rounded-xl hover:scale-105">
                <i class="fas fa-plus"></i> Nova Turma
            </a>
        </div>
    </div>

    <div class="bg-white dark:bg-slate-800 rounded-[2.5rem] shadow-sm border border-slate-100 dark:border-slate-700 overflow-hidden animate-fade-in-up" style="animation-delay: 0.1s;">
        <div class="flex flex-col items-center justify-between gap-4 p-6 border-b border-slate-100 dark:border-slate-700 sm:flex-row bg-slate-50/50 dark:bg-slate-900/20">
            <h2 class="flex items-center gap-2 text-xl font-bold text-slate-800 dark:text-white">
                <i class="text-indigo-500 fas fa-calendar-alt"></i> Grade Horária
            </h2>
            
            <div class="flex p-1 bg-slate-200 dark:bg-slate-700 rounded-xl">
                <button @click="periodo = 'manha'" 
                        :class="periodo === 'manha' ? 'bg-white dark:bg-slate-600 text-indigo-600 dark:text-white shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-700'"
                        class="px-4 py-1.5 rounded-lg text-xs font-bold transition-all">
                    Manhã
                </button>
                <button @click="periodo = 'tarde'" 
                        :class="periodo === 'tarde' ? 'bg-white dark:bg-slate-600 text-indigo-600 dark:text-white shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-700'"
                        class="px-4 py-1.5 rounded-lg text-xs font-bold transition-all">
                    Tarde
                </button>
                <button @click="periodo = 'noite'" 
                        :class="periodo === 'noite' ? 'bg-white dark:bg-slate-600 text-indigo-600 dark:text-white shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-700'"
                        class="px-4 py-1.5 rounded-lg text-xs font-bold transition-all">
                    Noite
                </button>
            </div>
        </div>

        <div class="overflow-x-auto">
            <table class="w-full min-w-[800px]">
                <thead>
                    <tr class="bg-white dark:bg-slate-800">
                        <th class="w-32 px-6 py-4 text-xs font-bold tracking-wider text-left uppercase border-b text-slate-400 border-slate-100 dark:border-slate-700">Horário</th>
                        {% for dia in dias_semana %}
                        <th class="w-1/5 px-6 py-4 text-xs font-bold tracking-wider text-center uppercase border-b text-slate-400 border-slate-100 dark:border-slate-700">{{ dia }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 dark:divide-slate-700">
                    {% for tempo, dias in grade.items %}
                    <tr x-show="(periodo === 'manha' && '{{ tempo }}' < '12:00') || 
                                (periodo === 'tarde' && '{{ tempo }}' >= '12:00' && '{{ tempo }}' < '18:00') || 
                                (periodo === 'noite' && '{{ tempo }}' >= '18:00')"
                        class="transition-colors hover:bg-slate-50/50 dark:hover:bg-slate-700/20">
                        
                        <td class="px-6 py-4 text-xs font-bold border-r text-slate-500 dark:text-slate-400 border-slate-50 dark:border-slate-700 bg-slate-50/30 dark:bg-slate-800">
                            {{ tempo }}
                        </td>

                        {% for dia_nome in dias_semana %}
                            {% with turma=dias|get_item:dia_nome %}
                            <td class="relative h-20 p-2 align-top border-r border-dashed border-slate-100 dark:border-slate-700 last:border-0 group">
                                {% if turma %}
                                <a href="{% url 'pedagogico:detalhar_turma' turma.id %}" class="flex flex-col justify-center block w-full h-full gap-1 p-3 transition-all border-l-4 border-indigo-500 rounded-xl bg-indigo-50 dark:bg-indigo-900/20 hover:bg-indigo-100 dark:hover:bg-indigo-900/40 hover:shadow-md group/card">
                                    <h4 class="text-xs font-black leading-tight text-indigo-900 truncate dark:text-indigo-100 group-hover/card:text-indigo-700">{{ turma.nome }}</h4>
                                    <div class="flex items-center gap-2 mt-1 opacity-70">
                                        <span class="text-[9px] font-bold bg-white/50 px-1.5 py-0.5 rounded text-indigo-800">{{ turma.alunos.count }} alunos</span>
                                        <span class="text-[9px] font-bold text-indigo-400">Sala 3B</span>
                                    </div>
                                </a>
                                {% else %}
                                <div class="flex items-center justify-center w-full h-full transition-opacity opacity-0 group-hover:opacity-100">
                                    <span class="text-[10px] text-slate-300 select-none">-</span>
                                </div>
                                {% endif %}
                            </td>
                            {% endwith %}
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <div class="grid grid-cols-1 gap-8 lg:grid-cols-3 animate-fade-in-up" style="animation-delay: 0.2s;">
        
        <div class="space-y-8 lg:col-span-2">
            
            <div class="relative rounded-[2rem] bg-gradient-to-br from-violet-600 to-fuchsia-700 p-8 text-white overflow-hidden shadow-xl shadow-purple-900/20 flex flex-col justify-center min-h-[220px] group transition-all hover:shadow-purple-900/40 hover:-translate-y-1">
                <div class="absolute top-0 right-0 w-64 h-64 transition-all duration-700 rounded-full translate-x-1/3 -translate-y-1/3 bg-white/10 blur-3xl group-hover:bg-white/20"></div>
                <div class="relative z-10 max-w-lg">
                    <span class="inline-block px-3 py-1 mb-3 text-[10px] font-bold tracking-wide uppercase border rounded-lg bg-white/20 backdrop-blur-md border-white/20">
                        <i class="mr-1 text-yellow-300 fas fa-bullhorn"></i> Mural da Escola
                    </span>
                    <h3 class="mb-2 text-2xl font-bold font-display">Reunião de Pais e Mestres</h3>
                    <p class="mb-6 text-sm leading-relaxed text-purple-100">
                        Sexta-feira, às 19h. Prepare os relatórios de desempenho da turma.
                    </p>
                    <a href="#" class="inline-flex items-center gap-2 px-5 py-2 text-xs font-bold text-purple-700 transition-all bg-white shadow-lg rounded-xl hover:bg-purple-50 hover:scale-105">
                        Ver Pauta <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
                <i class="absolute transition-transform duration-500 opacity-20 fas fa-users text-[8rem] -right-4 -bottom-8 text-white rotate-12 group-hover:rotate-6 group-hover:scale-110"></i>
            </div>

            <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
                <div class="relative p-6 overflow-hidden text-white bg-indigo-900 shadow-lg rounded-[2rem] group border border-indigo-800 hover:-translate-y-1 transition-transform">
                    <div class="relative z-10 space-y-2">
                        <span class="inline-flex items-center gap-1.5 px-3 py-1 text-[10px] font-bold text-indigo-100 uppercase bg-indigo-800/80 rounded-lg border border-indigo-600/50 backdrop-blur-md">
                            <i class="text-yellow-400 fas fa-robot animate-pulse"></i> Sugestão de Conteúdo
                        </span>
                        <h3 class="text-xl font-bold font-display">Metodologias Ativas</h3>
                        <p class="text-xs font-medium text-indigo-200">IA sugere aplicar "Sala de Aula Invertida" na turma 3º A.</p>
                        <button class="mt-4 text-xs font-bold text-white underline decoration-indigo-400 hover:text-indigo-200">Ver plano de aula</button>
                    </div>
                    <div class="absolute -right-10 -bottom-10 w-40 h-40 bg-purple-600 rounded-full blur-[60px] opacity-60 pointer-events-none"></div>
                </div>

                <div class="relative p-6 overflow-hidden text-white bg-emerald-900 shadow-lg rounded-[2rem] group border border-emerald-800 hover:-translate-y-1 transition-transform">
                    <div class="relative z-10 space-y-2">
                        <span class="inline-flex items-center gap-1.5 px-3 py-1 text-[10px] font-bold text-emerald-100 uppercase bg-emerald-800/80 rounded-lg border border-emerald-600/50 backdrop-blur-md">
                            <i class="text-teal-300 fas fa-globe"></i> Atualidades
                        </span>
                        <h3 class="text-xl font-bold font-display">Inteligência Artificial</h3>
                        <p class="text-xs font-medium text-emerald-200">Novo artigo sobre IA na educação disponível na biblioteca.</p>
                        <button class="mt-4 text-xs font-bold text-white underline decoration-emerald-400 hover:text-emerald-200">Ler artigo</button>
                    </div>
                    <div class="absolute -right-10 -top-10 w-40 h-40 bg-teal-500 rounded-full blur-[60px] opacity-40 pointer-events-none"></div>
                </div>
            </div>

        </div>

        <div class="space-y-6">
            
            <div class="flex flex-col p-6 bg-white dark:bg-slate-800 rounded-[2rem] shadow-sm border border-slate-100 dark:border-slate-700">
                <h4 class="flex items-center gap-2 mb-4 font-bold text-slate-800 dark:text-white">
                    <i class="text-red-500 fas fa-fire"></i> Prazos Próximos
                </h4>
                
                <div class="space-y-3">
                    <div class="flex items-center gap-3 p-3 transition-all border border-transparent cursor-pointer rounded-xl hover:bg-slate-50 dark:hover:bg-slate-700/50 group hover:border-red-100">
                        <div class="flex flex-col items-center justify-center w-10 h-10 text-xs font-bold leading-none text-red-500 rounded-lg shadow-sm bg-red-50">
                            20<span>OUT</span>
                        </div>
                        <div>
                            <div class="text-xs font-bold text-slate-700 dark:text-slate-300 group-hover:text-red-600">Fechar Notas 3º Bim</div>
                            <div class="text-[10px] text-slate-400">Todas as Turmas</div>
                        </div>
                    </div>

                    <div class="flex items-center gap-3 p-3 transition-all border border-transparent cursor-pointer rounded-xl hover:bg-slate-50 dark:hover:bg-slate-700/50 group hover:border-orange-100">
                        <div class="flex flex-col items-center justify-center w-10 h-10 text-xs font-bold leading-none text-orange-500 rounded-lg shadow-sm bg-orange-50">
                            22<span>OUT</span>
                        </div>
                        <div>
                            <div class="text-xs font-bold text-slate-700 dark:text-slate-300 group-hover:text-orange-600">Entrega Planejamento</div>
                            <div class="text-[10px] text-slate-400">Coordenação</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bg-slate-900 rounded-[2rem] p-6 text-white shadow-xl relative overflow-hidden">
                <div class="absolute inset-0 bg-gradient-to-br from-slate-900 to-indigo-950"></div>
                <div class="relative z-10">
                    <h4 class="flex items-center justify-center gap-2 mb-4 text-sm font-bold text-center">
                        <i class="text-indigo-400 fas fa-folder-open"></i> Materiais Extras
                    </h4>
                    <div class="flex flex-wrap justify-center gap-2">
                        <a href="#" class="px-3 py-1.5 text-[10px] font-bold transition-all border rounded-lg bg-white/5 hover:bg-indigo-600 hover:border-indigo-500 border-white/10 hover:-translate-y-0.5">BNCC PDF</a>
                        <a href="#" class="px-3 py-1.5 text-[10px] font-bold transition-all border rounded-lg bg-white/5 hover:bg-purple-600 hover:border-purple-500 border-white/10 hover:-translate-y-0.5">Modelos de Prova</a>
                        <a href="#" class="px-3 py-1.5 text-[10px] font-bold transition-all border rounded-lg bg-white/5 hover:bg-emerald-600 hover:border-emerald-500 border-white/10 hover:-translate-y-0.5">Dinâmicas</a>
                    </div>
                    <p class="text-[9px] text-center text-slate-500 mt-4 uppercase tracking-widest font-bold">Banco de Questões</p>
                </div>
            </div>

        </div>
    </div>

</div>
{% endblock %}
"""

def update_template():
    print("🎨 Aplicando layout 'Clean & Productive' no Dashboard do Professor...")
    with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ Sucesso! Template atualizado.")

if __name__ == "__main__":
    update_template()
    print("\n🚀 Acesse agora: http://127.0.0.1:8000/lumenios/professor/dashboard/")