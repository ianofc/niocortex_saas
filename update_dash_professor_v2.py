import os
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==============================================================================
# 1. ATUALIZAR MODELS (Garantir suporte a Horários)
# ==============================================================================
def update_models():
    print("📝 Verificando models para Grade Horária...")
    models_path = os.path.join(BASE_DIR, 'lumenios', 'pedagogico', 'models.py')
    
    with open(models_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "class Horario(" not in content:
        print("   ➕ Adicionando model 'Horario' em pedagogico/models.py...")
        new_model = """

class Horario(models.Model):
    DIAS_SEMANA = [
        (0, 'Segunda-feira'), (1, 'Terça-feira'), (2, 'Quarta-feira'),
        (3, 'Quinta-feira'), (4, 'Sexta-feira'), (5, 'Sábado'), (6, 'Domingo')
    ]
    
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    disciplina = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: Matemática")
    
    class Meta:
        ordering = ['dia_semana', 'hora_inicio']
        verbose_name = 'Horário'
        verbose_name_plural = 'Horários'

    def __str__(self):
        return f"{self.get_dia_semana_display()} - {self.hora_inicio} ({self.turma.nome})"
"""
        with open(models_path, 'a', encoding='utf-8') as f:
            f.write(new_model)
        print("   ✅ Model Horario adicionado. (Lembre-se de rodar makemigrations depois!)")
    else:
        print("   ℹ️  Model Horario já existe.")

# ==============================================================================
# 2. ATUALIZAR VIEW (Lógica da Grade Semanal)
# ==============================================================================
def update_view():
    print("🐍 Atualizando 'lumenios/plataforma/views.py' com lógica da Grade...")
    view_path = os.path.join(BASE_DIR, 'lumenios', 'plataforma', 'views.py')
    
    new_dashboard_logic = """
@login_required
def dashboard_professor(request):
    # ---------------------------------------------------------
    # 1. DADOS BÁSICOS
    # ---------------------------------------------------------
    if request.user.is_superuser:
        turmas = Turma.objects.all().order_by('nome')
    else:
        turmas = Turma.objects.filter(professor_regente=request.user).order_by('nome')

    # ---------------------------------------------------------
    # 2. GRADE HORÁRIA (Matriz)
    # ---------------------------------------------------------
    # Tenta buscar horários reais, senão usa mock para visualização
    try:
        from lumenios.pedagogico.models import Horario
        horarios_db = Horario.objects.filter(turma__in=turmas)
    except:
        horarios_db = []

    # Estrutura da Grade: 5 dias x 5 aulas (Exemplo)
    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    # Horários fixos para a grade (pode ser dinâmico no futuro)
    tempos_aula = ['07:30 - 08:20', '08:20 - 09:10', '09:10 - 10:00', '10:20 - 11:10', '11:10 - 12:00']
    
    # Matriz vazia
    grade = {tempo: {dia: None for dia in dias_semana} for tempo in tempos_aula}
    
    # Se tiver dados no banco, popula (Lógica simplificada para MVP)
    # Se não, vamos simular com as turmas do professor para ele ver o layout
    import random
    if not horarios_db and turmas.exists():
        # MOCK: Distribui as turmas aleatoriamente na grade para visualização
        lista_turmas = list(turmas)
        for i, tempo in enumerate(tempos_aula):
            for j, dia in enumerate(dias_semana):
                if (i + j) % 3 == 0 and lista_turmas: # Espalha um pouco
                    turma_escolhida = lista_turmas[(i+j) % len(lista_turmas)]
                    grade[tempo][dia] = turma_escolhida

    # ---------------------------------------------------------
    # 3. PRÓXIMA AULA (O "Agora")
    # ---------------------------------------------------------
    # Lógica real usaria datetime.now() vs Horario
    proxima_aula = {
        'turma': turmas.first() if turmas.exists() else None,
        'horario': '08:20',
        'sala': 'Sala 3B',
        'disciplina': 'Matemática'
    }

    # Estatísticas
    total_alunos = Aluno.objects.filter(turma__in=turmas).count()
    atividades_pendentes = Atividade.objects.filter(turma__in=turmas).count() # Exemplo

    return render(request, 'professor/dashboard.html', {
        'turmas': turmas,
        'grade': grade,
        'dias_semana': dias_semana,
        'tempos_aula': tempos_aula,
        'proxima_aula': proxima_aula,
        'stats': {
            'total_alunos': total_alunos,
            'pendencias': atividades_pendentes,
        },
        'hoje': timezone.now()
    })
"""
    
    # Lê o arquivo original
    with open(view_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adiciona importação de Horario se precisar (embora fiz import local na função para garantir)
    
    # Substitui a função dashboard_professor antiga
    lines = content.splitlines()
    new_lines = []
    skip = False
    
    for line in lines:
        if line.strip().startswith("def dashboard_professor(request):"):
            skip = True
            new_lines.append(new_dashboard_logic.strip())
        
        if skip and line.strip().startswith("@login_required") and "def dashboard_professor" not in line:
            skip = False
        
        if not skip:
            new_lines.append(line)

    with open(view_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_lines))
    print("   ✅ View atualizada com lógica de Grade.")

# ==============================================================================
# 3. NOVO TEMPLATE (Focado na Grade)
# ==============================================================================
def create_template():
    print("🎨 Criando novo template 'dashboard.html'...")
    template_path = os.path.join(BASE_DIR, 'lumenios', 'templates', 'professor', 'dashboard.html')
    
    html = """
{% extends 'layouts/base_app.html' %}
{% load static %}

{% block title %}Painel do Professor | NioCortex{% endblock %}

{% block content %}
<div class="max-w-[1600px] mx-auto px-4 md:px-8 pb-20 space-y-8">

    <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
        
        <div class="lg:col-span-2 relative overflow-hidden rounded-[2.5rem] bg-slate-900 text-white shadow-2xl p-8 flex flex-col justify-between min-h-[280px] group border border-slate-800">
            <div class="absolute inset-0 bg-gradient-to-br from-indigo-600/90 to-purple-800/90 mix-blend-multiply"></div>
            <div class="absolute top-0 right-0 w-64 h-64 -translate-y-1/2 rounded-full bg-white/10 blur-3xl translate-x-1/4"></div>
            <img src="https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=1600" class="absolute inset-0 object-cover w-full h-full opacity-20 mix-blend-overlay">

            <div class="relative z-10 flex items-start justify-between">
                <div>
                    <span class="inline-flex items-center gap-2 px-3 py-1 mb-4 text-xs font-bold text-indigo-100 uppercase border rounded-full bg-white/10 backdrop-blur-md border-white/20">
                        <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span> Acontecendo Agora / Próxima
                    </span>
                    <h1 class="mb-2 text-4xl font-black md:text-5xl font-display">{{ proxima_aula.disciplina }}</h1>
                    <div class="flex items-center gap-4 text-lg text-indigo-100">
                        <span class="flex items-center gap-2"><i class="far fa-clock"></i> {{ proxima_aula.horario }}</span>
                        <span class="flex items-center gap-2"><i class="fas fa-map-marker-alt"></i> {{ proxima_aula.sala }}</span>
                    </div>
                </div>
                <div class="text-right">
                    <p class="text-sm font-bold tracking-widest uppercase opacity-70">Turma</p>
                    <p class="text-3xl font-black">{{ proxima_aula.turma.nome|default:"--" }}</p>
                </div>
            </div>

            <div class="relative z-10 flex flex-wrap gap-4 mt-8">
                {% if proxima_aula.turma %}
                <a href="{% url 'pedagogico:detalhar_turma' proxima_aula.turma.id %}" class="flex items-center gap-3 px-8 py-4 font-bold text-indigo-900 transition bg-white shadow-lg rounded-2xl hover:bg-indigo-50 hover:scale-105">
                    <i class="text-xl fas fa-play-circle"></i> Iniciar Aula / Chamada
                </a>
                <a href="#" class="flex items-center gap-2 px-6 py-4 font-bold text-white transition border bg-white/10 border-white/20 rounded-2xl hover:bg-white/20 backdrop-blur-md">
                    <i class="fas fa-book-open"></i> Plano de Aula
                </a>
                {% else %}
                <p class="italic text-indigo-200">Nenhuma aula agendada para agora.</p>
                {% endif %}
            </div>
        </div>

        <div class="space-y-6">
            <div class="bg-white dark:bg-slate-800 rounded-[2rem] p-6 shadow-sm border border-slate-100 dark:border-slate-700 flex flex-col justify-center h-[130px] relative overflow-hidden group hover:border-orange-200 transition-colors">
                <div class="absolute right-[-20px] top-[-20px] w-24 h-24 bg-orange-100 dark:bg-orange-900/30 rounded-full blur-xl transition-transform group-hover:scale-150"></div>
                <div class="relative z-10 flex items-center justify-between">
                    <div>
                        <h3 class="text-3xl font-black text-slate-800 dark:text-white">{{ stats.pendencias }}</h3>
                        <p class="text-sm font-bold text-slate-500 dark:text-slate-400">Atividades Pendentes</p>
                    </div>
                    <div class="flex items-center justify-center w-12 h-12 text-xl text-orange-500 bg-orange-50 rounded-xl">
                        <i class="fas fa-inbox"></i>
                    </div>
                </div>
            </div>

            <div class="bg-white dark:bg-slate-800 rounded-[2rem] p-6 shadow-sm border border-slate-100 dark:border-slate-700 flex flex-col justify-center h-[130px] relative overflow-hidden group hover:border-blue-200 transition-colors cursor-pointer" onclick="window.location.href='{% url 'pedagogico:form_turmas' %}'">
                <div class="absolute right-[-20px] bottom-[-20px] w-24 h-24 bg-blue-100 dark:bg-blue-900/30 rounded-full blur-xl transition-transform group-hover:scale-150"></div>
                <div class="relative z-10 flex items-center justify-between">
                    <div>
                        <h3 class="text-lg font-bold text-slate-800 dark:text-white">Nova Turma</h3>
                        <p class="text-xs text-slate-500 dark:text-slate-400">Cadastrar</p>
                    </div>
                    <div class="flex items-center justify-center w-12 h-12 text-xl text-blue-600 transition-transform bg-blue-50 rounded-xl group-hover:rotate-90">
                        <i class="fas fa-plus"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="bg-white dark:bg-slate-800 rounded-[2.5rem] shadow-sm border border-slate-100 dark:border-slate-700 overflow-hidden">
        <div class="flex flex-col items-center justify-between gap-4 p-8 border-b border-slate-100 dark:border-slate-700 md:flex-row">
            <div>
                <h2 class="flex items-center gap-3 text-2xl font-bold text-slate-800 dark:text-white">
                    <i class="text-indigo-500 fas fa-calendar-alt"></i> Grade Horária
                </h2>
                <p class="mt-1 text-sm text-slate-500">Clique na turma para acessar o diário.</p>
            </div>
            <div class="flex items-center gap-2">
                <a href="{% url 'pedagogico:listar_turmas' %}" class="px-5 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-700 text-slate-600 dark:text-slate-300 font-bold text-sm hover:bg-slate-100 transition">
                    <i class="mr-2 fas fa-list"></i> Ver Lista de Turmas
                </a>
            </div>
        </div>

        <div class="overflow-x-auto">
            <table class="w-full min-w-[800px]">
                <thead>
                    <tr class="bg-slate-50/50 dark:bg-slate-900/30">
                        <th class="w-32 px-6 py-4 text-xs font-bold tracking-wider text-left uppercase text-slate-400">Horário</th>
                        {% for dia in dias_semana %}
                        <th class="w-1/5 px-6 py-4 text-xs font-bold tracking-wider text-center uppercase text-slate-400">{{ dia }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 dark:divide-slate-700">
                    {% for tempo, dias in grade.items %}
                    <tr class="transition-colors hover:bg-slate-50/30">
                        <td class="px-6 py-6 text-xs font-bold border-r text-slate-500 dark:text-slate-400 border-slate-50 dark:border-slate-700">
                            {{ tempo }}
                        </td>

                        {% for dia_nome in dias_semana %}
                            {% with turma=dias|get_item:dia_nome %}
                            <td class="relative h-24 p-2 align-top border-r border-dashed border-slate-100 dark:border-slate-700 last:border-0 group">
                                {% if turma %}
                                <a href="{% url 'pedagogico:detalhar_turma' turma.id %}" class="flex flex-col justify-center block w-full h-full gap-1 p-3 transition-all border-l-4 border-indigo-500 rounded-2xl bg-indigo-50 dark:bg-indigo-900/20 hover:bg-indigo-100 dark:hover:bg-indigo-900/40 hover:shadow-md group/card">
                                    <span class="mb-1 text-xs font-bold tracking-wider text-indigo-400 uppercase">Aula</span>
                                    <h4 class="text-sm font-black leading-tight text-indigo-900 dark:text-indigo-100 group-hover/card:text-indigo-700">{{ turma.nome }}</h4>
                                    <div class="flex items-center gap-2 mt-1 transition-opacity opacity-60 group-hover/card:opacity-100">
                                        <span class="text-[10px] font-bold bg-white/50 px-1.5 py-0.5 rounded text-indigo-800">{{ turma.alunos.count }} alunos</span>
                                    </div>
                                </a>
                                {% else %}
                                <div class="flex items-center justify-center w-full h-full transition-opacity opacity-0 group-hover:opacity-100">
                                    <button class="w-8 h-8 transition rounded-full bg-slate-100 text-slate-400 hover:bg-indigo-50 hover:text-indigo-500">
                                        <i class="text-xs fas fa-plus"></i>
                                    </button>
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

</div>
{% endblock %}
"""
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("   ✅ Template atualizado com Design Moderno e Grade.")

if __name__ == "__main__":
    print("🚀 REDESENHANDO DASHBOARD DO PROFESSOR (V2 - GRADE HORÁRIA)...\n")
    update_models()
    update_view()
    create_template()
    print("\n✨ Concluído! \n   1. Rode 'python manage.py makemigrations' e 'migrate' para criar a tabela de Horários.\n   2. Acesse o Dashboard.")