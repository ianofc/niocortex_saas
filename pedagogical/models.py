# niocortex_saas/pedagogical/models.py

from django.db import models
from django.conf import settings # 1. Importe settings em vez de CustomUser direto
from core.models import School
from uuid import uuid4

# --- MODEL MANAGERS ---

class TenantQuerySet(models.QuerySet):
    def for_tenant(self, tenant_id):
        return self.filter(tenant_id=tenant_id)

class TenantManager(models.Manager):
    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)

    def for_tenant(self, tenant_id):
        return self.get_queryset().for_tenant(tenant_id)

# --- MODELOS ---

class Turma(models.Model):
    # 🚨 CAMPOS DE ISOLAMENTO
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    nome = models.CharField(max_length=100)
    ano_letivo = models.IntegerField()
    
    # 2. Use settings.AUTH_USER_MODEL (referência string segura)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='turmas_criadas'
    )
    
    escola = models.ForeignKey(
        School, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    objects = TenantManager()

    class Meta:
        unique_together = ('tenant_id', 'nome', 'ano_letivo')
        verbose_name_plural = "Turmas"

    def __str__(self):
        return f"{self.nome} ({self.ano_letivo})"

class Aluno(models.Model):
    tenant_id = models.UUIDField(editable=False, db_index=True)

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='alunos')
    nome = models.CharField(max_length=200)
    data_nascimento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Feminino')], default='N/A')
    
    matricula_id = models.CharField(max_length=50, null=True, blank=True)
    
    objects = TenantManager()

    class Meta:
        unique_together = ('tenant_id', 'matricula_id')
        verbose_name_plural = "Alunos"
        
    def __str__(self):
        return self.nome