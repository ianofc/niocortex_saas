import json
import mercadopago
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST

# Models e Forms
from financial.models import Transacao
from ..forms import CustomUserCreationForm, CustomAuthenticationForm
from ..models import CustomUser
from core.services.ai_client import AIClient

@login_required
def professor_dashboard(request):
    """ Dashboard do Professor """
    if 'PROFESSOR' not in request.user.role:
        return redirect('core:dashboard')
    context = {
        'user': request.user,
        'is_freemium': request.user.tenant_type == 'INDIVIDUAL',
    }
    return render(request, 'core/professor_dashboard_base.html', context)

@login_required
def corporate_dashboard(request):
    """ Dashboard Corporativo (Direção/Secretaria) """
    if request.user.role not in ['DIRECAO', 'SECRETARIA', 'COORDENACAO']:
        return HttpResponseForbidden("Acesso restrito à gestão escolar.")
    return render(request, 'core/corporate_dashboard.html', {'user': request.user})
