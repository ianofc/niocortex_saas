from django.db import models
from core.models import CustomUser
from lumenios.pedagogico.models import Aluno
import uuid

class ModeloDocumento(models.Model):
    """
    Templates de documentos (Ex: Declaração de Matrícula, Histórico Simples).
    Permite HTML para formatação rica (negrito, tabelas).
    """
    TIPO_CHOICES = [
        ('DECLARACAO', 'Declaração'),
        ('HISTORICO', 'Histórico Escolar'),
        ('CONTRATO', 'Contrato de Prestação de Serviços'),
        ('CERTIFICADO', 'Certificado / Diploma'),
        ('OUTRO', 'Outro'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='DECLARACAO')
    
    # O conteúdo aceita HTML e placeholders como {{ aluno.nome }}
    conteudo = models.TextField(help_text="Use {{ aluno.nome }}, {{ aluno.cpf }}, etc. para campos dinâmicos.")
    
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class DocumentoEmitido(models.Model):
    """
    Registo oficial de documentos gerados.
    Garante a imutabilidade e permite validação futura via QR Code/Link.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='documentos')
    modelo = models.ForeignKey(ModeloDocumento, on_delete=models.PROTECT)
    
    # Dados do momento da emissão (snapshot)
    conteudo_final = models.TextField(help_text="Conteúdo com as variáveis já substituídas")
    
    # Segurança
    codigo_validacao = models.CharField(max_length=50, unique=True, editable=False)
    emitido_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    data_emissao = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.codigo_validacao:
            # Gera um código curto único (ex: 8 caracteres hexadecimais)
            self.codigo_validacao = uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.modelo.titulo} - {self.aluno.nome}"