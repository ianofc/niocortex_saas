from django.db import models
from django.conf import settings
# Importando modelos do Pedagógico (Integração)
from pedagogical.models import Turma, Disciplina 

class SalaVirtual(models.Model):
    """ Vincula uma Turma + Disciplina a um ambiente de aula (Curso) """
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='salas_lumenios')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    capa = models.ImageField(upload_to='lumenios/capas/', blank=True, null=True)
    descricao = models.TextField(blank=True, verbose_name="Sobre a Matéria")
    
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disciplina.nome} - {self.turma.nome}"

class Modulo(models.Model):
    """ Ex: '1º Bimestre', 'Introdução à Física', 'Semana de Provas' """
    sala = models.ForeignKey(SalaVirtual, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=200)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return self.titulo

class MaterialAula(models.Model):
    """ O conteúdo: Vídeo, PDF, Link, Tarefa """
    TIPO_CHOICES = [
        ('VIDEO', 'Vídeo Aula'),
        ('PDF', 'Material de Leitura (PDF)'),
        ('LINK', 'Link Externo'),
        ('TAREFA', 'Entrega de Trabalho'),
    ]

    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='materiais')
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    
    # Conteúdo (Polimórfico simples)
    arquivo = models.FileField(upload_to='lumenios/materiais/', blank=True, null=True)
    link_externo = models.URLField(blank=True, null=True, help_text="Link do YouTube ou site externo")
    texto_apoio = models.TextField(blank=True, help_text="Descrição ou instruções")

    ordem = models.PositiveIntegerField(default=0)
    visivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordem']

class ProgressoAluno(models.Model):
    """ Rastreia o que o aluno já consumiu """
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    material = models.ForeignKey(MaterialAula, on_delete=models.CASCADE)
    concluido = models.BooleanField(default=False)
    data_conclusao = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('aluno', 'material')
