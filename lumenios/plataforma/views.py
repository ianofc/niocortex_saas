from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Curso, Matricula, Conteudo
from .forms import CursoForm, ConteudoForm
from types import SimpleNamespace

import pandas as pd
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

# --- ÁREA DO ALUNO ---
@login_required
def dashboard_aluno(request):
    # Mostra cursos matriculados com barra de progresso (Estilo Estácio)
    matriculas = Matricula.objects.filter(aluno=request.user)
    return render(request, 'aluno/dashboard.html', {'matriculas': matriculas})

def sala_de_aula(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    modulos = curso.modulos.all().prefetch_related('conteudos')
    
    # Lógica para pegar a aula clicada ou a primeira disponível
    aula_id = request.GET.get('aula')
    conteudo_atual = None
    
    if aula_id:
        conteudo_atual = Conteudo.objects.filter(id=aula_id).first()
    
    # Se não tiver aula selecionada, tenta pegar a primeira do primeiro módulo
    if not conteudo_atual and modulos.exists():
        primeiro_modulo = modulos.first()
        conteudo_atual = primeiro_modulo.conteudos.first()

    return render(request, 'lumenios/templates/aluno/sala_de_aula.html', {
        'curso': curso,
        'modulos': modulos,
        'conteudo_atual': conteudo_atual
    })


# --- ÁREA DO PROFESSOR ---
@login_required
def dashboard_professor(request):
    # Verificação temporária simplificada (ou use a lógica do seu sistema atual)
    # Se seu sistema usa request.user.is_staff ou um grupo específico, ajuste aqui.
    if not request.user.is_authenticated: 
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


@login_required
def biblioteca_aluno(request):
    # Aqui futuramente você pode carregar livros do banco de dados
    return render(request, 'extras/biblioteca.html')

@login_required
def listar_disciplinas(request):
    # Aqui carregamos todas as disciplinas do aluno
    matriculas = Matricula.objects.filter(aluno=request.user)
    return render(request, 'extras/disciplina.html', {'matriculas': matriculas})


@login_required
def conscios_investigate(request):
    # Pega o termo da URL (ex: ?q=Logaritmo)
    tema = request.GET.get('q', 'Aprendizado') 
    return render(request, 'extras/conscios.html', {'tema': tema})

@login_required
def sala_de_aula_demo(request):
    """ View para testar o layout da sala de aula sem precisar de banco de dados """
    
    # Simula um QuerySet para o template (que chama .all())
    class MockQuerySet(list):
        def all(self): return self
        def count(self): return len(self)

    # 1. Professor Fake
    prof = SimpleNamespace(first_name="Alan", last_name="Turing", avatar=None)
    
    # 2. Curso Fake
    curso = SimpleNamespace(
        id=0,
        titulo="Inteligência Artificial: Fundamentos",
        categoria="Tecnologia",
        professor=prof,
        criado_em="2025-01-01",
        get_categoria_display="Tecnologia",
        imagem_capa=SimpleNamespace(url="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=1600&q=80")
    )
    
    # 3. Aulas Fake
    aula1 = SimpleNamespace(
        id=1, 
        titulo="O que são Redes Neurais?", 
        tipo="VIDEO", 
        link="https://www.youtube.com/watch?v=aircAruvnKk", # Vídeo Demo
        arquivo=None, 
        texto_apoio="Nesta aula aprenderemos os conceitos base."
    )
    aula2 = SimpleNamespace(
        id=2, 
        titulo="Material de Apoio PDF", 
        tipo="PDF", 
        link=None, 
        arquivo=SimpleNamespace(url="#"), 
        texto_apoio="Leitura obrigatória."
    )
    
    # 4. Módulos Fake
    mod1 = SimpleNamespace(titulo="Módulo 1: Introdução", conteudos=MockQuerySet([aula1]))
    mod2 = SimpleNamespace(titulo="Módulo 2: Aprofundamento", conteudos=MockQuerySet([aula2]))
    
    modulos = [mod1, mod2]
    
    # Renderiza o template normal com dados falsos
    return render(request, 'extras/sala_de_aula.html', {
        'curso': curso,
        'modulos': modulos,
        'conteudo_atual': aula1, # Já começa na aula 1
        'is_demo': True
    })

@login_required
def ensino_complementar(request):
    # Futuramente, você pode filtrar Matriculas onde o curso.tipo == 'COMPLEMENTAR'
    # Por enquanto, renderiza o template estático/demo
    return render(request, 'extras/complementar.html')

@login_required
def avaliacoes_aluno(request):
    # Futuramente: Buscar Avaliacao.objects.filter(turma__alunos=request.user)
    # Por enquanto, renderiza o template com dados estáticos
    return render(request, 'extras/avaliacoes.html')

import pandas as pd
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def desempenho_analytics(request):
    # 1. Simulação de Dados (No futuro, virá de Avaliacao.objects.filter(...))
    dados_mock = [
        {'disciplina': 'Matemática', 'atividade': 'Prova 1', 'nota': 7.5, 'peso': 1, 'data': '2025-02-10'},
        {'disciplina': 'Matemática', 'atividade': 'Trabalho', 'nota': 9.0, 'peso': 0.5, 'data': '2025-02-25'},
        {'disciplina': 'Matemática', 'atividade': 'Prova 2', 'nota': 8.0, 'peso': 1, 'data': '2025-03-15'},
        {'disciplina': 'Física', 'atividade': 'Prova 1', 'nota': 6.0, 'peso': 1, 'data': '2025-02-12'},
        {'disciplina': 'Física', 'atividade': 'Relatório', 'nota': 8.5, 'peso': 0.5, 'data': '2025-03-01'},
        {'disciplina': 'História', 'atividade': 'Seminário', 'nota': 10.0, 'peso': 1, 'data': '2025-02-20'},
        {'disciplina': 'Química', 'atividade': 'Prova 1', 'nota': 5.5, 'peso': 1, 'data': '2025-02-15'},
        {'disciplina': 'Química', 'atividade': 'Recuperação', 'nota': 7.0, 'peso': 1, 'data': '2025-03-10'},
    ]

    # 2. Criação do DataFrame
    df = pd.DataFrame(dados_mock)

    # 3. Análises com Pandas
    if not df.empty:
        # Média Ponderada Global (Simplificada para média aritmética aqui para demo)
        media_geral = df['nota'].mean()
        
        # Média por Disciplina
        medias_por_materia = df.groupby('disciplina')['nota'].mean().round(1).to_dict()
        
        # Melhor e Pior Desempenho
        melhor_materia = max(medias_por_materia, key=medias_por_materia.get)
        pior_materia = min(medias_por_materia, key=medias_por_materia.get)
        
        # Tendência (Últimas 3 notas)
        ultimas_notas = df.sort_values('data', ascending=False).head(5).to_dict('records')
        
        # Quantidade de Avaliações
        total_avaliacoes = len(df)
        
        # Status (Aprovado/Atenção) baseado na média 7.0
        status_materias = {k: ('Aprovado' if v >= 7 else 'Atenção') for k, v in medias_por_materia.items()}
        
    else:
        media_geral = 0
        medias_por_materia = {}
        ultimas_notas = []
        status_materias = {}

    context = {
        'media_geral': round(media_geral, 1),
        'medias_materia': medias_por_materia, # Dicionário {'Matemática': 8.2, ...}
        'historico': ultimas_notas,
        'melhor_materia': melhor_materia,
        'pior_materia': pior_materia,
        'total': total_avaliacoes,
        'status': status_materias
    }

    return render(request, 'aluno/desempenho.html', context)