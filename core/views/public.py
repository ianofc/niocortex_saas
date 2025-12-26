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

# ==============================================================================
# 1. PÁGINAS PÚBLICAS (AURORA UI)
# ==============================================================================

def index(request):
    """ Landing Page Principal """
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'public/landing_page.html')

def about(request):
    """ Página Sobre Nós """
    return render(request, 'public/about.html')

def pricing(request):
    """ Página de Planos e Preços """
    return render(request, 'public/pricing.html')

def contact(request):
    """ Página de Contato """
    return render(request, 'public/contact.html')

def demo(request):
    """ Página de Demonstração Interativa """
    return render(request, 'public/demo.html')

# --- Landing Pages de Funcionalidades ---
def feature_financial(request):
    """ Feature: Módulo Financeiro """
    return render(request, 'public/financial_feature.html')

def feature_diary(request):
    """ Feature: Diário Digital """
    return render(request, 'public/digital_diary.html')

# --- Páginas Institucionais e Legais ---
def system_status(request):
    """ Status do Sistema """
    return render(request, 'public/system_status.html')

def help_center(request):
    """ Central de Ajuda """
    return render(request, 'public/help_center.html')

def privacy_policy(request):
    """ Política de Privacidade """
    return render(request, 'public/privacy_policy.html')

def terms_of_use(request):
    """ Termos de Uso """
    return render(request, 'public/terms_of_use.html')
