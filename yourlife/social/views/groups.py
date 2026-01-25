from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Grupo

@login_required
def groups_list(request):
    # Grupos que o usuário participa
    meus_grupos = request.user.grupos_participantes.all()
    # Todos os grupos (para explorar)
    todos_grupos = Grupo.objects.all().exclude(id__in=meus_grupos.values_list('id', flat=True))
    
    return render(request, 'social/groups/list.html', {
        'meus_grupos': meus_grupos,
        'todos_grupos': todos_grupos
    })

@login_required
def create_group(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        capa = request.FILES.get('capa')
        
        if nome:
            grupo = Grupo.objects.create(
                nome=nome,
                descricao=descricao,
                capa=capa
            )
            grupo.membros.add(request.user) # Criador é membro automático
            return redirect('yourlife_social:groups_list')
            
    return render(request, 'social/groups/create.html')

@login_required
def group_detail(request, group_id):
    grupo = get_object_or_404(Grupo, id=group_id)
    is_member = request.user in grupo.membros.all()
    
    if request.method == 'POST' and 'join' in request.POST:
        grupo.membros.add(request.user)
        return redirect('yourlife_social:group_detail', group_id=grupo.id)
        
    if request.method == 'POST' and 'leave' in request.POST:
        grupo.membros.remove(request.user)
        return redirect('yourlife_social:groups_list')

    return render(request, 'social/groups/detail.html', {
        'grupo': grupo,
        'is_member': is_member
    })
