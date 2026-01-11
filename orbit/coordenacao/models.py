from django.db import models
from django.conf import settings
import uuid

# --- CORREÇÃO: Importação direta para evitar erro de App Label ---
from lumenios.pedagogico.models import Aluno, Turma, Disciplina
# ---------------------------------------------------------------

class OcorrenciaDisciplinar(models.Model):
    """ Registros de comportamento/ocorrências dos alunos """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    # Referência direta à classe Aluno importada
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='ocorrencias')
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_ocorrencia = models.DateTimeField()
    
    GRAVIDADE_CHOICES = [
        ('BAIXA', 'Baixa (Conversa/Aviso)'),
        ('MEDIA', 'Média (Advertência)'),
        ('ALTA', 'Alta (Suspensão)'),
        ('GRAVE', 'Grave (Expulsão/Conselho)'),
    ]
    gravidade = models.CharField(max_length=10, choices=GRAVIDADE_CHOICES, default='BAIXA')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno} - {self.titulo}"

class PlanejamentoAula(models.Model):
    """ Planos de aula enviados pelos professores para aprovação da coordenação """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Referências diretas
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_aplicacao = models.DateField()
    
    STATUS_CHOICES = [
        ('RASCUNHO', 'Rascunho'),
        ('ENVIADO', 'Enviado para Análise'),
        ('APROVADO', 'Aprovado'),
        ('REVISAO', 'Solicitada Revisão'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')
    comentario_coord = models.TextField(blank=True, help_text="Feedback da coordenação")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plano: {self.titulo} ({self.status})"