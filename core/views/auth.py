from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# NOTA: As views de Login, Registro e Logout foram movidas para 'social.views'
# pois a autenticação agora pertence ao módulo social.

@login_required
def dashboard_router_view(request):
    """
    Roteador Central (acessado via /core/app/).
    
    Lógica:
    1. Superusuários/Staff -> Admin do Django (para manutenção).
    2. TODOS os outros (Diretor, Professor, Aluno) -> Feed Social (YourLife).
       O perfil social é a porta de entrada e identidade do usuário no sistema.
    """
    
    # Manutenção / Admin Técnico
    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin:index')
    
    # Direção, Coordenação, Professores e Alunos
    # Todos convergem para a experiência social primeiro.
    return redirect('yourlife_social:home')