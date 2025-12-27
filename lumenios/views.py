from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import SalaVirtual, Modulo, MaterialAula, ProgressoAluno
from pedagogical.models import Turma # Assumindo que existe relação Aluno <-> Turma

# ==============================================================================
# VISÃO DO ALUNO
# ==============================================================================

@login_required
def aluno_painel_cursos(request):
    """ Lista as disciplinas da turma do aluno """
    # Lógica simplificada: Pegar a turma do aluno logado
    # aluno_turma = request.user.aluno_profile.turma 
    # salas = SalaVirtual.objects.filter(turma=aluno_turma)
    
    # Mock para visualização inicial
    salas = SalaVirtual.objects.all() 
    return render(request, 'lumenios/aluno/painel_cursos.html', {'salas': salas})

@login_required
def aluno_player(request, sala_id):
    """ O Ambiente de Aula (Player estilo Udemy/Netflix) """
    sala = get_object_or_404(SalaVirtual, id=sala_id)
    modulos = sala.modulos.prefetch_related('materiais').all()
    
    # Calcular progresso
    total_materiais = MaterialAula.objects.filter(modulo__sala=sala).count()
    concluidos = ProgressoAluno.objects.filter(aluno=request.user, material__modulo__sala=sala, concluido=True).count()
    porcentagem = (concluidos / total_materiais * 100) if total_materiais > 0 else 0

    return render(request, 'lumenios/aluno/player.html', {
        'sala': sala,
        'modulos': modulos,
        'porcentagem': int(porcentagem)
    })

@login_required
def marcar_concluido(request, material_id):
    """ API para marcar aula como vista via AJAX """
    if request.method == 'POST':
        material = get_object_or_404(MaterialAula, id=material_id)
        ProgressoAluno.objects.update_or_create(
            aluno=request.user, material=material,
            defaults={'concluido': True}
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


# ==============================================================================
# VISÃO DO PROFESSOR
# ==============================================================================

@login_required
def professor_painel(request):
    """ Lista as turmas/disciplinas que o professor leciona """
    # salas = SalaVirtual.objects.filter(disciplina__professor=request.user)
    salas = SalaVirtual.objects.all() # Mock
    return render(request, 'lumenios/professor/dashboard.html', {'salas': salas})

@login_required
def professor_editor(request, sala_id):
    """ Interface para criar módulos e subir arquivos """
    sala = get_object_or_404(SalaVirtual, id=sala_id)
    return render(request, 'lumenios/professor/editor_curso.html', {'sala': sala})

@login_required
def criar_modulo(request, sala_id):
    if request.method == 'POST':
        sala = get_object_or_404(SalaVirtual, id=sala_id)
        Modulo.objects.create(sala=sala, titulo=request.POST.get('titulo'))
        return redirect('lumenios:professor_editor', sala_id=sala.id)

@login_required
def upload_material(request, modulo_id):
    if request.method == 'POST':
        modulo = get_object_or_404(Modulo, id=modulo_id)
        MaterialAula.objects.create(
            modulo=modulo,
            titulo=request.POST.get('titulo'),
            tipo=request.POST.get('tipo'),
            link_externo=request.POST.get('link'),
            arquivo=request.FILES.get('arquivo')
        )
        return redirect('lumenios:professor_editor', sala_id=modulo.sala.id)
