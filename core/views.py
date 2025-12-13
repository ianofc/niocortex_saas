# niocortex_saas/core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, CustomAuthenticationForm

# --- VIEWS DE AUTENTICAÇÃO ---

def register_view(request):
    """ Lida com o registro freemium de Professor ou Aluno. """
    if request.user.is_authenticated:
        return redirect('core:dashboard') 
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bem-vindo(a) ao NioCortex, {user.username}. Sua conta freemium ({user.get_role_display()}) está pronta!")
            return redirect('core:dashboard') 
        else:
            messages.error(request, "Ocorreu um erro no registro. Por favor, corrija os erros.")
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    """ Lida com o login. """
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            messages.success(request, f"Login bem-sucedido. Olá, {user.username}!")
            return redirect('core:dashboard')
        else:
            messages.error(request, "Nome de usuário ou senha inválidos.")
            
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Sua sessão foi encerrada com sucesso.")
    return redirect('core:login')

# --- VIEW DE REDIRECIONAMENTO CENTRAL (O Router de Dashboards) ---

@login_required
def dashboard_router_view(request):
    """
    Função central que verifica a Role do usuário e o envia para o dashboard correto.
    """
    user = request.user
    role = user.role
    
    # 🚨 LÓGICA DE REDIRECIONAMENTO (As rotas devem estar mapeadas)
    if role == 'ADMIN':
        return redirect(reverse('admin:index'))
    elif role in ['DIRECAO', 'SECRETARIA', 'COORDENACAO']:
        return redirect('core:corporate_admin_dashboard')
    elif 'PROFESSOR' in role:
        return redirect('core:professor_dashboard')
    elif 'ALUNO' in role:
        return redirect('core:aluno_dashboard')
        
    # Fallback para qualquer usuário não mapeado
    messages.error(request, "Seu perfil de usuário não está configurado corretamente. Contate o suporte.")
    return redirect('core:logout')


# --- VIEWS DUMMY (Placeholders) ---

@login_required
def professor_dashboard(request):
    return render(request, 'core/professor_dashboard_base.html', {'user': request.user})

@login_required
def aluno_dashboard(request):
    return render(request, 'core/aluno_dashboard_base.html', {'user': request.user})

@login_required
def corporate_admin_dashboard(request):
    # Futuramente: lógica de permissão mais restrita aqui
    return render(request, 'core/corporate_admin_base.html', {'user': request.user})