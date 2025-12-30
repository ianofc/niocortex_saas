from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# --- GESTÃO DE ALUNOS ---
@login_required
def listar_alunos(request):
    return render(request, 'pedagogico/alunos/listar_alunos.html')

@login_required
def form_alunos(request):
    return render(request, 'pedagogico/alunos/form_alunos.html')

# --- GESTÃO DE TURMAS ---
@login_required
def listar_turmas(request):
    return render(request, 'pedagogico/turmas/listar_turmas.html')

@login_required
def detalhar_turma(request, turma_id):
    return render(request, 'pedagogico/turmas/detalhar_turmas.html')

# --- FERRAMENTAS PEDAGÓGICAS ---
@login_required
def gradebook(request):
    return render(request, 'pedagogico/gradebook/gradebook.html')

@login_required
def gerador_atividades(request):
    return render(request, 'pedagogico/ferramentas/gerador_atividades.html')

@login_required
def gerador_provas(request):
    return render(request, 'pedagogico/ferramentas/gerador_provas.html')
