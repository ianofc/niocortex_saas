from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt

@login_required
@xframe_options_exempt
def conscios_view(request):
    return render(request, 'social/components/conscios_widget.html')

@login_required
@xframe_options_exempt
def talkio_app(request):
    return render(request, 'social/talkio/index.html')

@login_required
def support_page(request):
    return render(request, 'social/pages/support.html')

@login_required
def settings_page(request):
    return render(request, 'social/pages/settings.html')

@login_required
def settings_support(request):
    return support_page(request)

@login_required
def settings_theme(request):
    return render(request, 'social/pages/themes.html')

@login_required
def settings_a11y(request):
    return render(request, 'social/pages/accessibility.html')
