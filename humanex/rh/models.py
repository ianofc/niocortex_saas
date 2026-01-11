from django.db import models
from core.models import CustomUser
import uuid

class Departamento(models.Model):
    """ Ex: Secretaria, Limpeza, Docentes, TI, Coordenação """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    nome = models.CharField(max_length=100)
    codigo_centro_custo = models.CharField(max_length=20, blank=True, help_text="Para integração financeira")
    responsavel = models.ForeignKey('Funcionario', on_delete=models.SET_NULL, null=True, blank=True, related_name='gerente_departamento')

    def __str__(self):
        return self.nome

class Cargo(models.Model):
    """ Ex: Professor I, Professor II, Auxiliar Administrativo """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    titulo = models.CharField(max_length=100)
    cbo = models.CharField(max_length=20, blank=True, help_text="Código Brasileiro de Ocupações")
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.titulo

class Funcionario(models.Model):
    """
    A ficha completa do colaborador.
    Vincula-se ao User para permitir login, mas existe mesmo se o funcionário não acessar o sistema.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    # Vínculo com usuário de sistema
    usuario = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='ficha_funcionario')
    
    # Dados Pessoais Estendidos
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField()
    
    # Dados Contratuais
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    matricula = models.CharField(max_length=50)
    data_admissao = models.DateField()
    data_demissao = models.DateField(null=True, blank=True)
    
    tipo_contrato = models.CharField(max_length=20, choices=[
        ('CLT', 'CLT'),
        ('PJ', 'PJ / Prestador'),
        ('ESTAGIO', 'Estagiário'),
        ('TEMPORARIO', 'Temporário'),
        ('CONCURSADO', 'Concursado (Público)')
    ], default='CLT')

    salario_atual = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Dados de Contato
    email_corporativo = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField(blank=True)
    
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome_completo} ({self.cargo.titulo})"