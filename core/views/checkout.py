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
# 6. CHECKOUT E PAGAMENTOS
# ==============================================================================

def checkout(request):
    """ Exibe o resumo do pedido antes de enviar para o Mercado Pago """
    plano = request.GET.get('plano', 'Córtex Essential')
    ciclo = request.GET.get('ciclo', 'Mensal')
    preco = request.GET.get('price', '199,00')

    context = {
        'plan_name': plano,
        'cycle': ciclo,
        'price': preco
    }
    return render(request, 'public/checkout.html', context)

def processar_pagamento(request):
    """
    Recebe os dados do formulário de checkout, cria a transação e
    redireciona para o checkout transparente do Mercado Pago.
    """
    if request.method == 'POST':
        # 1. Dados do Formulário
        nome = request.POST.get('name')
        email = request.POST.get('email')
        doc = request.POST.get('document')
        phone = request.POST.get('phone')
        
        plano_nome = request.POST.get('plan_name')
        ciclo = request.POST.get('cycle')
        preco_str = request.POST.get('price', '0').replace('.', '').replace(',', '.')
        try:
            preco = float(preco_str)
        except ValueError:
            preco = 0.0

        # 2. Configuração da BASE_URL
        host = getattr(settings, 'NGROK_URL', None)
        if not host:
            host = request.build_absolute_uri('/')[:-1]

        # 3. Criar Transação no Banco (Pendente)
        transacao = Transacao.objects.create(
            nome_cliente=nome,
            email_cliente=email,
            cpf_cnpj=doc,
            telefone=phone,
            plano=plano_nome,
            ciclo=ciclo,
            valor=preco
        )

        # 4. Criar Preferência no Mercado Pago
        try:
            sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
            
            webhook_path = '/financial/webhook/mercadopago/' 
            notification_url = f"{host}{webhook_path}"

            preference_data = {
                "items": [
                    {
                        "title": f"NioCortex - {plano_nome} ({ciclo})",
                        "quantity": 1,
                        "unit_price": preco,
                        "currency_id": "BRL"
                    }
                ],
                "payer": {
                    "name": nome,
                    "email": email,
                    "identification": {
                        "type": "CPF" if len(doc) <= 14 else "CNPJ",
                        "number": ''.join(filter(str.isdigit, doc))
                    }
                },
                "back_urls": {
                    "success": f"{host}/checkout/sucesso/",
                    "failure": f"{host}/checkout/erro/",
                    "pending": f"{host}/checkout/pendente/"
                },
                "notification_url": notification_url,
                "auto_return": "approved",
                "external_reference": str(transacao.id)
            }

            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]

            # VERIFICAÇÃO DE ERRO DO MERCADO PAGO
            if 'id' not in preference:
                print(f"ERRO MP: {preference_response}")
                error_msg = preference.get('message', 'Erro desconhecido no gateway de pagamento.')
                messages.error(request, f"Falha ao iniciar pagamento: {error_msg}")
                transacao.delete()
                return redirect('core:checkout')

            # 5. Salvar ID do MP e Redirecionar
            transacao.mercado_pago_id = preference['id']
            transacao.save()

            return redirect(preference['init_point']) 

        except Exception as e:
            print(f"EXCEPTION: {e}")
            messages.error(request, "Erro de conexão com o sistema de pagamento.")
            return redirect('core:checkout')

    return redirect('core:pricing')

def checkout_sucesso(request):
    """ Página de agradecimento após retorno do MP """
    return render(request, 'public/sucesso.html')
