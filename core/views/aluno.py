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
from financial.models import Transacao
from ..forms import CustomUserCreationForm, CustomAuthenticationForm
from ..models import CustomUser
from core.services.ai_client import AIClient

# ==============================================================================
# 4. PORTAL DO ALUNO (SUB-PÁGINAS NÃO PEDAGÓGICAS)
# ==============================================================================

@login_required
def aluno_dashboard(request):
    """ Dashboard Principal do Aluno (Feed Social) """
    if 'ALUNO' not in request.user.role:
        return redirect('core:dashboard')
    
    # Simulação: Recupera dados do aluno (substituir por query real)
    # Ex: aluno = request.user.aluno_profile
    # Mock para teste:
    aluno_mock = {
        'nivel_ensino': getattr(request.user, 'nivel_ensino', 'medio'), # infantil, fundamental, medio, superior, pos
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
    return render(request, 'core/aluno_dashboard_base.html', context)

@login_required
def student_id_card(request):
    """ Carteirinha Digital do Aluno (Visualização Full) """
    if 'ALUNO' not in request.user.role:
        return redirect('core:dashboard')
    
    is_premium = getattr(request.user, 'is_premium', False)
    
    context = {
        'user': request.user,
        'is_premium': is_premium,
        'aluno': getattr(request.user, 'aluno', {'nivel_ensino': 'medio', 'turma': {'nome': '3º A'}, 'serie': '3', 'matricula': request.user.id})
    }
    return render(request, 'aluno/student_id_card.html', context)

# --- Módulos Administrativos & Extras ---

@login_required
def student_financial(request):
    """ Financeiro do Aluno (Boletos) """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/financial.html', {'is_premium': is_premium})

@login_required
def student_services(request):
    """ Secretaria Virtual (Solicitações) """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/services.html', {'is_premium': is_premium})

@login_required
def daily_diary(request):
    """ Diário Infantil (Para Pais) """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/daily_diary.html', {'is_premium': is_premium})

@login_required
def gamification_store(request):
    """ NioStore - Loja de Gamificação """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/gamification_store.html', {'is_premium': is_premium})

@login_required
def talkio_view(request):
    """ Interface Full-Screen do Chat """
    context = {
        'user': request.user,
        'is_premium': getattr(request.user, 'is_premium', False)
    }
    return render(request, 'core/talkio.html', context)

# --- Premium e Perfil ---

@login_required
def student_premium(request):
    """ Página de Venda/Upgrade para Aluno Premium """
    # Se já for premium, redireciona para stats
    if getattr(request.user, 'is_premium', False):
        return redirect('core:student_premium_stats')
    return render(request, 'aluno/premium.html')

@login_required
def student_premium_stats(request):
    """ Painel de Analytics Premium (Acesso Restrito) """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/premium_stats.html', {'is_premium': is_premium})

@login_required
def student_profile(request):
    """ Perfil Gamificado do Aluno """
    is_premium = getattr(request.user, 'is_premium', False)
    return render(request, 'aluno/profile.html', {'is_premium': is_premium})
