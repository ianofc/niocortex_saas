from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import CustomUser

# Tenta importar modelos satélites
try:
    from lumenios.pedagogico.models import Aluno
except ImportError:
    Aluno = None

try:
    from yourlife.social.models import Album
except ImportError:
    Album = None

@receiver(post_save, sender=CustomUser)
def gerenciar_integracoes_usuario(sender, instance, created, **kwargs):
    if created:
        print(f"   ---> [Signal] Integrando usuário: {instance.username}")
        
        # 1. Integração com Pedagógico
        # CORREÇÃO: Usa 'matricula_escolar' e remove 'nome' (que já está no User)
        if instance.role == 'ALUNO' and Aluno:
            try:
                Aluno.objects.get_or_create(
                    usuario=instance,
                    defaults={
                        'matricula_escolar': instance.matricula,
                        'turma': instance.turma
                    }
                )
            except Exception as e:
                print(f"   [!] Erro ao criar Aluno auto: {e}")

        # 2. Integração com Social (Álbuns)
        if Album:
            try:
                Album.objects.get_or_create(
                    usuario=instance,
                    titulo="Fotos de Perfil",
                    defaults={
                        'descricao': 'Album automático para fotos de perfil',
                        'privacidade': 'PUBLIC'
                    }
                )
                Album.objects.get_or_create(
                    usuario=instance,
                    titulo="Linha do Tempo",
                    defaults={'privacidade': 'PUBLIC'}
                )
            except Exception as e:
                print(f"   [!] Erro ao criar Álbuns auto: {e}")

@receiver(post_save, sender=CustomUser)
def salvar_integracoes(sender, instance, **kwargs):
    # Atualiza vinculos se necessário
    if instance.role == 'ALUNO' and Aluno:
        try:
            if hasattr(instance, 'perfil_escolar'):
                instance.perfil_escolar.save()
        except:
            pass