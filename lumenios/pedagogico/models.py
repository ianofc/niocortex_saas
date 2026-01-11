from django.db import models
from django.conf import settings
from django.utils import timezone

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    tenant_id = models.CharField(max_length=100, blank=True, null=True)

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    ano_letivo = models.IntegerField(default=2025)
    professor_regente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='turmas_regente')
    tenant_id = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self): return self.nome

class Aluno(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    telefone_responsavel = models.CharField(max_length=20, blank=True, null=True)
    matricula_id = models.CharField(max_length=50, blank=True, null=True)
    
    # FKs
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, related_name='alunos')
    
    # O CAMPO NOVO (CRÍTICO)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='aluno_profile')
    
    tenant_id = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self): return self.nome

class PlanoDeAula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    tema = models.CharField(max_length=200) # Era titulo
    data = models.DateField(default=timezone.now) # Era data_prevista - DEFAULT ADICIONADO

class Horario(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    dia_semana = models.IntegerField()
    hora_inicio = models.TimeField()

class DiarioClasse(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField()
    conteudo = models.TextField() # Era conteudo_lecionado

class Atividade(models.Model):
    titulo = models.CharField(max_length=200)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data_entrega = models.DateField(default=timezone.now) # Era data_aplicacao - DEFAULT ADICIONADO

class Frequencia(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now) # DEFAULT ADICIONADO PARA NÃO TRAVAR
    presente = models.BooleanField(default=True)

class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
