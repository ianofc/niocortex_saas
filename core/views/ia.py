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
from finexio.models import Transacao
from ..forms import CustomUserCreationForm, CustomAuthenticationForm
from ..models import CustomUser
from core.services.ai_client import AIClient

# ==============================================================================
# 5. INTEGRAÇÃO IA (IO CONSCIOS)
# ==============================================================================

@login_required
@require_POST
def api_check_conscios(request):
    """ Verifica se a IA deve interagir proativamente """
    try:
        data = json.loads(request.body)
        path = data.get('path', '/')
        meta = {} 
        resultado = AIClient.check_proactive_thought(request.user, path, meta)
        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({"should_speak": False, "error": str(e)})

@login_required
@require_POST
def api_chat_conscios(request):
    """ Chat Universal com a IA """
    try:
        data = json.loads(request.body)
        mensagem = data.get('message', '')
        if not mensagem:
            return JsonResponse({'reply': 'Por favor, digite algo.'})
        resultado = AIClient.chat_universal(mensagem, request.user)
        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({'reply': 'Erro de conexão com o Conscios.'}, status=500)
