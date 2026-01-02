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

# ==============================================================================
# 2. AUTENTICAÇÃO (AUTH)
# ==============================================================================

def register_view(request):
    """ Registro Universal """
    if request.user.is_authenticated:
        return redirect('core:dashboard') 
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            role_msg = "Professor" if "PROFESSOR" in user.role else "Estudante"
            messages.success(request, f"Bem-vindo ao NioCortex! Seu ambiente de {role_msg} está pronto.")
            return redirect('core:dashboard') 
        else:
            messages.error(request, "Erro no registro. Verifique os dados abaixo.")
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    """ Login Unificado """
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            return redirect('core:dashboard')
        else:
            messages.error(request, "Credenciais inválidas.")
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:login')

# ==============================================================================
# 3. DASHBOARDS (ÁREA LOGADA)
# ==============================================================================

@login_required
def dashboard_router_view(request):
    """ Redireciona para o dashboard correto com base na Role """
    user = request.user
    role = user.role
    
    if role == 'ADMIN':
        return redirect('admin:index') 
    elif role in ['DIRECAO', 'SECRETARIA', 'COORDENACAO']:
        return redirect('core:corporate_dashboard')
    elif 'PROFESSOR' in role:
        return redirect('core:professor_dashboard')
    elif 'ALUNO' in role:
        return redirect('core:aluno_dashboard')
        
    messages.warning(request, "Perfil não identificado. Redirecionando para login.")
    logout(request)
    return redirect('core:login')
