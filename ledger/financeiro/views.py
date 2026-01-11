import mercadopago
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from .models import ContratoAluno, BoletoAluno, Fornecedor
from .forms import ContratoAlunoForm, GerarBoletoForm, FornecedorForm, PatrimonioForm
from .services import FinancialService, liberar_acesso_pos_pagamento

@csrf_exempt
def mercadopago_webhook(request):
    topic = request.GET.get('topic') or request.GET.get('type')
    resource_id = request.GET.get('id') or request.GET.get('data.id')

    if topic == 'payment':
        try:
            sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
            payment_info = sdk.payment().get(resource_id)
            payment = payment_info['response']
            transacao_id = payment.get('external_reference')
            status = payment.get('status')

            if status == 'approved' and transacao_id:
                liberar_acesso_pos_pagamento(transacao_id)
                    
        except Exception as e:
            print(f"Erro no webhook MP: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=200)

@login_required
def listar_patrimonio(request):
    relatorio = FinancialService.get_asset_report(request.user)
    return render(request, 'financeiro/patrimonio/listar_patrimonios.html', {
        'itens': relatorio['itens'],
        'total_investido': relatorio['total_investido'],
        'valor_atual': relatorio['valor_contabil_atual']
    })

@login_required
def novo_patrimonio(request):
    if request.method == 'POST':
        form = PatrimonioForm(request.POST)
        if form.is_valid():
            try:
                FinancialService.register_asset(request.user, form.cleaned_data)
                messages.success(request, "Bem patrimonial cadastrado com sucesso!")
                return redirect('ledger_financeiro:listar_patrimonio')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = PatrimonioForm()
        
    return render(request, 'financeiro/patrimonio/form_patrimonios.html', {
        'form': form, 'titulo': 'Tombamento de Património'
    })

@login_required
def listar_fornecedores(request):
    fornecedores = Fornecedor.objects.filter(tenant_id=request.user.tenant_id)
    return render(request, 'financeiro/compras/listar_fornecedores.html', {'fornecedores': fornecedores})

@login_required
def novo_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            try:
                FinancialService.register_supplier(request.user, form.cleaned_data)
                messages.success(request, "Fornecedor registado.")
                return redirect('ledger_financeiro:listar_fornecedores')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = FornecedorForm()

    return render(request, 'financeiro/compras/form_fornecedor.html', {
        'form': form, 'titulo': 'Novo Fornecedor'
    })

@login_required
def dashboard_financeiro(request):
    try:
        boletos = FinancialService.list_receivables(request.user)
        contratos = ContratoAluno.objects.filter(tenant_id=request.user.tenant_id)
        
        total_a_receber = sum(b.valor for b in boletos if b.status == 'PENDENTE')
        total_recebido = sum(b.valor for b in boletos if b.status == 'PAGO')
        inadimplencia = boletos.filter(status='VENCIDO').count()

        context = {
            'boletos_recentes': boletos[:5],
            'total_contratos': contratos.count(),
            'total_a_receber': total_a_receber,
            'total_recebido': total_recebido,
            'inadimplencia': inadimplencia
        }
        return render(request, 'financeiro/dashboard.html', context)
    except Exception as e:
        messages.error(request, f"Erro ao carregar dashboard: {str(e)}")
        return redirect('core:dashboard')

@login_required
def listar_contratos(request):
    contratos = FinancialService.list_contracts(request.user)
    return render(request, 'financeiro/contratos/listar_contratos.html', {'contratos': contratos})

@login_required
def criar_contrato(request):
    if request.method == 'POST':
        form = ContratoAlunoForm(request.user, request.POST)
        if form.is_valid():
            try:
                dados = form.cleaned_data
                aluno_id = dados['aluno'].id 
                FinancialService.create_student_contract(request.user, aluno_id, dados)
                messages.success(request, "Contrato criado com sucesso!")
                return redirect('ledger_financeiro:listar_contratos')
            except ValidationError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Erro inesperado: {e}")
    else:
        form = ContratoAlunoForm(request.user)
    
    return render(request, 'financeiro/contratos/forms_contratos.html', {
        'form': form, 'titulo': 'Novo Contrato de Aluno'
    })

@login_required
def listar_boletos(request):
    boletos = FinancialService.list_receivables(request.user)
    return render(request, 'financeiro/boletos/listar_boletos.html', {'boletos': boletos})

@login_required
def gerar_mensalidade_manual(request, contrato_id):
    try:
        FinancialService.generate_monthly_boletos(request.user, contrato_id)
        messages.success(request, "Mensalidade gerada com sucesso!")
    except Exception as e:
        messages.error(request, f"Erro ao gerar: {str(e)}")
    
    return redirect('ledger_financeiro:listar_boletos')

@login_required
def gerar_boleto_avulso(request, contrato_id):
    contrato = get_object_or_404(ContratoAluno, id=contrato_id, tenant_id=request.user.tenant_id)
    if request.method == 'POST':
        form = GerarBoletoForm(request.POST)
        if form.is_valid():
            try:
                FinancialService.create_custom_charge(
                    request.user, 
                    contrato_id,
                    descricao=form.cleaned_data['referencia'],
                    valor=form.cleaned_data['valor']
                )
                messages.success(request, "Cobrança avulsa gerada com sucesso!")
                return redirect('ledger_financeiro:listar_boletos')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = GerarBoletoForm()

    return render(request, 'financeiro/boletos/forms_boletos.html', {
        'form': form, 'contrato': contrato
    })

@login_required
def baixar_boleto(request, boleto_id):
    if request.method == 'POST':
        try:
            FinancialService.register_payment(request.user, boleto_id)
            messages.success(request, "Pagamento registrado com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao baixar: {str(e)}")
    return redirect('ledger_financeiro:listar_boletos')