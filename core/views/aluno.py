from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from yourlife.social.models import Post

@login_required
def aluno_dashboard(request):
    return render(request, 'social/dashboard_aluno/home.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Tenta importar os modelos necessários (ajuste conforme onde você definiu 'Matricula')
try:
    # Opção A: Se estiver usando o módulo Plataforma (LMS)
    from lumenios.plataforma.models import Matricula
except ImportError:
    Matricula = None

@login_required
def student_subjects(request):
    matriculas = []
    
    # Lógica para buscar as disciplinas/cursos do aluno
    if Matricula:
        # Busca matrículas onde o aluno é o usuário logado
        # Ajuste 'aluno' para 'usuario' se for o nome do campo no seu model
        try:
            matriculas = Matricula.objects.filter(aluno=request.user)
        except:
            pass
            
    # Se não tiver modelo de Matrícula ainda, mas tiver Pedagógico (Turma/Disciplina)
    # Podemos tentar montar uma lista fictícia baseada na Turma do aluno
    if not matriculas and hasattr(request.user, 'perfil_escolar'):
        aluno = request.user.perfil_escolar
        if aluno.turma:
            # Pega as disciplinas da turma e "finge" ser uma matrícula para o template
            for disciplina in aluno.turma.disciplinas.all():
                matriculas.append({
                    'curso': {
                        'titulo': disciplina.nome,
                        'professor': disciplina.professor
                    },
                    'progresso': 0 # Valor padrão
                })

    context = {
        'matriculas': matriculas
    }
    
    # [CORREÇÃO] Aponta para o arquivo que você criou em 'lumenios/templates/extras/'
    return render(request, 'extras/disciplina.html', context)

# --- Views Acadêmicas (Restauradas para evitar AttributeError) ---
@login_required
def student_subjects(request): return render(request, 'aluno/academico/disciplinas.html')
@login_required
def student_grades(request): return render(request, 'aluno/academico/boletim.html')
@login_required
def student_calendar(request): return render(request, 'aluno/calendar.html')
@login_required
def student_timetable(request): return render(request, 'aluno/academico/grade_horaria.html')
@login_required
def student_files(request): return render(request, 'aluno/academico/arquivos.html')
@login_required
def student_lesson(request): return render(request, 'extras/sala_de_aula.html') # A view que faltava!
@login_required
def student_activity(request): return render(request, 'aluno/academico/atividade.html')
@login_required
def student_financial(request): return render(request, 'aluno/administrativo/financeiro.html')
@login_required
def student_services(request): return render(request, 'aluno/administrativo/secretaria.html')
@login_required
def daily_diary(request): return render(request, 'aluno/extras/diario_infantil.html')
@login_required
def student_id_card(request): return render(request, 'core/ferramentas/carteirinha.html')
@login_required
def gamification_store(request): return render(request, 'aluno/extras/loja.html')
@login_required
def student_library(request): return render(request, 'aluno/extras/biblioteca.html')
@login_required
def career_center(request): return render(request, 'aluno/extras/carreira.html')
@login_required
def thesis_manager(request): return render(request, 'aluno/extras/tcc.html')
@login_required
def student_premium_stats(request): return render(request, 'aluno/premium/stats.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Tenta importar os modelos necessários
try:
    from lumenios.plataforma.models import Matricula
except ImportError:
    Matricula = None

# --- DASHBOARD ---
@login_required
def aluno_dashboard(request):
    # Aponta para o template do dashboard do aluno (Social ou Lumenios)
    return render(request, 'aluno/dashboard.html') 

# --- PERFIL (A função que faltava e causava o erro) ---
@login_required
def student_profile(request):
    # Renderiza o perfil do usuário logado (usando a estrutura social)
    return render(request, 'social/profile/profile_detail.html', {'profile_user': request.user})

# --- DISCIPLINAS (Versão com Lógica Completa) ---
@login_required
def student_subjects(request):
    matriculas = []
    
    # 1. Tenta buscar matrículas reais do módulo Plataforma
    if Matricula:
        try:
            matriculas = Matricula.objects.filter(aluno=request.user)
        except:
            pass
            
    # 2. Se não tiver matrícula, simula baseado na Turma (Pedagógico)
    if not matriculas and hasattr(request.user, 'perfil_escolar'):
        aluno_perfil = request.user.perfil_escolar
        if aluno_perfil and aluno_perfil.turma:
            # Pega as disciplinas da turma e estrutura para o template
            for disciplina in aluno_perfil.turma.disciplinas.all():
                matriculas.append({
                    'curso': {
                        'titulo': disciplina.nome,
                        'professor': disciplina.professor
                    },
                    'progresso': 0 # Valor padrão visual
                })

    context = {
        'matriculas': matriculas
    }
    
    # Aponta para o arquivo correto em 'lumenios/templates/extras/'
    return render(request, 'extras/disciplina.html', context)

# --- VIEWS SECUNDÁRIAS (Stubs) ---

@login_required
def student_grades(request): 
    return render(request, 'aluno/academico/boletim.html')

@login_required
def student_calendar(request): 
    return render(request, 'aluno/calendar.html')

@login_required
def student_timetable(request): 
    return render(request, 'aluno/academico/grade_horaria.html')

@login_required
def student_files(request): 
    return render(request, 'aluno/academico/arquivos.html')

@login_required
def student_lesson(request): 
    return render(request, 'extras/sala_de_aula.html') 

@login_required
def student_activity(request): 
    return render(request, 'aluno/academico/atividade.html')

@login_required
def student_financial(request): 
    return render(request, 'aluno/administrativo/financeiro.html')

@login_required
def student_services(request): 
    return render(request, 'aluno/administrativo/secretaria.html')

@login_required
def daily_diary(request): 
    return render(request, 'aluno/extras/diario_infantil.html')

@login_required
def student_id_card(request): 
    return render(request, 'core/ferramentas/carteirinha.html')

@login_required
def gamification_store(request): 
    return render(request, 'aluno/extras/loja.html')

@login_required
def student_library(request): 
    return render(request, 'aluno/extras/biblioteca.html')

@login_required
def career_center(request): 
    return render(request, 'aluno/extras/carreira.html')

@login_required
def thesis_manager(request): 
    return render(request, 'aluno/extras/tcc.html')

@login_required
def student_premium_stats(request): 
    return render(request, 'aluno/premium/stats.html')