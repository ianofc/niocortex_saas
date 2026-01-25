from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def global_premium(request):
    return render(request, 'social/premium.html')

@login_required
def explore(request):
    return render(request, 'social/explore.html')

@login_required
def notifications(request):
    return render(request, 'social/notifications.html')
