# niocortex/pedagogical/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import JsonResponse

# Models e Forms
from .models import Turma, Aluno
from .forms import TurmaForm, AlunoForm

# Services
from .services import PedagogicalService
from core.services.ai_client import AIClient  # Cliente para o FastAPI (IA)

# ----------------------------------------------------------------------
# GESTÃO DE TURMAS
# ----------------------------------------------------------------------

@login_required
def listar_turmas_view(request):
    """ Exibe as turmas do professor (Free ou Corp) """
    try:
        # O Serviço blinda o acesso: só retorna dados do tenant atual
        turmas = PedagogicalService.list_turmas(request.user)
    except Exception as e:
        messages.error(request, f"Erro ao carregar turmas: {e}")
        turmas = []

    # ATENÇÃO: Nome do arquivo ajustado para o que está na sua pasta
    return render(request, 'pedagogical/turmas/listar_turmas.html', {'turmas': turmas})

@login_required
def criar_turma_view(request):
    """ Cria nova turma delegando validação de limites ao Serviço """
    if request.method == 'POST':
        form = TurmaForm(request.POST) 
        if form.is_valid():
            try:
                # O Serviço injeta o tenant_id e checa limites (ex: máx 5 turmas no Free)
                PedagogicalService.create_turma(request.user, form.cleaned_data)
                messages.success(request, "Turma criada com sucesso!")
                return redirect('pedagogical:listar_turmas')
            except ValidationError as e:
                # Captura erro de negócio (limite atingido)
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, "Erro inesperado ao criar turma.")
    else:
        form = TurmaForm()

    # ATENÇÃO: Nome do arquivo ajustado para 'form_turmas.html'
    return render(request, 'pedagogical/turmas/form_turmas.html', {
        'form': form,
        'titulo': 'Nova Turma',
        'btn_texto': 'Criar Turma'
    })

@login_required
def detalhe_turma(request, turma_id):
    """ Exibe o painel da turma (Dashboard da Turma) """
    try:
        # Busca segura via serviço
        turma = PedagogicalService.get_turma(request.user, turma_id)
        # Ordenação alfabética dos alunos
        alunos = turma.alunos.all().order_by('nome')
    except PermissionDenied:
        messages.error(request, "Você não tem permissão para acessar esta turma.")
        return redirect('pedagogical:listar_turmas')

    # ATENÇÃO: Nome do arquivo ajustado para 'detalhar_turmas.html'
    return render(request, 'pedagogical/turmas/detalhar_turmas.html', {'turma': turma, 'alunos': alunos})

@login_required
def editar_turma(request, turma_id):
    """ Edita dados básicos da turma """
    try:
        turma = PedagogicalService.get_turma(request.user, turma_id)
    except PermissionDenied:
        return redirect('pedagogical:listar_turmas')

    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save() # O tenant_id já existe, seguro salvar direto
            messages.success(request, "Turma atualizada com sucesso.")
            return redirect('pedagogical:detalhe_turma', turma_id=turma.id)
    else:
        form = TurmaForm(instance=turma)
    
    # Reutiliza 'form_turmas.html'
    return render(request, 'pedagogical/turmas/form_turmas.html', {
        'form': form, 
        'titulo': f'Editar {turma.nome}',
        'btn_texto': 'Salvar Alterações'
    })

@login_required
def excluir_turma(request, turma_id):
    """ Exclui turma e seus dados associados """
    try:
        turma = PedagogicalService.get_turma(request.user, turma_id)
    except PermissionDenied:
        return redirect('pedagogical:listar_turmas')

    if request.method == 'POST':
        turma.delete()
        messages.success(request, "Turma excluída permanentemente.")
        return redirect('pedagogical:listar_turmas')
    
    # ATENÇÃO: Nome do arquivo ajustado para 'exclusao_turmas.html'
    return render(request, 'pedagogical/turmas/exclusao_turmas.html', {'objeto': turma})

# ----------------------------------------------------------------------
# GESTÃO DE ALUNOS
# ----------------------------------------------------------------------

@login_required
def adicionar_aluno(request, turma_id):
    """ 
    Adiciona aluno delegando a regra de negócio (limite 20 alunos) ao Serviço.
    """
    try:
        turma = PedagogicalService.get_turma(request.user, turma_id)
    except PermissionDenied:
        messages.error(request, "Turma não encontrada.")
        return redirect('pedagogical:listar_turmas')

    if request.method == 'POST':
        # Passamos 'request.user' para o form filtrar apenas turmas desse professor
        form = AlunoForm(request.user, request.POST) 
        if form.is_valid():
            try:
                # O Serviço cuida do tenant_id e do limite do plano
                PedagogicalService.add_aluno(
                    request.user, 
                    turma_id, 
                    form.cleaned_data
                )
                messages.success(request, "Aluno matriculado com sucesso!")
                return redirect('pedagogical:detalhe_turma', turma_id=turma.id)
            
            except ValidationError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Erro ao matricular: {e}")
    else:
        # Pré-seleciona a turma no formulário
        form = AlunoForm(request.user, initial={'turma': turma})
    
    # ATENÇÃO: Nome do arquivo ajustado para 'form_alunos.html'
    return render(request, 'pedagogical/alunos/form_alunos.html', {
        'form': form, 
        'titulo': 'Novo Aluno',
        'subtitulo': f'Adicionando em: {turma.nome}'
    })

@login_required
def editar_aluno(request, aluno_id):
    """ Edita dados do aluno """
    # Busca manual por enquanto (TODO: mover para Service.get_aluno no futuro para centralizar)
    aluno = get_object_or_404(Aluno, id=aluno_id, tenant_id=request.user.tenant_id)
    turma_origem_id = aluno.turma.id

    if request.method == 'POST':
        form = AlunoForm(request.user, request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados do aluno atualizados.")
            return redirect('pedagogical:detalhe_turma', turma_id=turma_origem_id)
    else:
        form = AlunoForm(request.user, instance=aluno)
    
    # Reutiliza 'form_alunos.html'
    return render(request, 'pedagogical/alunos/form_alunos.html', {
        'form': form, 
        'titulo': f'Editar {aluno.nome}'
    })

@login_required
def excluir_aluno(request, aluno_id):
    """ Remove um aluno """
    aluno = get_object_or_404(Aluno, id=aluno_id, tenant_id=request.user.tenant_id)
    turma_id = aluno.turma.id

    if request.method == 'POST':
        aluno.delete()
        messages.success(request, "Aluno removido com sucesso.")
        return redirect('pedagogical:detalhe_turma', turma_id=turma_id)
    
    # ATENÇÃO: Nome do arquivo ajustado para 'exclusao_alunos.html'
    return render(request, 'pedagogical/alunos/exclusao_alunos.html', {
        'objeto': aluno,
        'voltar_para': turma_id
    })

# ----------------------------------------------------------------------
# API / IA (Integração com FastAPI)
# ----------------------------------------------------------------------

@login_required
def analisar_desempenho_aluno(request, aluno_id):
    """
    Endpoint AJAX para solicitar análise do aluno ao microsserviço de IA.
    Retorna JSON para ser consumido pelo frontend (Modal).
    """
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método não permitido"}, status=405)

    try:
        # 1. Busca segura do aluno
        aluno = get_object_or_404(Aluno, id=aluno_id, tenant_id=request.user.tenant_id)
        
        # 2. Prepara dados para o FastAPI (Simulação de métricas por enquanto)
        # Futuramente: Buscar do GradebookService
        dados_preparados = {
            "nome": aluno.nome,
            "turma": aluno.turma.nome if aluno.turma else "Sem Turma",
            "media": 7.5, # Placeholder: Calcular média real
            "frequencia": 88.0, # Placeholder: Calcular frequência real
            "notas": [7.0, 8.0], # Placeholder: Histórico recente
            "obs": ["Solicitação manual de análise via dashboard."]
        }

        # 3. Chama o Serviço de IA
        resultado_ia = AIClient.analisar_aluno(dados_preparados)

        if "error" in resultado_ia:
            return JsonResponse({"status": "error", "message": resultado_ia["error"]}, status=503)

        return JsonResponse({
            "status": "success",
            "data": resultado_ia
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)