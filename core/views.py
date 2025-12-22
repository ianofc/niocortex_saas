# niocortex/core/views.py

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
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser
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


# ==============================================================================
# 2. AUTENTICAÇÃO (AUTH)
# ==============================================================================

def register_view(request):
    """ Registro Universal """
    if request.user.is_authenticated:
        return redirect('core:dashboard') 
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            role_msg = "Professor" if "PROFESSOR" in user.role else "Estudante"
            messages.success(request, f"Bem-vindo ao NioCortex! Seu ambiente de {role_msg} está pronto.")
            return redirect('core:dashboard') 
        else:
            messages.error(request, "Erro no registro. Verifique os dados abaixo.")
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    """ Login Unificado """
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            return redirect('core:dashboard')
        else:
            messages.error(request, "Credenciais inválidas.")
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:login')


# ==============================================================================
# 3. DASHBOARDS (ÁREA LOGADA)
# ==============================================================================

@login_required
def dashboard_router_view(request):
    """ Redireciona para o dashboard correto com base na Role """
    user = request.user
    role = user.role
    
    if role == 'ADMIN':
        return redirect('admin:index') 
    elif role in ['DIRECAO', 'SECRETARIA', 'COORDENACAO']:
        return redirect('core:corporate_dashboard')
    elif 'PROFESSOR' in role:
        return redirect('core:professor_dashboard')
    elif 'ALUNO' in role:
        return redirect('core:aluno_dashboard')
        
    messages.warning(request, "Perfil não identificado. Redirecionando para login.")
    logout(request)
    return redirect('core:login')

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


# ==============================================================================
# 4. PORTAL DO ALUNO (SUB-PÁGINAS)
# ==============================================================================

@login_required
def aluno_dashboard(request):
    """ Dashboard Principal do Aluno (Feed Social) """
    if 'ALUNO' not in request.user.role:
        return redirect('core:dashboard')
    context = {
        'user': request.user,
        'is_homeschooling': request.user.tenant_type == 'INDIVIDUAL',
    }
    return render(request, 'core/aluno_dashboard_base.html', context)

@login_required
def student_profile(request):
    """ Perfil Gamificado do Aluno """
    return render(request, 'aluno/profile.html')

@login_required
def student_subjects(request):
    """ Lista de Disciplinas """
    return render(request, 'aluno/subjects.html')

@login_required
def student_grades(request):
    """ Boletim e Notas """
    return render(request, 'aluno/grades.html')

@login_required
def student_calendar(request):
    """ Agenda Escolar """
    return render(request, 'aluno/calendar.html')

@login_required
def student_files(request):
    """ Central de Arquivos """
    return render(request, 'aluno/files.html')

@login_required
def student_lesson(request):
    """ Sala de Aula Virtual (Player) """
    return render(request, 'aluno/lesson_viewer.html')

@login_required
def student_activity(request):
    """ Detalhe de Atividade / Entrega """
    return render(request, 'aluno/activity_detail.html')

@login_required
def student_financial(request):
    """ Financeiro do Aluno (Boletos) """
    return render(request, 'aluno/financial.html')

@login_required
def student_services(request):
    """ Secretaria Virtual (Solicitações) """
    return render(request, 'aluno/services.html')


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