from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Turma, Aluno
from .forms import TurmaForm, AlunoForm

@login_required
def lista_turmas(request):
    # O Manager 'for_tenant' garante que só vejo MINHAS turmas
    turmas = Turma.objects.for_tenant(request.user.tenant_id)
    return render(request, 'pedagogical/turmas/lista.html', {'turmas': turmas})

@login_required
def criar_turma(request):
    # Verifica limite do plano Free (Lógica de Negócio)
    if request.user.role == 'PROFESSOR_FREE':
        count = Turma.objects.for_tenant(request.user.tenant_id).count()
        if count >= 3: # Exemplo: Limite de 3 turmas no Free
            messages.error(request, "Limite de turmas atingido no plano Gratuito.")
            return redirect('pedagogical:lista_turmas')

    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save(commit=False)
            turma.tenant_id = request.user.tenant_id # 🚨 CRÍTICO
            turma.autor = request.user
            turma.save()
            messages.success(request, "Turma criada com sucesso!")
            return redirect('pedagogical:lista_turmas')
    else:
        form = TurmaForm()
    
    return render(request, 'pedagogical/turmas/form.html', {'form': form, 'titulo': 'Nova Turma'})

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
    pass # Implementação similar
@login_required
def excluir_aluno(request, aluno_id):
    pass # Implementação similar