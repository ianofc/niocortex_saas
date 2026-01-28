from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def search_pinterest(request):
    return render(request, 'social/search/explore.html')

@login_required
def settings_view(request):
    return render(request, 'social/pages/settings.html')

@login_required
def settings_theme(request):
    return render(request, 'social/pages/themes.html')

@login_required
def settings_accessibility(request):
    return render(request, 'social/pages/accessibility.html')

@login_required
def support_view(request):
    return render(request, 'social/pages/support.html')
