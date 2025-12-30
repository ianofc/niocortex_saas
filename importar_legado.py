import os
import uuid
import django
from django.db import connection

# Configurar ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from core.models import CustomUser, School
from lumenios.pedagogico.models import Turma, Aluno

def dict_fetchall(cursor):
    "Converte linhas do SQL em dicionários"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def importar_dados():
    with connection.cursor() as cursor:
        print("--- INICIANDO IMPORTAÇÃO DO SUPABASE (LEGADO) ---")

        # 1. IMPORTAR ESCOLAS
        # No sistema antigo: tabela 'escolas'
        # No novo: model 'School'
        print(">> Importando Escolas...")
        # Verifica se a tabela antiga existe
        try:
            cursor.execute("SELECT * FROM escolas")
            old_escolas = dict_fetchall(cursor)
        except Exception as e:
            print(f"Erro ao ler tabela 'escolas': {e}")
            old_escolas = []

        mapa_escolas = {} # ID Antigo -> Objeto Novo

        for old in old_escolas:
            # Nota: Django usa School.objects.filter... corrigindo abaixo:
            escola, created = School.objects.get_or_create(
            nome=old['nome'],  
            defaults={
                'tenant_id': str(uuid.uuid4())
            }
        )
            
            mapa_escolas[old['id']] = escola
            if created:
                print(f"   + Escola criada: {escola.nome}")
        
        # 2. IMPORTAR USUÁRIOS
        print("\n>> Importando Usuários...")
        cursor.execute("""
            SELECT u.*, r.name as role_nome 
            FROM users u 
            LEFT JOIN roles r ON u.role_id = r.id
        """)
        old_users = dict_fetchall(cursor)

        mapa_users = {} # ID Antigo -> Objeto Novo

        for old in old_users:
            if CustomUser.objects.filter(email=old['email']).exists():
                print(f"   ! Usuário {old['email']} já existe. Pulando.")
                u = CustomUser.objects.get(email=old['email'])
                mapa_users[old['id']] = u
                continue

            # Tradução de Roles (Flask -> Django)
            role_nova = 'ALUNO_FREE'
            role_antiga = old['role_nome']
            
            if role_antiga == 'admin': role_nova = 'ADMIN'
            elif role_antiga == 'professor': role_nova = 'PROFESSOR_FREE'
            elif role_antiga == 'coordenador': role_nova = 'COORDENACAO'
            elif role_antiga == 'aluno': role_nova = 'ALUNO_FREE'

            # Lógica para separar Nome e Sobrenome
            nome_completo = old.get('nome', '') or ''
            partes_nome = nome_completo.strip().split(' ', 1)
            first_name = partes_nome[0]
            last_name = partes_nome[1] if len(partes_nome) > 1 else ''

            # Lógica de Tenant (CORREÇÃO AQUI)
            tenant_type = 'INDIVIDUAL'
            escola_ref = None
            # Por padrão, gera um ID novo (usuário avulso)
            user_tenant_id = uuid.uuid4()

            # Se pertencer a uma escola migrada, herda o ID dela
            if old.get('escola_id') and old['escola_id'] in mapa_escolas:
                tenant_type = 'SCHOOL'
                escola_ref = mapa_escolas[old['escola_id']]
                user_tenant_id = escola_ref.tenant_id

            novo_user = CustomUser(
                username=old['username'],
                email=old['email'],
                password=old['password_hash'], 
                first_name=first_name,
                last_name=last_name,
                role=role_nova,
                tenant_type=tenant_type,
                tenant_id=user_tenant_id,  # <--- O CAMPO QUE FALTAVA
                school=escola_ref
            )
            
            novo_user.save()
            mapa_users[old['id']] = novo_user
            print(f"   + Usuário migrado: {novo_user.username} ({novo_user.role})")

        # 3. IMPORTAR TURMAS
        print("\n>> Importando Turmas...")
        try:
            cursor.execute("SELECT * FROM turmas")
            old_turmas = dict_fetchall(cursor)
            
            for t in old_turmas:
                # Usando o nome correto da coluna descoberto: 'autor_id'
                dono_id = t.get('autor_id')
                
                novo_autor = mapa_users.get(dono_id)
                
                if novo_autor:
                    # Verifica se a turma já existe para evitar duplicação
                    if not Turma.objects.filter(nome=t['nome'], tenant_id=novo_autor.tenant_id).exists():
                        nova_turma = Turma(
                            nome=t['nome'],
                            ano_letivo=2024, # Defina o ano padrão ou pegue do banco se existir
                            autor=novo_autor,
                            tenant_id=novo_autor.tenant_id
                        )
                        nova_turma.save()
                        print(f"   + Turma migrada: {nova_turma.nome}")
                    else:
                        print(f"   . Turma '{t['nome']}' já existe no banco novo.")
                else:
                    print(f"   ? Turma '{t.get('nome')}' ignorada: Autor (ID {dono_id}) não encontrado.")

        except Exception as e:
            print(f"   Erro ao migrar turmas: {e}")

    print("\n✅ Concluído.")

if __name__ == "__main__":
    importar_dados()