# niocortex_saas/core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

# --- CONSTANTES DE ROLE (Funções/Ambientes) ---
ROLE_CHOICES = (
    ('ADMIN', 'Super Administrador (NioCortex)'),
    ('DIRECAO', 'Direção Escolar'),
    ('SECRETARIA', 'Secretaria Escolar'),
    ('COORDENACAO', 'Coordenação Pedagógica'),
    ('PROFESSOR_CORP', 'Professor (Ambiente Corporativo)'),
    ('PROFESSOR_FREE', 'Professor (Conta Individual Freemium)'),
    ('ALUNO_CORP', 'Aluno (Ambiente Corporativo)'),
    ('ALUNO_FREE', 'Aluno (Homeschooling/Autoestudo)'),
)

# --- CONSTANTES DE TENANT TYPE (Proprietário dos Dados) ---
TENANT_TYPE_CHOICES = (
    ('SCHOOL', 'Escola/Instituição'),
    ('INDIVIDUAL', 'Usuário Individual'),
)

class School(models.Model):
    """
    Representa o Tenant Corporativo (A Escola Pagante).
    """
    tenant_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    nome = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Escolas"
        
    def __str__(self):
        return self.nome

class CustomUser(AbstractUser):
    """
    Modelo de Usuário Personalizado (AUTH_USER_MODEL)
    Inclui as chaves de isolamento e as Roles para Multi-Tenancy.
    """
    # 🚨 CHAVE DE ISOLAMENTO DE DADOS (CRÍTICA)
    tenant_id = models.UUIDField(
        null=True, 
        blank=True, 
        db_index=True,
        help_text="UUID da Escola (Corporate) ou do próprio usuário (Individual)."
    )
    
    tenant_type = models.CharField(
        max_length=15, 
        choices=TENANT_TYPE_CHOICES, 
        default='INDIVIDUAL'
    )
    
    # 🚨 ROLE/FUNÇÃO (Define o Ambiente de Dashboard e Acesso)
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='PROFESSOR_FREE'
    )
    
    # Associação à Escola (apenas para usuários CORPORATE)
    school = models.ForeignKey(
        School, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    # Campos adicionais do antigo Cortex
    imagem_perfil = models.ImageField(upload_to='perfil_imgs/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Usuário NioCortex"
        verbose_name_plural = "Usuários NioCortex"

    def is_corporate_user(self):
        """ Conveniência para checar se o usuário está associado a uma escola pagante. """
        return self.tenant_type == 'SCHOOL' and self.school is not None
        
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
