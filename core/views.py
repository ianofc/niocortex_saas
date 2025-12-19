# niocortex_saas/core/views.py

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
from financial.models import Transacao

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser
from core.services.ai_client import AIClient # Importação do Cérebro

# niocortex/core/views.py (Adicione estas funções)

def index(request):
    """ Landing Page (Aurora UI) """
    # Se o usuário já estiver logado, manda direto pro dashboard
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'public/landing_page.html')

def pricing(request):
    """ Página de Planos """
    return render(request, 'public/pricing.html')

def contact(request):
    """ Página de Contato """
    return render(request, 'public/contact.html')

def demo(request):
    """ Página de Demonstração Interativa """
    return render(request, 'public/demo.html')

# ... (Mantenha as outras views: login_view, register_view, dashboard, etc.) ...

# --- AUTENTICAÇÃO E REGISTRO ---

def register_view(request):
    """ 
    Registro Universal para Usuários Freemium (Professor ou Aluno).
    Ao registrar, o usuário ganha seu próprio tenant_id (Auto-Gestão).
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard') 
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Mensagem personalizada baseada no perfil
            role_msg = "Professor" if "PROFESSOR" in user.role else "Estudante"
            messages.success(request, f"Bem-vindo ao NioCortex! Seu ambiente de {role_msg} está pronto.")
            
            return redirect('core:dashboard') 
        else:
            messages.error(request, "Erro no registro. Verifique os dados abaixo.")
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    """ Login unificado para todos os perfis. """
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
        
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:login')

# --- ROUTER DE DASHBOARDS (O Cérebro da Navegação) ---

# niocortex/core/views.py

@login_required
def dashboard_router_view(request):
    """
    Direciona o usuário para a interface correta baseada em sua Role.
    """
    user = request.user
    role = user.role
    
    # 1. Super Admin (Infraestrutura)
    # CORREÇÃO: Removemos 'or user.is_superuser' para permitir que você teste as outras telas.
    # Agora, só vai para o admin se a ROLE for explicitamente 'ADMIN'.
    if role == 'ADMIN':
        return redirect('admin:index') 
        
    # 2. Gestão Escolar (Corporate)
    elif role in ['DIRECAO', 'SECRETARIA', 'COORDENACAO']:
        return redirect('core:corporate_dashboard')
        
    # 3. Professores (Corporate ou Free)
    elif 'PROFESSOR' in role: # Pega PROFESSOR_CORP e PROFESSOR_FREE
        return redirect('core:professor_dashboard')
        
    # 4. Alunos (Corporate ou Free)
    elif 'ALUNO' in role: # Pega ALUNO_CORP e ALUNO_FREE
        return redirect('core:aluno_dashboard')
        
    # Fallback
    messages.warning(request, "Perfil não identificado. Redirecionando para login.")
    logout(request)
    return redirect('core:login')

# --- VIEWS DE DASHBOARD (COM CONTEXTO DE VIRALIDADE) ---

@login_required
def professor_dashboard(request):
    """ Dashboard do Professor (Híbrido: Pessoal ou Corporativo) """
    if 'PROFESSOR' not in request.user.role:
        return redirect('core:dashboard')
        
    context = {
        'user': request.user,
        'is_freemium': request.user.tenant_type == 'INDIVIDUAL',
        # Aqui futuramente carregaremos: turmas = TurmaService.get_turmas(request.user)
    }
    return render(request, 'core/professor_dashboard_base.html', context)

@login_required
def aluno_dashboard(request):
    """ Dashboard do Aluno (LPA - Personal Learning Assistant) """
    if 'ALUNO' not in request.user.role:
        return redirect('core:dashboard')
        
    context = {
        'user': request.user,
        'is_homeschooling': request.user.tenant_type == 'INDIVIDUAL',
        # Aqui futuramente carregaremos: plano_estudo = PedagogicalService.get_plano(request.user)
    }
    return render(request, 'core/aluno_dashboard_base.html', context)

@login_required
def corporate_dashboard(request):
    """ Visão da Gestão Escolar (Direção/Secretaria) """
    # Validação estrita
    if request.user.role not in ['DIRECAO', 'SECRETARIA', 'COORDENACAO']:
        return HttpResponseForbidden("Acesso restrito à gestão escolar.")
        
    return render(request, 'core/corporate_dashboard.html', {'user': request.user})

# --- INTEGRAÇÃO COM IO CONSCIOS (AJAX / API INTERNA) ---

@login_required
@require_POST
def api_check_conscios(request):
    """
    Endpoint chamado periodicamente pelo JS (widget flutuante) para ver se o Conscios quer falar.
    Essa view atua como Proxy seguro entre o Browser e o FastAPI.
    """
    try:
        data = json.loads(request.body)
        path = data.get('path', '/')
        
        # Aqui podemos injetar metadados reais do contexto do usuário
        # Ex: Se estiver na tela de notas, buscar a média da turma para o Conscios analisar
        meta = {} 
        
        # Chama o serviço de IA
        resultado = AIClient.check_proactive_thought(request.user, path, meta)
        
        return JsonResponse(resultado)
    except Exception as e:
        # Falha silenciosa para não quebrar a UX
        return JsonResponse({"should_speak": False, "error": str(e)})

@login_required
@require_POST
def api_chat_conscios(request):
    """
    Endpoint para interação direta via chat (Janela do Widget).
    """
    try:
        data = json.loads(request.body)
        mensagem = data.get('message', '')
        
        if not mensagem:
            return JsonResponse({'reply': 'Por favor, digite algo.'})

        resultado = AIClient.chat_universal(mensagem, request.user)
        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({'reply': 'Erro de conexão com o Conscios.'}, status=500)

def checkout(request):
    """
    Página de Checkout.
    Recebe parâmetros via GET da página de preços.
    Ex: /checkout/?plano=Sinapse+Pro&ciclo=Mensal&price=29,90
    """
    # Captura os dados da URL ou define valores padrão caso acessem direto
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
    if request.method == 'POST':
        # 1. Capturar dados do formulário
        nome = request.POST.get('name')
        email = request.POST.get('email')
        doc = request.POST.get('document')
        phone = request.POST.get('phone')
        
        plano_nome = request.POST.get('plan_name')
        ciclo = request.POST.get('cycle')
        preco_str = request.POST.get('price', '0').replace('.', '').replace(',', '.') # Formata 29,90 para 29.90
        preco = float(preco_str)

        # 2. Criar registro no banco de dados (Status Pendente)
        transacao = Transacao.objects.create(
            nome_cliente=nome,
            email_cliente=email,
            cpf_cnpj=doc,
            telefone=phone,
            plano=plano_nome,
            ciclo=ciclo,
            valor=preco
        )

        # 3. Configurar SDK do Mercado Pago
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

        # 4. Criar Dados da Preferência
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
                    "number": ''.join(filter(str.isdigit, doc)) # Remove pontuação
                }
            },
            "back_urls": {
                # URLs para onde o usuário volta após pagar
                "success": request.build_absolute_uri('/checkout/sucesso/'),
                "failure": request.build_absolute_uri('/checkout/erro/'),
                "pending": request.build_absolute_uri('/checkout/pendente/')
            },
            "auto_return": "approved",
            "external_reference": str(transacao.id) # Linkamos o ID do nosso banco
        }

        # 5. Gerar Preferência
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        # 6. Atualizar transação com o ID do MP
        transacao.mercado_pago_id = preference['id']
        transacao.save()

        # 7. Redirecionar para o Checkout do Mercado Pago
        # O 'init_point' é a URL segura do MP
        return redirect(preference['init_point'])

    return redirect('core:pricing')

def checkout_sucesso(request):
    return render(request, 'public/sucesso.html')