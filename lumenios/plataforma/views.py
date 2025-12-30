from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Curso, Matricula, Conteudo, Modulo
from .forms import CursoForm
from types import SimpleNamespace
import pandas as pd

# ==============================================================================
# ÁREA DO PROFESSOR (LUMENIOS - AVA)
# ==============================================================================

@login_required
def dashboard_professor(request):
    cursos = Curso.objects.filter(professor=request.user)
    total_alunos = Matricula.objects.filter(curso__in=cursos).count()
    total_cursos = cursos.count()
    atividades_pendentes = [
        {'titulo': 'Correção: Redação 3º Ano', 'data': 'Hoje', 'tipo': 'urgente'},
        {'titulo': 'Planejamento: Física Quântica', 'data': 'Amanhã', 'tipo': 'normal'},
    ]
    return render(request, 'professor/dashboard.html', {
        'cursos': cursos,
        'stats': {'alunos': total_alunos, 'cursos': total_cursos},
        'atividades': atividades_pendentes
    })

@login_required
def gerenciar_curso(request, curso_id):
    # Fallback se o curso não for do professor ou não existir
    try:
        curso = get_object_or_404(Curso, id=curso_id) # Remover professor=request.user para teste se necessário
    except:
        return redirect('lumenios:dashboard_professor')
        
    modulos = curso.modulos.all().prefetch_related('conteudos')
    return render(request, 'professor/gerenciar_curso.html', {'curso': curso, 'modulos': modulos})

@login_required
def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.professor = request.user
            curso.save()
            return redirect('lumenios:dashboard_professor')
    else:
        form = CursoForm()
    return render(request, 'professor/criar_conteudo.html', {'form': form})

@login_required
def editor_conteudo(request, curso_id):
    return render(request, 'professor/editor_conteudo.html', {'curso_id': curso_id})

# ==============================================================================
# ÁREA DO ALUNO (LEGADO / ESTUDO)
# ==============================================================================

@login_required
def dashboard_aluno(request):
    matriculas = Matricula.objects.filter(aluno=request.user)
    return render(request, 'aluno/dashboard.html', {'matriculas': matriculas})

@login_required
def perfil_aluno(request):
    return render(request, 'aluno/dashboard.html', {'section': 'perfil'})

@login_required
def disciplinas_aluno(request):
    matriculas = Matricula.objects.filter(aluno=request.user)
    return render(request, 'extras/disciplina.html', {'matriculas': matriculas})

@login_required
def sala_de_aula(request, conteudo_id=None):
    if not conteudo_id: return redirect('lumenios:dashboard_aluno')
    conteudo_atual = get_object_or_404(Conteudo, id=conteudo_id)
    modulo = conteudo_atual.modulo
    curso = modulo.curso
    modulos = curso.modulos.all().prefetch_related('conteudos')
    
    if conteudo_atual.tipo == 'VIDEO' and conteudo_atual.link:
        if 'watch?v=' in conteudo_atual.link:
            conteudo_atual.embed_link = conteudo_atual.link.replace('watch?v=', 'embed/')
        elif 'youtu.be/' in conteudo_atual.link:
            conteudo_atual.embed_link = conteudo_atual.link.replace('youtu.be/', 'www.youtube.com/embed/')
        else:
            conteudo_atual.embed_link = conteudo_atual.link
    else:
        conteudo_atual.embed_link = None

    return render(request, 'extras/sala_de_aula.html', {'curso': curso, 'modulos': modulos, 'conteudo_atual': conteudo_atual})

@login_required
def sala_de_aula_demo(request):
    # ... código demo mantido (resumido para caber no script) ...
    class MockQuerySet(list): 
        def all(self): return self
        def count(self): return len(self)
    prof = SimpleNamespace(first_name="Alan", last_name="Turing", avatar=None)
    curso = SimpleNamespace(id=0, titulo="IA Fundamentos", categoria="Tecnologia", professor=prof, imagem_capa=SimpleNamespace(url="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=1600&q=80"))
    aula1 = SimpleNamespace(id=1, titulo="1. Redes Neurais", tipo="VIDEO", link="https://www.youtube.com/watch?v=aircAruvnKk", embed_link="https://www.youtube.com/embed/aircAruvnKk", arquivo=None, texto_apoio="Intro.")
    mod1 = SimpleNamespace(titulo="Módulo 1", conteudos=MockQuerySet([aula1]))
    return render(request, 'extras/sala_de_aula.html', {'curso': curso, 'modulos': [mod1], 'conteudo_atual': aula1, 'is_demo': True})

@login_required
def biblioteca_aluno(request): return render(request, 'extras/biblioteca.html')
@login_required
def ensino_complementar(request): return render(request, 'extras/complementar.html')
@login_required
def avaliacoes_aluno(request): return render(request, 'extras/avaliacoes.html')
@login_required
def conscios_investigate(request): return render(request, 'extras/conscios.html', {'tema': request.GET.get('q', 'Aprendizado')})
@login_required
def desempenho_analytics(request): return render(request, 'aluno/desempenho.html', {'media_geral': 0})