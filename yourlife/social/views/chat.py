from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def talkio_view(request):
    # Lista de usuários para chat (exemplo: amigos)
    # Na prática, buscaria de Friendship
    contatos = User.objects.exclude(id=request.user.id)[:20]
    return render(request, 'social/talkio/index.html', {'contatos': contatos})
