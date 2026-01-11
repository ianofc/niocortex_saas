from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from yourlife.social.models import Post

@login_required
def aluno_dashboard(request):
    return render(request, 'social/dashboard_aluno/home.html')

@login_required
def student_profile(request):
    # Garante que o perfil exiba os posts do usuário
    posts = Post.objects.filter(autor=request.user).order_by('-data_criacao')
    return render(request, 'social/profile/profile_detail.html', {'profile_user': request.user, 'posts': posts})

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
