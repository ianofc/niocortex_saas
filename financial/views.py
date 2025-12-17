# niocortex/financial/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError, PermissionDenied

# Models e Forms
from .models import ContratoAluno, BoletoAluno
from .forms import ContratoAlunoForm, GerarBoletoForm
from .services import FinancialService

from .models import Fornecedor, Patrimonio
from .forms import FornecedorForm, PatrimonioForm

# ----------------------------------------------------------------------
# GESTÃO DE PATRIMÓNIO E ALMOXARIFADO
# ----------------------------------------------------------------------

@login_required
def listar_patrimonio(request):
    """ 
    Relatório de Bens com cálculo de depreciação.
    Essencial para gestão pública e auditoria.
    """
    # Usa o serviço para obter os dados processados (Valor Atual Contabilístico)
    relatorio = FinancialService.get_asset_report(request.user)
    
    return render(request, 'financial/patrimonio/listar_patrimonios.html', {
        'itens': relatorio['itens'],
        'total_investido': relatorio['total_investido'],
        'valor_atual': relatorio['valor_contabil_atual']
    })

@login_required
def novo_patrimonio(request):
    """ Cadastro de Bens (Tombamento) """
    if request.method == 'POST':
        form = PatrimonioForm(request.POST)
        if form.is_valid():
            try:
                # Usa o Service para garantir integridade do tenant e validações
                FinancialService.register_asset(request.user, form.cleaned_data)
                messages.success(request, "Bem patrimonial cadastrado com sucesso!")
                return redirect('financial:listar_patrimonios')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = PatrimonioForm()
        
    return render(request, 'financial/patrimonio/form_patrimonios.html', {
        'form': form,
        'titulo': 'Tombamento de Património'
    })

@login_required
def listar_fornecedores(request):
    fornecedores = Fornecedor.objects.filter(tenant_id=request.user.tenant_id)
    return render(request, 'financial/compras/listar_fornecedores.html', {'fornecedores': fornecedores})

@login_required
def novo_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            try:
                FinancialService.register_supplier(request.user, form.cleaned_data)
                messages.success(request, "Fornecedor registado.")
                return redirect('financial:listar_fornecedores')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = FornecedorForm()

    return render(request, 'financial/compras/form_fornecedor.html', {
        'form': form,
        'titulo': 'Novo Fornecedor'
    })

# ----------------------------------------------------------------------
# DASHBOARD
# ----------------------------------------------------------------------

@login_required
def dashboard_financeiro(request):
    """ Visão geral das finanças (Contas a Receber) """
    try:
        # Busca dados via Service (já filtrado por tenant)
        boletos = FinancialService.list_receivables(request.user)
        contratos = ContratoAluno.objects.filter(tenant_id=request.user.tenant_id)
        
        # Métricas em memória (para MVP)
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
        return render(request, 'financial/dashboard.html', context)
    except Exception as e:
        messages.error(request, f"Erro ao carregar dashboard: {str(e)}")
        return redirect('core:dashboard')

# ----------------------------------------------------------------------
# CONTRATOS
# ----------------------------------------------------------------------

@login_required
def listar_contratos(request):
    """ Lista contratos ativos da escola """
    contratos = FinancialService.list_contracts(request.user)
    return render(request, 'financial/contratos/listar_contratos.html', {'contratos': contratos})

@login_required
def criar_contrato(request):
    """ Cria novo contrato financeiro """
    if request.method == 'POST':
        form = ContratoAlunoForm(request.user, request.POST)
        if form.is_valid():
            try:
                dados = form.cleaned_data
                aluno_id = dados['aluno'].id 
                
                FinancialService.create_student_contract(request.user, aluno_id, dados)
                messages.success(request, "Contrato criado com sucesso!")
                return redirect('financial:listar_contratos')
            except ValidationError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Erro inesperado: {e}")
    else:
        form = ContratoAlunoForm(request.user)
    
    return render(request, 'financial/contratos/forms_contratos.html', {
        'form': form,
        'titulo': 'Novo Contrato de Aluno'
    })

# ----------------------------------------------------------------------
# BOLETOS E COBRANÇAS
# ----------------------------------------------------------------------

@login_required
def listar_boletos(request):
    """ Lista histórico de cobranças """
    boletos = FinancialService.list_receivables(request.user)
    return render(request, 'financial/boletos/listar_boletos.html', {'boletos': boletos})

@login_required
def gerar_mensalidade_manual(request, contrato_id):
    """ 
    Ação: Gera a mensalidade padrão do próximo mês imediatamente.
    """
    try:
        FinancialService.generate_monthly_boletos(request.user, contrato_id)
        messages.success(request, "Mensalidade gerada com sucesso!")
    except Exception as e:
        messages.error(request, f"Erro ao gerar: {str(e)}")
    
    return redirect('financial:listar_boletos')

@login_required
def gerar_boleto_avulso(request, contrato_id):
    """ 
    Formulário: Cria cobrança extra (Material, Taxa, Uniforme).
    """
    # Busca segura para garantir que o contrato pertence ao tenant
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
                return redirect('financial:listar_boletos')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = GerarBoletoForm()

    return render(request, 'financial/boletos/forms_boletos.html', {
        'form': form,
        'contrato': contrato
    })

@login_required
def baixar_boleto(request, boleto_id):
    """ 
    Ação: Marca boleto como PAGO (Baixa Manual).
    Aceita apenas POST para evitar ações acidentais via link.
    """
    if request.method == 'POST':
        try:
            FinancialService.register_payment(request.user, boleto_id)
            messages.success(request, "Pagamento registrado com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao baixar: {str(e)}")
            
    return redirect('financial:listar_boletos')