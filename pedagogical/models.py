# niocortex/pedagogical/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class Turma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    nome = models.CharField(max_length=100)
    ano_letivo = models.IntegerField(default=timezone.now().year)

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    # Campos Pessoais (Adicionados para corrigir o FieldError)
    nome = models.CharField(max_length=255)
    matricula_id = models.CharField(max_length=50, blank=True, null=True, help_text="Código ou número de chamada")
    email = models.EmailField(blank=True, null=True, help_text="Email do aluno ou responsável")
    telefone_responsavel = models.CharField(max_length=20, blank=True, null=True)
    
    # Relacionamentos
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True, related_name='alunos')
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.matricula_id or 'S/M'})"

# --- MIGRAÇÃO DO LEGADO CORTEX (ADAPTADO PARA DJANGO) ---

class PlanoDeAula(models.Model):
    """
    Antigo: class PlanoDeAula(db.Model)
    Foco: Planejamento pedagógico e integração com BNCC.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='planos_aula')
    
    titulo = models.CharField(max_length=200)
    data_prevista = models.DateField()
    
    # Conteúdo Pedagógico
    conteudo = models.TextField(blank=True)
    habilidades_bncc = models.TextField(blank=True, help_text="Códigos da BNCC separados por vírgula")
    objetivos = models.TextField(blank=True)
    metodologia = models.TextField(blank=True)
    recursos = models.TextField(blank=True)
    avaliacao_texto = models.TextField(blank=True, verbose_name="Método de Avaliação")
    
    status = models.CharField(max_length=50, default='Planejado', choices=[
        ('Planejado', 'Planejado'),
        ('Ministrado', 'Ministrado'),
        ('Adiado', 'Adiado')
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.turma.nome}"

class Atividade(models.Model):
    """
    Antigo: class Atividade(db.Model)
    Foco: Avaliações que valem nota (Provas, Trabalhos).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='atividades')
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, default='Atividade', choices=[
        ('Prova', 'Prova'),
        ('Trabalho', 'Trabalho'),
        ('Atividade', 'Atividade em Sala'),
        ('Simulado', 'Simulado')
    ])
    
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso na média final")
    valor_maximo = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    
    unidade = models.CharField(max_length=20, default='1ª Unidade', choices=[
        ('1ª Unidade', '1º Bimestre/Trimestre'),
        ('2ª Unidade', '2º Bimestre/Trimestre'),
        ('3ª Unidade', '3º Bimestre/Trimestre'),
        ('4ª Unidade', '4º Bimestre/Trimestre'),
        ('Recuperação', 'Recuperação Final')
    ])
    
    data_aplicacao = models.DateField()
    descricao = models.TextField(blank=True)
    
    # Arquivo anexo (Prova escaneada ou gabarito)
    arquivo = models.FileField(upload_to='provas/', null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.unidade})"

class Nota(models.Model):
    """
    Antigo: class Presenca(db.Model) - Parte de NOTAS
    Foco: A nota individual do aluno em uma atividade.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas')
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='notas_lancadas')
    
    valor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Feedback qualitativo
    feedback = models.TextField(blank=True, help_text="Comentário do professor para o aluno")
    
    situacao = models.CharField(max_length=50, default='Normal', choices=[
        ('Normal', 'Entregue'),
        ('Pendente', 'Não Entregue'),
        ('Justificado', 'Falta Justificada')
    ])

    class Meta:
        unique_together = ('aluno', 'atividade') # Um aluno só tem uma nota por atividade

    def __str__(self):
        return f"{self.aluno.nome} - {self.atividade.titulo}: {self.valor}"

class DiarioClasse(models.Model):
    """
    Antigo: class DiarioBordo(db.Model)
    Foco: Registro oficial do que aconteceu na aula (obrigatório pelo MEC).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    
    conteudo_lecionado = models.TextField()
    observacoes = models.TextField(blank=True)
    
    # Se a aula foi baseada em um plano
    plano_referencia = models.ForeignKey(PlanoDeAula, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Aula {self.data} - {self.turma.nome}"

class Frequencia(models.Model):
    """
    Antigo: class Presenca(db.Model) - Parte de FREQUÊNCIA
    Foco: Presença ou Falta do aluno em um dia letivo.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    diario = models.ForeignKey(DiarioClasse, on_delete=models.CASCADE, related_name='frequencias')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='frequencias')
    
    presente = models.BooleanField(default=True)
    justificativa = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('diario', 'aluno')