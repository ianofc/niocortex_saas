# niocortex_saas/core/views.py

import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser
from core.services.ai_client import AIClient # Importação do Cérebro

# --- AUTENTICAÇÃO E REGISTRO ---

def register_view(request):
    """ 
    Registro Universal para Usuários Freemium (Professor ou Aluno).
    Ao registrar, o usuário ganha seu próprio tenant_id (Auto-Gestão).
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard') 
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Mensagem personalizada baseada no perfil
            role_msg = "Professor" if "PROFESSOR" in user.role else "Estudante"
            messages.success(request, f"Bem-vindo ao NioCortex! Seu ambiente de {role_msg} está pronto.")
            
            return redirect('core:dashboard') 
        else:
            messages.error(request, "Erro no registro. Verifique os dados abaixo.")
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    """ Login unificado para todos os perfis. """
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
        
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:login')

# --- ROUTER DE DASHBOARDS (O Cérebro da Navegação) ---

@login_required
def dashboard_router_view(request):
    """
    Direciona o usuário para a interface correta baseada em sua Role e Tipo de Tenant.
    """
    user = request.user
    role = user.role
    
    # 1. Super Admin (Infraestrutura)
    if role == 'ADMIN' or user.is_superuser:
        return redirect('admin:index') # Ou um dashboard customizado de métricas SaaS
        
    # 2. Gestão Escolar (Corporate)
    elif role in ['DIRECAO', 'SECRETARIA', 'COORDENACAO']:
        return redirect('core:corporate_dashboard')
        
    # 3. Professores (Corporate ou Free)
    elif 'PROFESSOR' in role:
        return redirect('core:professor_dashboard')
        
    # 4. Alunos (Corporate ou Free/Homeschooling)
    elif 'ALUNO' in role:
        return redirect('core:aluno_dashboard')
        
    # Fallback de Segurança
    messages.warning(request, "Perfil não identificado. Contate o suporte.")
    logout(request)
    return redirect('core:login')

# --- VIEWS DE DASHBOARD (COM CONTEXTO DE VIRALIDADE) ---

@login_required
def professor_dashboard(request):
    """ Dashboard do Professor (Híbrido: Pessoal ou Corporativo) """
    if 'PROFESSOR' not in request.user.role:
        return redirect('core:dashboard')
        
    context = {
        'user': request.user,
        'is_freemium': request.user.tenant_type == 'INDIVIDUAL',
        # Aqui futuramente carregaremos: turmas = TurmaService.get_turmas(request.user)
    }
    return render(request, 'core/professor_dashboard_base.html', context)

@login_required
def aluno_dashboard(request):
    """ Dashboard do Aluno (LPA - Personal Learning Assistant) """
    if 'ALUNO' not in request.user.role:
        return redirect('core:dashboard')
        
    context = {
        'user': request.user,
        'is_homeschooling': request.user.tenant_type == 'INDIVIDUAL',
        # Aqui futuramente carregaremos: plano_estudo = PedagogicalService.get_plano(request.user)
    }
    return render(request, 'core/aluno_dashboard_base.html', context)

@login_required
def corporate_dashboard(request):
    """ Visão da Gestão Escolar (Direção/Secretaria) """
    # Validação estrita
    if request.user.role not in ['DIRECAO', 'SECRETARIA', 'COORDENACAO']:
        return HttpResponseForbidden("Acesso restrito à gestão escolar.")
        
    return render(request, 'core/corporate_dashboard.html', {'user': request.user})

# --- INTEGRAÇÃO COM IO CONSCIOS (AJAX / API INTERNA) ---

@login_required
@require_POST
def api_check_conscios(request):
    """
    Endpoint chamado periodicamente pelo JS (widget flutuante) para ver se o Conscios quer falar.
    Essa view atua como Proxy seguro entre o Browser e o FastAPI.
    """
    try:
        data = json.loads(request.body)
        path = data.get('path', '/')
        
        # Aqui podemos injetar metadados reais do contexto do usuário
        # Ex: Se estiver na tela de notas, buscar a média da turma para o Conscios analisar
        meta = {} 
        
        # Chama o serviço de IA
        resultado = AIClient.check_proactive_thought(request.user, path, meta)
        
        return JsonResponse(resultado)
    except Exception as e:
        # Falha silenciosa para não quebrar a UX
        return JsonResponse({"should_speak": False, "error": str(e)})

@login_required
@require_POST
def api_chat_conscios(request):
    """
    Endpoint para interação direta via chat (Janela do Widget).
    """
    try:
        data = json.loads(request.body)
        mensagem = data.get('message', '')
        
        if not mensagem:
            return JsonResponse({'reply': 'Por favor, digite algo.'})

        resultado = AIClient.chat_universal(mensagem, request.user)
        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({'reply': 'Erro de conexão com o Conscios.'}, status=500)