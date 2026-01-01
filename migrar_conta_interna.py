import os
import sys
import django

# ==============================================================================
# CONFIGURAÇÃO DO AMBIENTE DJANGO
# ==============================================================================
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from django.db import transaction
from core.models import CustomUser
from lumenios.pedagogico.models import Turma, PlanoDeAula, DiarioClasse, Atividade
from lumenios.plataforma.models import Curso # Se houver cursos do AVA

def migrar_dados():
    print("🚀 INICIANDO MIGRAÇÃO INTERNA (SUPABASE -> SUPABASE)...")
    
    # 1. IDENTIFICAR USUÁRIOS
    USERNAME_ORIGEM = 'iansantos'
    USERNAME_DESTINO = 'ian'

    try:
        user_origem = CustomUser.objects.get(username=USERNAME_ORIGEM)
        print(f"   👤 Origem encontrada: {user_origem.get_full_name()} ({user_origem.username})")
    except CustomUser.DoesNotExist:
        print(f"   ❌ Erro: Usuário de origem '{USERNAME_ORIGEM}' não encontrado.")
        return

    # 2. CRIAR OU RECUPERAR USUÁRIO DE DESTINO
    user_destino, created = CustomUser.objects.get_or_create(
        username=USERNAME_DESTINO,
        defaults={
            'email': 'ian@niocortex.com', # Email diferente para não conflitar se unique
            'first_name': 'Ian',
            'last_name': 'Professor',
            'role': 'PROFESSOR_CORP', # Define como Professor
            'is_staff': True,
            'tenant_id': user_origem.tenant_id, # Herda o mesmo Tenant/Escola
            'tenant_type': user_origem.tenant_type
        }
    )
    
    if created:
        user_destino.set_password('123456')
        user_destino.save()
        print(f"   ✨ Usuário de destino '{USERNAME_DESTINO}' CRIADO com sucesso.")
    else:
        print(f"   ℹ️  Usuário de destino '{USERNAME_DESTINO}' já existe. Mesclando dados.")

    # 3. TRANSFERÊNCIA DE DADOS (ATÔMICA)
    with transaction.atomic():
        print("\n   📦 Transferindo responsabilidades...")

        # -- MÓDULO PEDAGÓGICO (Gestão Escolar) --
        
        # 1. Turmas (Professor Regente)
        turmas = Turma.objects.filter(professor_regente=user_origem)
        qtd = turmas.update(professor_regente=user_destino)
        print(f"      ✅ {qtd} Turmas transferidas.")

        # 2. Planos de Aula
        planos = PlanoDeAula.objects.filter(professor=user_origem)
        qtd = planos.update(professor=user_destino)
        print(f"      ✅ {qtd} Planos de Aula transferidos.")

        # 3. Diários de Classe
        diarios = DiarioClasse.objects.filter(professor=user_origem)
        qtd = diarios.update(professor=user_destino)
        print(f"      ✅ {qtd} Diários de Classe transferidos.")

        # -- MÓDULO PLATAFORMA (AVA) --
        
        # 4. Cursos (Conteúdo)
        # Verifica se o modelo tem o campo 'professor' (comum em AVAs)
        if hasattr(Curso, 'professor'):
            cursos = Curso.objects.filter(professor=user_origem)
            qtd = cursos.update(professor=user_destino)
            print(f"      ✅ {qtd} Cursos (AVA) transferidos.")

        # -- PERMISSÕES E TENANT --
        # Garante que o professor tenha acesso ao mesmo Tenant (Escola) do Admin
        if user_destino.tenant_id != user_origem.tenant_id:
            user_destino.tenant_id = user_origem.tenant_id
            user_destino.save()
            print("      🏢 Tenant do professor sincronizado com o Admin.")

    print("\n✅ MIGRAÇÃO CONCLUÍDA!")
    print(f"   Agora você pode logar como '{USERNAME_DESTINO}' (Senha: 123456) e ver as turmas.")

if __name__ == "__main__":
    migrar_dados()