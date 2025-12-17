# niocortex/financial/models.py

from django.db import models
from django.conf import settings
from pedagogical.models import Aluno
import uuid

class Contrato(models.Model):
    """
    Define a relação financeira entre a Escola e o Aluno/Responsável.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False) # Isolamento Multi-Tenancy
    
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE, related_name='contrato_financeiro')
    responsavel_nome = models.CharField(max_length=255)
    responsavel_cpf = models.CharField(max_length=14)
    responsavel_email = models.EmailField()
    
    valor_mensalidade = models.DecimalField(max_digits=10, decimal_places=2)
    dia_vencimento = models.PositiveSmallIntegerField(default=10)
    
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contrato - {self.aluno.nome}"

class Fatura(models.Model):
    """
    Representa uma cobrança específica (mensalidade, material, taxa).
    """
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False)
    
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='faturas')
    descricao = models.CharField(max_length=255) # Ex: "Mensalidade Março/2025"
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    data_pagamento = models.DateField(null=True, blank=True)
    
    link_boleto = models.URLField(null=True, blank=True) # Para integração futura (Asaas/Stripe)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descricao} - {self.contrato.aluno.nome}"

    @property
    def is_atrasado(self):
        from django.utils import timezone
        return self.status == 'PENDENTE' and self.data_vencimento < timezone.now().date()