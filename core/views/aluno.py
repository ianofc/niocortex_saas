import json
import mercadopago
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST

# Models e Forms
from finexio.models import Transacao
from ..forms import CustomUserCreationForm, CustomAuthenticationForm
from ..models import CustomUser
from core.services.ai_client import AIClient
from lumenios.plataforma.models import Curso

# ==============================================================================
# 4. PORTAL DO ALUNO (SUB-PÁGINAS NÃO PEDAGÓGICAS)
# ==============================================================================

@login_required
def aluno_dashboard(request):
    """ Dashboard Principal do Aluno (Feed Social) """
    if 'ALUNO' not in request.user.role:
        return redirect('core:dashboard')
    
    # Mock de dados para evitar erro se o perfil não existir ainda
    aluno_mock = {
        'nivel_ensino': getattr(request.user, 'nivel_ensino', 'medio'),
        'turma': {'nome': '3º Ano A'},
        'nivel_xp': 5
    }
    
    is_premium = getattr(request.user, 'is_premium', False)

    context = {
        'user': request.user,
        'aluno': aluno_mock,
        'is_homeschooling': request.user.tenant_type == 'INDIVIDUAL',
        'is_premium': is_premium,
    }
    # CORREÇÃO: Aponta para a nova pasta 'aluno/dashboard/'
    return render(request, 'aluno/dashboard/home.html', context)

# --- Sub-páginas atualizadas ---

@login_required
def student_subjects(request):
    return render(request, 'aluno/academico/disciplinas.html')

@login_required
def student_grades(request):
    return render(request, 'aluno/academico/boletim.html')

@login_required
def student_calendar(request):
    return render(request, 'aluno/calendar.html') # Se não moveu para academico, mantenha aqui

@login_required
def student_files(request):
    return render(request, 'aluno/academico/arquivos.html')

@login_required
def student_timetable(request):
    return render(request, 'aluno/academico/grade_horaria.html')

@login_required
def student_lesson(request):
    # Pega o primeiro curso disponível só para não dar erro na tela de demonstração
    curso = Curso.objects.first() 
    modulos = curso.modulos.all() if curso else []
    
    return render(request, 'extras/sala_de_aula.html', {
    'curso': curso, 
    'modulos': modulos
})

@login_required
def student_financial(request):
    return render(request, 'aluno/administrativo/financeiro.html')

@login_required
def student_services(request):
    return render(request, 'aluno/administrativo/secretaria.html')

@login_required
def student_id_card(request):
    return render(request, 'aluno/administrativo/carteirinha.html')

# --- Módulos Extras ---
@login_required
def daily_diary(request):
    return render(request, 'aluno/extras/diario_infantil.html')

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

# --- Perfil e Premium ---
@login_required
def student_profile(request):
    return render(request, 'aluno/dashboard/perfil.html')

@login_required
def student_premium(request):
    if getattr(request.user, 'is_premium', False):
        return redirect('core:student_premium_stats')
    return render(request, 'aluno/premium/landing.html')

@login_required
def student_premium_stats(request):
    return render(request, 'aluno/premium/stats.html')

@login_required
def student_activity(request):
    return render(request, 'aluno/academico/atividade.html')
