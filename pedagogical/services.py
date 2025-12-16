# niocortex/pedagogical/services.py

from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError
from .models import Turma, Aluno
from core.models import CustomUser

class PedagogicalService:
    """
    Controlador central de lógica acadêmica.
    Garante que NENHUM dado seja acessado sem o filtro de tenant_id correto.
    """

    @staticmethod
    def _get_active_tenant_id(user: CustomUser):
        """
        Determina qual é o 'contexto' atual do usuário.
        - Se for Corporate: Retorna o ID da Escola.
        - Se for Free/Individual: Retorna o ID do próprio Usuário.
        """
        # Se o usuário tem um tenant_id definido no perfil (School ou Pessoal)
        if user.tenant_id:
            return user.tenant_id
        
        # Fallback de segurança (nunca deve acontecer se o registro for bem feito)
        raise PermissionDenied("Usuário sem Tenant ID definido. Contate o suporte.")

    # --- GESTÃO DE TURMAS ---

    @classmethod
    def list_turmas(cls, user: CustomUser):
        """
        Lista apenas as turmas que pertencem ao tenant atual do usuário.
        """
        tenant_id = cls._get_active_tenant_id(user)
        
        # Regra de Ouro: Filtrar sempre pelo tenant_id
        return Turma.objects.filter(tenant_id=tenant_id).order_by('-ano_letivo', 'nome')

    @classmethod
    def create_turma(cls, user: CustomUser, data: dict) -> Turma:
        """
        Cria uma turma, atribuindo automaticamente o tenant_id correto.
        """
        tenant_id = cls._get_active_tenant_id(user)
        
        # Verificação de Limites para Plano Free (Exemplo)
        if user.tenant_type == 'INDIVIDUAL':
            contagem = Turma.objects.filter(tenant_id=tenant_id).count()
            if contagem >= 5:  # Limite de 5 turmas no plano Free
                raise ValidationError("Limite de turmas atingido no plano Gratuito.")

        with transaction.atomic():
            nova_turma = Turma(
                tenant_id=tenant_id,
                nome=data.get('nome'),
                ano_letivo=data.get('ano_letivo', 2025),
                autor=user, # O criador original (para auditoria)
                # Se for Corporate, vinculamos a escola explicitamente se necessário
                escola=user.school if user.is_corporate_user() else None
            )
            nova_turma.save()
            
        return nova_turma

    @classmethod
    def get_turma(cls, user: CustomUser, turma_id: int) -> Turma:
        """
        Busca uma turma específica, garantindo que ela pertença ao usuário.
        """
        tenant_id = cls._get_active_tenant_id(user)
        
        try:
            return Turma.objects.get(id=turma_id, tenant_id=tenant_id)
        except Turma.DoesNotExist:
            raise PermissionDenied("Turma não encontrada ou acesso negado.")

    # --- GESTÃO DE ALUNOS ---

    @classmethod
    def add_aluno(cls, user: CustomUser, turma_id: int, dados_aluno: dict) -> Aluno:
        """
        Adiciona um aluno a uma turma, respeitando os limites do plano.
        """
        tenant_id = cls._get_active_tenant_id(user)
        turma = cls.get_turma(user, turma_id) # Já valida a segurança da turma

        # Verificação de Limites (20 alunos por turma no Free)
        if user.tenant_type == 'INDIVIDUAL':
            if turma.alunos.count() >= 20:
                raise ValidationError("Limite de 20 alunos por turma no plano Gratuito.")

        aluno = Aluno(
            tenant_id=tenant_id,
            turma=turma,
            nome=dados_aluno.get('nome'),
            matricula_id=dados_aluno.get('matricula', None) 
            # Se não passar matrícula, podemos gerar uma automática depois
        )
        aluno.save()
        return aluno