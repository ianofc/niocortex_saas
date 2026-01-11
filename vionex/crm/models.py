from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class FunilEtapa(models.Model):
    """ Etapas do Pipeline de Vendas (Ex: Novo, Qualificado, Proposta, Fechado) """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    nome = models.CharField(max_length=50)
    ordem = models.PositiveIntegerField(default=0)
    cor = models.CharField(max_length=20, default="#3B82F6", help_text="Cor em Hex para o Kanban")

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return self.nome

class Lead(models.Model):
    """ Cadastro de Potenciais Clientes """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    nome = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    origem = models.CharField(max_length=50, choices=[
        ('SITE', 'Site/Landing Page'),
        ('INDICACAO', 'Indicação'),
        ('REDES_SOCIAIS', 'Redes Sociais'),
        ('OUTRO', 'Outro')
    ], default='SITE')
    
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='leads_responsaveis')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Oportunidade(models.Model):
    """ O Deal/Negócio em andamento """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    titulo = models.CharField(max_length=100, help_text="Ex: Matrícula 2 Filhos - João Silva")
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='oportunidades')
    etapa = models.ForeignKey(FunilEtapa, on_delete=models.PROTECT, related_name='oportunidades')
    
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    probabilidade = models.IntegerField(default=50, help_text="Probabilidade de fechamento em %")
    data_fechamento_prevista = models.DateField(null=True, blank=True)
    
    STATUS_CHOICES = [
        ('ABERTO', 'Em Aberto'),
        ('GANHO', 'Ganho (Matriculado)'),
        ('PERDIDO', 'Perdido'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.valor_estimado})"

class AtividadeCRM(models.Model):
    """ Log de interações (ligações, reuniões, emails) """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE, related_name='atividades')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    tipo = models.CharField(max_length=20, choices=[
        ('LIGACAO', 'Ligação'),
        ('WHATSAPP', 'WhatsApp'),
        ('REUNIAO', 'Reunião'),
        ('EMAIL', 'E-mail'),
        ('NOTA', 'Anotação Interna'),
    ])
    descricao = models.TextField()
    data_atividade = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-data_atividade']