from django.db import models
from django.utils import timezone
from decimal import Decimal
from core.models import School, CustomUser
from lumenios.pedagogico.models import Aluno
from django.conf import settings
import uuid

# ==============================================================================
# 1. GESTÃO DA ASSINATURA NIOCORTEX (SAAS BILLING)
# ==============================================================================

class PlanoSaaS(models.Model):
    """ Planos do próprio NioCortex (Ex: Free, Pro, Enterprise, Public Sector) """
    nome = models.CharField(max_length=50)
    preco_base = models.DecimalField(max_digits=10, decimal_places=2)
    limite_alunos = models.IntegerField(default=100)
    limite_armazenamento_gb = models.IntegerField(default=10)
    permite_gestao_publica = models.BooleanField(default=False) 

    def __str__(self):
        return self.nome

class AssinaturaEscola(models.Model):
    """ O contrato da Escola com o NioCortex """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    escola = models.OneToOneField(School, on_delete=models.CASCADE, related_name='assinatura')
    plano = models.ForeignKey(PlanoSaaS, on_delete=models.PROTECT)
    
    status = models.CharField(max_length=20, choices=[
        ('ATIVA', 'Ativa'),
        ('INADIMPLENTE', 'Inadimplente'),
        ('CANCELADA', 'Cancelada')
    ], default='ATIVA')
    
    data_proxima_cobranca = models.DateField()
    asaas_customer_id = models.CharField(max_length=50, blank=True, null=True)

# ==============================================================================
# 2. RECEITA ESCOLAR (MENSALIDADES / ALUNOS)
# ==============================================================================

class ContratoAluno(models.Model):
    """ Contrato financeiro entre Escola e Aluno """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE, related_name='contrato_financeiro')
    responsavel_financeiro = models.CharField(max_length=255)
    cpf_cnpj_responsavel = models.CharField(max_length=20)
    
    valor_mensalidade = models.DecimalField(max_digits=10, decimal_places=2)
    dia_vencimento = models.PositiveSmallIntegerField(default=10)
    ativo = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contrato {self.aluno.nome}"

class BoletoAluno(models.Model):
    """ Faturas geradas para os alunos """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    contrato = models.ForeignKey(ContratoAluno, on_delete=models.CASCADE, related_name='faturas')
    descricao = models.CharField(max_length=255, default="Mensalidade")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    vencimento = models.DateField()
    status = models.CharField(max_length=20, choices=[('PENDENTE', 'Pendente'), ('PAGO', 'Pago'), ('VENCIDO', 'Vencido')])
    
    link_pagamento = models.URLField(blank=True, null=True)
    asaas_payment_id = models.CharField(max_length=50, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Boleto {self.vencimento} - {self.contrato.aluno.nome}"

# ==============================================================================
# 3. COMPRAS, LICITAÇÕES E FORNECEDORES (GESTÃO PÚBLICA/PRIVADA)
# ==============================================================================

class Fornecedor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    razao_social = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20)
    categoria = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True)
    
    aprovado_licitacao = models.BooleanField(default=False, help_text="Fornecedor homologado em licitação?")

    def __str__(self):
        return self.razao_social

class Licitacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    numero_processo = models.CharField(max_length=50)
    modalidade = models.CharField(max_length=50)
    objeto = models.TextField(help_text="Descrição do que está sendo comprado")
    
    data_abertura = models.DateField()
    valor_total_estimado = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('ABERTA', 'Aberta'),
        ('EM_ANALISE', 'Em Análise'),
        ('HOMOLOGADA', 'Homologada'),
        ('DESERTA', 'Deserta/Fracassada')
    ])

    def __str__(self):
        return f"Licitação {self.numero_processo}"

class PedidoCompra(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    licitacao = models.ForeignKey(Licitacao, on_delete=models.SET_NULL, null=True, blank=True)
    
    descricao = models.CharField(max_length=255)
    data_pedido = models.DateField(default=timezone.now)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=[
        ('SOLICITADO', 'Solicitado'),
        ('APROVADO', 'Aprovado'),
        ('RECEBIDO', 'Recebido/Estoque'),
        ('PAGO', 'Pago')
    ], default='SOLICITADO')

    def __str__(self):
        return f"Pedido {self.descricao} - {self.fornecedor.razao_social}"

# ==============================================================================
# 4. PATRIMÔNIO (ATIVO IMOBILIZADO)
# ==============================================================================

class LocalizacaoPatrimonio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Patrimonio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    codigo_etiqueta = models.CharField(max_length=50, unique=True, help_text="Número da plaqueta")
    descricao = models.CharField(max_length=255)
    
    data_aquisicao = models.DateField()
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2)
    vida_util_anos = models.IntegerField(default=5)
    
    localizacao_atual = models.ForeignKey(LocalizacaoPatrimonio, on_delete=models.SET_NULL, null=True)
    compra_origem = models.ForeignKey(PedidoCompra, on_delete=models.SET_NULL, null=True, blank=True)
    
    estado_conservacao = models.CharField(max_length=20, choices=[
        ('NOVO', 'Novo'),
        ('BOM', 'Bom'),
        ('REGULAR', 'Regular'),
        ('DANIFICADO', 'Danificado'),
        ('BAIXADO', 'Baixado/Descartado')
    ], default='NOVO')

    def __str__(self):
        return f"#{self.codigo_etiqueta} - {self.descricao}"

    @property
    def valor_depreciado(self):
        hoje = timezone.now().date()
        if self.data_aquisicao > hoje:
            return self.valor_compra

        dias_de_uso = (hoje - self.data_aquisicao).days
        vida_util_dias = self.vida_util_anos * 365
        
        if dias_de_uso >= vida_util_dias:
            return Decimal('0.00')

        depreciacao_diaria = self.valor_compra / Decimal(vida_util_dias)
        valor_perdido = depreciacao_diaria * Decimal(dias_de_uso)
        valor_atual = self.valor_compra - valor_perdido
        return max(valor_atual.quantize(Decimal('0.01')), Decimal('0.00'))

class Transacao(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    nome_cliente = models.CharField(max_length=255)
    email_cliente = models.EmailField()
    cpf_cnpj = models.CharField(max_length=20, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    
    plano = models.CharField(max_length=100)
    ciclo = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    
    mercado_pago_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email_cliente} - {self.plano} - {self.status}"