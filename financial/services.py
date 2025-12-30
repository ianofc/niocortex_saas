# niocortex/financial/services.py

from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Importando Modelos
from .models import (
    ContratoAluno, 
    BoletoAluno, 
    Fornecedor, 
    PedidoCompra, 
    Patrimonio,
    Transacao
)
from lumenios.pedagogico.models import Aluno
from core.models import CustomUser

# ==========================================================================
# 1. FUNÇÕES DE PAGAMENTO E WEBHOOK (Nível de Módulo)
#    Estas funções ficam fora da classe para facilitar o import nas views
# ==========================================================================

def enviar_email_boas_vindas(transacao):
    """ Envia o e-mail estilizado Aurora Lumina após compra aprovada. """
    assunto = 'Bem-vindo ao NioCortex! Seu acesso foi liberado 🚀'
    destinatario = [transacao.email_cliente]
    
    # Link para login (ajuste o domínio em produção)
    link_login = "https://niocortex.com.br/login" 

    contexto = {
        'nome_cliente': transacao.nome_cliente.split()[0],
        'plano': transacao.plano,
        'ciclo': transacao.ciclo,
        'valor': transacao.valor,
        'link_acesso': link_login
    }

    try:
        html_content = render_to_string('emails/compra_sucesso.html', contexto)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(assunto, text_content, settings.DEFAULT_FROM_EMAIL, destinatario)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print(f"Erro ao renderizar/enviar email: {e}")

def liberar_acesso_pos_pagamento(transacao_id):
    """
    Processa o webhook do Mercado Pago.
    Libera lóbulos e envia e-mail.
    """
    try:
        transacao = Transacao.objects.get(id=transacao_id)
        
        if transacao.status == 'approved':
            return "Já aprovado"

        transacao.status = 'approved'
        transacao.data_aprovacao = timezone.now()
        transacao.save()

        user = transacao.usuario
        # Tenta encontrar usuário pelo email se não estiver vinculado (compra deslogada)
        if not user:
            user = CustomUser.objects.filter(email=transacao.email_cliente).first()

        if user:
            plano = transacao.plano.lower()

            # Lógica de Liberação de Lóbulos
            if 'sinapse' in plano or 'neuronio' in plano:
                # Exemplo: Atualiza role ou flags de permissão
                # user.role = 'PROFESSOR_PREMIUM' 
                user.is_premium = True
                user.save()
                print(f"LÓBULOS PEDAGÓGICOS LIBERADOS PARA: {user.email}")

            elif 'córtex' in plano or 'lumina' in plano:
                # user.role = 'GESTOR_ESCOLA'
                user.is_premium = True
                print(f"SISTEMA NERVOSO INSTITUCIONAL ATIVADO PARA: {user.email}")

            # Enviar e-mail de boas-vindas
            try:
                enviar_email_boas_vindas(transacao)
                print(f"E-mail enviado para {transacao.email_cliente}")
            except Exception as e:
                print(f"Erro ao enviar email: {e}")

            return True
            
    except Transacao.DoesNotExist:
        return False
    except Exception as e:
        print(f"Erro genérico na liberação: {e}")
        return False


# ==========================================================================
# 2. CLASSE DE SERVIÇOS FINANCEIROS (CRUDs)
# ==========================================================================

class FinancialService:
    """
    Controlador Financeiro Central para operações do dia a dia.
    Gerencia Contratos, Boletos, Compras e Patrimônio.
    """

    @staticmethod
    def _get_active_tenant_id(user: CustomUser):
        """ Recupera o ID do tenant ativo para filtrar queries. """
        if user.tenant_id:
            return user.tenant_id
        raise PermissionDenied("Usuário sem Tenant ID definido.")

    # --- CONTRATOS E MENSALIDADES ---

    @classmethod
    def create_student_contract(cls, user: CustomUser, aluno_id: int, data: dict) -> ContratoAluno:
        tenant_id = cls._get_active_tenant_id(user)
        
        try:
            aluno = Aluno.objects.get(id=aluno_id, tenant_id=tenant_id)
        except Aluno.DoesNotExist:
            raise ValidationError("Aluno não encontrado ou não pertence à sua organização.")

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
        return contrato

    @classmethod
    def list_contracts(cls, user: CustomUser):
        tenant_id = cls._get_active_tenant_id(user)
        return ContratoAluno.objects.filter(tenant_id=tenant_id).select_related('aluno')

    @classmethod
    def list_receivables(cls, user: CustomUser):
        tenant_id = cls._get_active_tenant_id(user)
        return BoletoAluno.objects.filter(tenant_id=tenant_id).select_related('contrato__aluno').order_by('vencimento')

    @classmethod
    def generate_monthly_boletos(cls, user: CustomUser, contrato_id: str):
        tenant_id = cls._get_active_tenant_id(user)
        
        try:
            contrato = ContratoAluno.objects.get(id=contrato_id, tenant_id=tenant_id)
        except ContratoAluno.DoesNotExist:
            raise PermissionDenied("Contrato não encontrado.")

        hoje = timezone.now().date()
        prox_mes = hoje + relativedelta(months=1)
        
        try:
            data_vencimento = prox_mes.replace(day=contrato.dia_vencimento)
        except ValueError:
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
        tenant_id = cls._get_active_tenant_id(user)
        contrato = ContratoAluno.objects.get(id=contrato_id, tenant_id=tenant_id)
        vencimento = timezone.now().date() + timezone.timedelta(days=3)

        boleto = BoletoAluno.objects.create(
            tenant_id=tenant_id,
            contrato=contrato,
            descricao=descricao,
            valor=valor if valor else contrato.valor_mensalidade, 
            vencimento=vencimento,
            status='PENDENTE'
        )
        return boleto

    @classmethod
    def register_payment(cls, user: CustomUser, boleto_id: str):
        tenant_id = cls._get_active_tenant_id(user)
        try:
            boleto = BoletoAluno.objects.get(id=boleto_id, tenant_id=tenant_id)
            if boleto.status == 'PAGO':
                raise ValidationError("Este boleto já consta como pago.")
            
            boleto.status = 'PAGO'
            boleto.save()
            return boleto
        except BoletoAluno.DoesNotExist:
            raise PermissionDenied("Boleto não encontrado.")

    # --- GESTÃO DE COMPRAS E FORNECEDORES ---

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

    # --- GESTÃO DE PATRIMÔNIO ---

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