# niocortex/financial/services.py

from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from decimal import Decimal  # <--- Faltava esta importação

# Importando os Modelos Corretos (Atualizados)
from .models import (
    ContratoAluno, 
    BoletoAluno, 
    Fornecedor, 
    PedidoCompra, 
    Patrimonio
)
from pedagogical.models import Aluno
from core.models import CustomUser

class FinancialService:
    """
    Controlador Financeiro Central.
    Garante isolamento de dados (Multi-Tenancy) para Receitas e Despesas.
    """

    @staticmethod
    def _get_active_tenant_id(user: CustomUser):
        """ Recupera o ID do tenant ativo para filtrar queries. """
        if user.tenant_id:
            return user.tenant_id
        raise PermissionDenied("Usuário sem Tenant ID definido.")

    # ==========================================================================
    # 1. RECEITA ESCOLAR (CONTRATOS E MENSALIDADES)
    # ==========================================================================

    @classmethod
    def create_student_contract(cls, user: CustomUser, aluno_id: int, data: dict) -> ContratoAluno:
        """ 
        Cria contrato financeiro para um aluno.
        Substitui o antigo 'create_contract'.
        """
        tenant_id = cls._get_active_tenant_id(user)
        
        # 1. Valida se o aluno pertence ao mesmo tenant
        try:
            aluno = Aluno.objects.get(id=aluno_id, tenant_id=tenant_id)
        except Aluno.DoesNotExist:
            raise ValidationError("Aluno não encontrado ou não pertence à sua organização.")

        # 2. Verificar se já existe contrato ativo
        if hasattr(aluno, 'contrato_financeiro') and aluno.contrato_financeiro.ativo:
            raise ValidationError(f"O aluno {aluno.nome} já possui um contrato ativo.")

        with transaction.atomic():
            contrato = ContratoAluno.objects.create(
                tenant_id=tenant_id,
                aluno=aluno,
                responsavel_financeiro=data.get('responsavel_financeiro'),
                cpf_cnpj_responsavel=data.get('cpf_cnpj_responsavel'),
                valor_mensalidade=data.get('valor_mensalidade'),
                dia_vencimento=data.get('dia_vencimento', 10),
                ativo=True
            )
            # Opcional: Gerar primeira fatura automaticamente aqui se desejar

        return contrato

    @classmethod
    def list_contracts(cls, user: CustomUser):
        """ Lista contratos do tenant (Usado na view listar_contratos) """
        tenant_id = cls._get_active_tenant_id(user)
        return ContratoAluno.objects.filter(tenant_id=tenant_id).select_related('aluno')

    @classmethod
    def list_receivables(cls, user: CustomUser):
        """ 
        Lista todos os boletos (antigo list_invoices).
        Usado no Dashboard e na lista de Boletos.
        """
        tenant_id = cls._get_active_tenant_id(user)
        return BoletoAluno.objects.filter(tenant_id=tenant_id).select_related('contrato__aluno').order_by('vencimento')

    @classmethod
    def generate_monthly_boletos(cls, user: CustomUser, contrato_id: str):
        """ 
        Gera a mensalidade padrão do próximo mês.
        Substitui o antigo 'generate_invoice'.
        """
        tenant_id = cls._get_active_tenant_id(user)
        
        try:
            contrato = ContratoAluno.objects.get(id=contrato_id, tenant_id=tenant_id)
        except ContratoAluno.DoesNotExist:
            raise PermissionDenied("Contrato não encontrado.")

        # Calcula vencimento (Ex: dia 10 do próximo mês)
        hoje = timezone.now().date()
        prox_mes = hoje + relativedelta(months=1)
        # Garante que o dia existe (ex: evita dia 31 em fevereiro)
        try:
            data_vencimento = prox_mes.replace(day=contrato.dia_vencimento)
        except ValueError:
            # Fallback para o último dia do mês se o dia configurado não existir
            from calendar import monthrange
            _, last_day = monthrange(prox_mes.year, prox_mes.month)
            data_vencimento = prox_mes.replace(day=last_day)

        boleto = BoletoAluno.objects.create(
            tenant_id=tenant_id,
            contrato=contrato,
            descricao=f"Mensalidade - {prox_mes.strftime('%m/%Y')}",
            valor=contrato.valor_mensalidade,
            vencimento=data_vencimento,
            status='PENDENTE'
        )
        return boleto

    @classmethod
    def create_custom_charge(cls, user: CustomUser, contrato_id: str, descricao: str, valor: Decimal):
        """ 
        Gera uma cobrança avulsa (Ex: Material, Uniforme).
        Usado na view 'gerar_boleto_avulso'.
        """
        tenant_id = cls._get_active_tenant_id(user)
        contrato = ContratoAluno.objects.get(id=contrato_id, tenant_id=tenant_id)
        
        # Vencimento padrão: 3 dias a partir de hoje
        vencimento = timezone.now().date() + timezone.timedelta(days=3)

        boleto = BoletoAluno.objects.create(
            tenant_id=tenant_id,
            contrato=contrato,
            descricao=descricao,
            # Se valor for None ou 0, usa mensalidade como fallback, mas o form obriga preencher ou lógica view
            valor=valor if valor else contrato.valor_mensalidade, 
            vencimento=vencimento,
            status='PENDENTE'
        )
        return boleto

    @classmethod
    def register_payment(cls, user: CustomUser, boleto_id: str):
        """ 
        Baixa manual de pagamento.
        Substitui o antigo 'registrar_pagamento'.
        """
        tenant_id = cls._get_active_tenant_id(user)
        try:
            boleto = BoletoAluno.objects.get(id=boleto_id, tenant_id=tenant_id)
            
            if boleto.status == 'PAGO':
                raise ValidationError("Este boleto já consta como pago.")
            
            boleto.status = 'PAGO'
            # boleto.data_pagamento = timezone.now().date() # Se adicionar este campo no model BoletoAluno depois
            boleto.save()
            return boleto
        except BoletoAluno.DoesNotExist:
            raise PermissionDenied("Boleto não encontrado.")

    # ==========================================================================
    # 2. GESTÃO DE COMPRAS E FORNECEDORES (Sem alterações, mantido para integridade)
    # ==========================================================================

    @classmethod
    def register_supplier(cls, user: CustomUser, data: dict) -> Fornecedor:
        tenant_id = cls._get_active_tenant_id(user)
        return Fornecedor.objects.create(tenant_id=tenant_id, **data)

    @classmethod
    def create_purchase_order(cls, user: CustomUser, dados_pedido: dict) -> PedidoCompra:
        tenant_id = cls._get_active_tenant_id(user)
        with transaction.atomic():
            pedido = PedidoCompra.objects.create(
                tenant_id=tenant_id,
                fornecedor_id=dados_pedido['fornecedor_id'],
                descricao=dados_pedido['descricao'],
                valor_total=dados_pedido['valor_total'],
                status='SOLICITADO'
            )
        return pedido

    # ==========================================================================
    # 3. GESTÃO DE PATRIMÔNIO (Sem alterações, mantido para integridade)
    # ==========================================================================

    @classmethod
    def register_asset(cls, user: CustomUser, data: dict) -> Patrimonio:
        tenant_id = cls._get_active_tenant_id(user)
        if Patrimonio.objects.filter(tenant_id=tenant_id, codigo_etiqueta=data['codigo_etiqueta']).exists():
            raise ValidationError("Já existe um bem com esta etiqueta patrimonial.")

        bem = Patrimonio.objects.create(
            tenant_id=tenant_id,
            codigo_etiqueta=data['codigo_etiqueta'],
            descricao=data['descricao'],
            data_aquisicao=data['data_aquisicao'],
            valor_compra=data['valor_compra'],
            vida_util_anos=data.get('vida_util_anos', 5),
            localizacao_atual_id=data.get('localizacao_id'),
            compra_origem_id=data.get('pedido_origem_id')
        )
        return bem

    @classmethod
    def get_asset_report(cls, user: CustomUser):
        tenant_id = cls._get_active_tenant_id(user)
        bens = Patrimonio.objects.filter(tenant_id=tenant_id).select_related('localizacao_atual')
        
        relatorio = []
        total_aquisicao = Decimal(0)
        total_atual = Decimal(0)

        for bem in bens:
            valor_atual = bem.valor_depreciado
            total_aquisicao += bem.valor_compra
            total_atual += valor_atual
            
            relatorio.append({
                'bem': bem,
                'valor_atual': valor_atual,
                'depreciacao_acumulada': bem.valor_compra - valor_atual
            })

        return {
            'itens': relatorio,
            'total_investido': total_aquisicao,
            'valor_contabil_atual': total_atual
        }