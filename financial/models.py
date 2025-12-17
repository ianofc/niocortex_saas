# niocortex/financial/models.py

from django.db import models
from django.utils import timezone
from decimal import Decimal
from core.models import School, CustomUser
from pedagogical.models import Aluno
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
    permite_gestao_publica = models.BooleanField(default=False) # Habilita licitações/patrimônio

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
    asaas_customer_id = models.CharField(max_length=50, blank=True, null=True) # ID no Gateway

# ==============================================================================
# 2. RECEITA ESCOLAR (MENSALIDADES / ALUNOS)
# ==============================================================================

class ContratoAluno(models.Model):
    """ Contrato financeiro entre Escola e Aluno """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True) # Isolamento
    
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
    
    link_pagamento = models.URLField(blank=True, null=True) # Link do Asaas/Boleto
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
    categoria = models.CharField(max_length=100) # Ex: Papelaria, Limpeza, TI
    telefone = models.CharField(max_length=20, blank=True)
    
    aprovado_licitacao = models.BooleanField(default=False, help_text="Fornecedor homologado em licitação?")

    def __str__(self):
        return self.razao_social

class Licitacao(models.Model):
    """ Processo Licitatório (Específico para Gestão Pública) """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    numero_processo = models.CharField(max_length=50)
    modalidade = models.CharField(max_length=50) # Pregão, Tomada de Preço, Dispensa
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
    """ Ordem de Compra (Almoxarifado/Material) """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    licitacao = models.ForeignKey(Licitacao, on_delete=models.SET_NULL, null=True, blank=True, help_text="Vincular a processo licitatório se houver")
    
    descricao = models.CharField(max_length=255)
    data_pedido = models.DateField(default=timezone.now)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=[
        ('SOLICITADO', 'Solicitado'),
        ('APROVADO', 'Aprovado'), # Direção aprovou
        ('RECEBIDO', 'Recebido/Estoque'),
        ('PAGO', 'Pago')
    ], default='SOLICITADO')

    def __str__(self):
        return f"Pedido {self.descricao} - {self.fornecedor.razao_social}"

# ==============================================================================
# 4. PATRIMÔNIO (ATIVO IMOBILIZADO)
# ==============================================================================

class LocalizacaoPatrimonio(models.Model):
    """ Salas, Laboratórios, Departamentos """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    nome = models.CharField(max_length=100) # Ex: Lab Informática 1

    def __str__(self):
        return self.nome

class Patrimonio(models.Model):
    """ O Bem em si (Cadeira, Computador, Projetor) """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    codigo_etiqueta = models.CharField(max_length=50, unique=True, help_text="Número da plaqueta")
    descricao = models.CharField(max_length=255)
    
    data_aquisicao = models.DateField()
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2)
    vida_util_anos = models.IntegerField(default=5, help_text="Para cálculo de depreciação (Ex: TI=5 anos, Móveis=10 anos)")
    
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
        """
        Calcula o valor contábil atual do bem usando Depreciação Linear.
        Fórmula: Valor Atual = Valor Compra - (Depreciação Acumulada)
        """
        hoje = timezone.now().date()
        
        # Se comprado no futuro (erro de cadastro), vale o preço de compra
        if self.data_aquisicao > hoje:
            return self.valor_compra

        # Cálculo em dias para precisão
        dias_de_uso = (hoje - self.data_aquisicao).days
        vida_util_dias = self.vida_util_anos * 365
        
        # Se já passou da vida útil, o valor contábil é zero (ou valor residual, aqui usamos zero)
        if dias_de_uso >= vida_util_dias:
            return Decimal('0.00')

        # Depreciação por dia
        depreciacao_diaria = self.valor_compra / Decimal(vida_util_dias)
        valor_perdido = depreciacao_diaria * Decimal(dias_de_uso)
        
        valor_atual = self.valor_compra - valor_perdido
        
        # Retorna o maior valor entre o calculado e zero (evita negativos por arredondamento)
        return max(valor_atual.quantize(Decimal('0.01')), Decimal('0.00'))