from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def professor_dashboard(request):
    """ Dashboard Principal do Professor """
    context = {
        'user': request.user,
        'is_freemium': False, # Ajuste conforme sua lógica
    }
    return render(request, 'professor/dashboard/home.html', context)

@login_required
def corporate_dashboard(request):
    """ Dashboard Corporativo (Direção/Secretaria) """
    if request.user.role not in ['DIRECAO', 'SECRETARIA', 'COORDENACAO']:
        return HttpResponseForbidden("Acesso restrito à gestão escolar.")
    return render(request, 'professor/dashboard/corporate.html', {'user': request.user})

# --- Outras views que você possa ter (Exemplos adaptados para a nova estrutura) ---

@login_required
def gradebook_view(request):
    """ Lançamento de Notas """
    return render(request, 'professor/turmas/notas.html', {'user': request.user})

@login_required
def planning_view(request):
    """ Planejamento de Aulas """
    return render(request, 'professor/planejamento/meus_planos.html', {'user': request.user})

@login_required
def teacher_schedule(request):
    """ Grade Horária do Professor """
    # Se tiver lógica específica, adicione aqui
    return render(request, 'professor/teacher_schedule.html', {'user': request.user})
