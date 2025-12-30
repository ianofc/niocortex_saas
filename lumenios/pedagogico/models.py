from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class Turma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True, null=True, blank=True)
    nome = models.CharField(max_length=100)
    ano_letivo = models.IntegerField(default=timezone.now().year)
    professor_regente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='turmas_regente')

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True, null=True, blank=True)
    
    nome = models.CharField(max_length=255)
    matricula_id = models.CharField(max_length=50, blank=True, null=True, help_text="Código ou número de chamada")
    email = models.EmailField(blank=True, null=True, help_text="Email do aluno ou responsável")
    telefone_responsavel = models.CharField(max_length=20, blank=True, null=True)
    
    # Relacionamentos
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True, related_name='alunos')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.matricula_id or 'S/M'})"

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Disciplina")
    descricao = models.TextField(blank=True, verbose_name="Descrição")

    def __str__(self):
        return self.nome

class PlanoDeAula(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True, null=True, blank=True)
    
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='planos_aula')
    
    titulo = models.CharField(max_length=200)
    data_prevista = models.DateField()
    
    conteudo = models.TextField(blank=True)
    habilidades_bncc = models.TextField(blank=True)
    objetivos = models.TextField(blank=True)
    metodologia = models.TextField(blank=True)
    recursos = models.TextField(blank=True)
    
    status = models.CharField(max_length=50, default='Planejado', choices=[
        ('Planejado', 'Planejado'),
        ('Ministrado', 'Ministrado'),
        ('Adiado', 'Adiado')
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.turma.nome}"

class Atividade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True, null=True, blank=True)
    
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
    data_aplicacao = models.DateField()
    descricao = models.TextField(blank=True)
    arquivo = models.FileField(upload_to='provas/', null=True, blank=True)

    def __str__(self):
        return self.titulo

class Nota(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True, null=True, blank=True)
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas')
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='notas_lancadas')
    
    valor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('aluno', 'atividade')

    def __str__(self):
        return f"{self.aluno.nome} - {self.valor}"

class DiarioClasse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True, null=True, blank=True)
    
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    
    conteudo_lecionado = models.TextField()
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"Aula {self.data} - {self.turma.nome}"

class Frequencia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True, null=True, blank=True)
    
    diario = models.ForeignKey(DiarioClasse, on_delete=models.CASCADE, related_name='frequencias')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='frequencias')
    
    presente = models.BooleanField(default=True)
    justificativa = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('diario', 'aluno')