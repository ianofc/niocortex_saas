from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Pessoal
    cpf = models.CharField(max_length=14, blank=True, null=True, unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=20, blank=True)
    
    # Institucional
    role = models.CharField("Cargo", max_length=20, default='ALUNO') 
    matricula = models.CharField(max_length=50, blank=True)
    
    # Correção da FK para Turma usando o label definido acima
    turma = models.ForeignKey('pedagogico.Turma', on_delete=models.SET_NULL, null=True, blank=True)
    
    school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True, blank=True)
    tenant_type = models.CharField(max_length=20, default='PUBLIC')
    tenant_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Status
    is_premium = models.BooleanField(default=False)
    
    # Mídia (Campos Corrigidos)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    capa = models.ImageField(upload_to='covers/', blank=True, null=True)
    bio = models.TextField(blank=True)
    
    # Preferências
    hobby = models.CharField(max_length=100, blank=True)
    visao_mundo = models.CharField(max_length=20, blank=True)
    
    # Lógica Vital para o Menu
    nivel_ensino = models.CharField(max_length=20, default='medio') # superior, bebe, medio
    fase_vida = models.CharField(max_length=20, default='JOVEM') # ADULTO, BEBE

class School(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20)
    def __str__(self): return self.nome
