from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Curso, Matricula, Conteudo
from .forms import CursoForm, ConteudoForm

# --- ÁREA DO ALUNO ---
@login_required
def dashboard_aluno(request):
    # Mostra cursos matriculados com barra de progresso (Estilo Estácio)
    matriculas = Matricula.objects.filter(aluno=request.user)
    return render(request, 'aluno/dashboard.html', {'matriculas': matriculas})

@login_required
def sala_de_aula(request, curso_id):
    # Interface estilo Udemy (Vídeo no centro, lista na lateral)
    curso = get_object_or_404(Curso, id=curso_id)
    # Aqui verificaríamos se o aluno está matriculado
    modulos = curso.modulos.all()
    return render(request, 'aluno/sala_de_aula.html', {'curso': curso, 'modulos': modulos})

# --- ÁREA DO PROFESSOR ---
@login_required
def dashboard_professor(request):
    if not request.user.is_professor:
        return redirect('dashboard_aluno')
    
    cursos = Curso.objects.filter(professor=request.user)
    return render(request, 'professor/dashboard.html', {'cursos': cursos})

@login_required
def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.professor = request.user
            curso.save()
            return redirect('dashboard_professor')
    else:
        form = CursoForm()
    return render(request, 'professor/criar_conteudo.html', {'form': form})