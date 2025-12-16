from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Turma, Aluno
from .forms import TurmaForm, AlunoForm
from django.contrib.auth.decorators import login_required
from .services import PedagogicalService

@login_required
def listar_turmas_view(request):
    """ Exibe as turmas do professor (Free ou Corp) """
    try:
        # O Serviço decide quais turmas mostrar baseado no usuário
        turmas = PedagogicalService.list_turmas(request.user)
    except Exception as e:
        messages.error(request, f"Erro ao carregar turmas: {e}")
        turmas = []

    return render(request, 'pedagogical/listar_turmas.html', {'turmas': turmas})

@login_required
def criar_turma_view(request):
    """ Cria nova turma com validação de limites via Serviço """
    if request.method == 'POST':
        # Aqui usamos um Form do Django para validar os campos básicos (nome, ano)
        # Supondo que você tenha criado um TurmaForm em forms.py
        form = TurmaForm(request.POST) 
        if form.is_valid():
            try:
                # O Serviço injeta o tenant_id e checa limites
                PedagogicalService.create_turma(request.user, form.cleaned_data)
                messages.success(request, "Turma criada com sucesso!")
                return redirect('pedagogical:listar_turmas')
            except Exception as e:
                # Captura erro de limite (ValidationError) do serviço
                messages.error(request, str(e))
    else:
        form = TurmaForm()

    return render(request, 'pedagogical/criar_turma.html', {'form': form})

@login_required
def detalhe_turma(request, turma_id):
    # get_object_or_404 respeitando o tenant
    turma = get_object_or_404(Turma, id=turma_id, tenant_id=request.user.tenant_id)
    alunos = turma.alunos.all()
    return render(request, 'pedagogical/turmas/detalhe.html', {'turma': turma, 'alunos': alunos})

@login_required
def editar_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id, tenant_id=request.user.tenant_id)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada.")
            return redirect('pedagogical:lista_turmas')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'pedagogical/turmas/form.html', {'form': form, 'titulo': f'Editar {turma.nome}'})

@login_required
def excluir_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id, tenant_id=request.user.tenant_id)
    if request.method == 'POST':
        turma.delete()
        messages.success(request, "Turma excluída.")
        return redirect('pedagogical:lista_turmas')
    return render(request, 'pedagogical/turmas/confirmar_exclusao.html', {'objeto': turma})

# --- ALUNOS ---

@login_required
def adicionar_aluno(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id, tenant_id=request.user.tenant_id)
    
    # Limite de Alunos por Turma (Regra Freemium)
    if request.user.role == 'PROFESSOR_FREE' and turma.alunos.count() >= 20:
        messages.error(request, "Limite de 20 alunos por turma atingido no plano Gratuito.")
        return redirect('pedagogical:detalhe_turma', turma_id=turma.id)

    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.tenant_id = request.user.tenant_id # 🚨 CRÍTICO
            aluno.turma = turma
            aluno.save()
            messages.success(request, "Aluno matriculado.")
            return redirect('pedagogical:detalhe_turma', turma_id=turma.id)
    else:
        form = AlunoForm()
    
    return render(request, 'pedagogical/alunos/form.html', {'form': form, 'turma': turma})

# (Implementar editar_aluno e excluir_aluno seguindo a mesma lógica de tenant_id)
@login_required
def editar_aluno(request, aluno_id):
    # 1. Busca segura: Garante que o aluno pertence ao tenant do usuário logado
    aluno = get_object_or_404(Aluno, id=aluno_id, tenant_id=request.user.tenant_id)
    turma_id = aluno.turma.id  # Guardamos o ID para redirecionar depois

    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados do aluno atualizados com sucesso.")
            # Redireciona de volta para a lista de alunos daquela turma
            return redirect('pedagogical:detalhe_turma', turma_id=turma_id)
    else:
        form = AlunoForm(instance=aluno)
    
    # Reutilizamos o template de formulário de alunos
    return render(request, 'pedagogical/alunos/form.html', {
        'form': form, 
        'turma': aluno.turma, 
        'titulo': f'Editar {aluno.nome}'
    })

@login_required
def excluir_aluno(request, aluno_id):
    # 1. Busca segura: Garante que o aluno pertence ao tenant
    aluno = get_object_or_404(Aluno, id=aluno_id, tenant_id=request.user.tenant_id)
    turma_id = aluno.turma.id  # Guardamos o ID para redirecionar depois

    if request.method == 'POST':
        aluno.delete()
        messages.success(request, "Aluno removido com sucesso.")
        return redirect('pedagogical:detalhe_turma', turma_id=turma_id)
    
    # Renderiza uma página de confirmação antes de excluir
    return render(request, 'pedagogical/alunos/confirmar_exclusao.html', {
        'objeto': aluno,
        'voltar_para': turma_id  # Contexto útil para criar um botão "Cancelar" no template
    })