from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Notification

@login_required
def notifications(request):
    # Pega todas as notificações do usuário logado
    notifs = Notification.objects.filter(recipient=request.user)
    
    # Marca como lidas ao abrir a página
    notifs.update(is_read=True)
    
    return render(request, 'social/notifications/list.html', {'notifications': notifs})

@login_required
def global_premium(request):
    return render(request, 'social/premium/index.html')

@login_required
def search_pinterest(request):
    return render(request, 'social/explore/pinterest.html')

@login_required
def settings_support(request):
    return render(request, 'social/settings/support.html')

@login_required
def settings_theme(request):
    return render(request, 'social/settings/theme.html')

@login_required
def settings_support(request):
    return render(request, 'social/settings/support.html')

@login_required
def settings_theme(request):
    return render(request, 'social/settings/theme.html')
