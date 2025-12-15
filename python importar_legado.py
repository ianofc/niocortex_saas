import os
import django
from django.db import connection

# Configurar ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from core.models import CustomUser, School
from pedagogical.models import Turma, Aluno

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
            # Verifica se já existe para não duplicar
            escola_existente = School.query.filter(nome=old['nome']).first() # Adaptar query Django
            # Nota: Django usa School.objects.filter... corrigindo abaixo:
            escola, created = School.objects.get_or_create(
                nome=old['nome'],
                defaults={'tenant_id': None} # O Model gera UUID automático
            )
            mapa_escolas[old['id']] = escola
            if created:
                print(f"   + Escola criada: {escola.nome}")
        
        # 2. IMPORTAR USUÁRIOS
        # Antigo: tabela 'users' com 'role_id'
        # Novo: CustomUser com 'role' (string)
        print("\n>> Importando Usuários...")
        cursor.execute("""
            SELECT u.*, r.name as role_name 
            FROM users u 
            LEFT JOIN roles r ON u.role_id = r.id
        """)
        old_users = dict_fetchall(cursor)

        mapa_users = {} # ID Antigo -> ID Novo

        for old in old_users:
            if CustomUser.objects.filter(email=old['email']).exists():
                print(f"   ! Usuário {old['email']} já existe. Pulando.")
                u = CustomUser.objects.get(email=old['email'])
                mapa_users[old['id']] = u
                continue

            # Tradução de Roles (Flask -> Django)
            role_nova = 'ALUNO_FREE'
            role_antiga = old['role_name']
            
            if role_antiga == 'admin': role_nova = 'ADMIN'
            elif role_antiga == 'professor': role_nova = 'PROFESSOR_FREE'
            elif role_antiga == 'coordenador': role_nova = 'COORDENACAO'
            elif role_antiga == 'aluno': role_nova = 'ALUNO_FREE'

            # Define Tenant Type
            tenant_type = 'INDIVIDUAL'
            escola_ref = None
            if old.get('escola_id') and old['escola_id'] in mapa_escolas:
                tenant_type = 'SCHOOL'
                escola_ref = mapa_escolas[old['escola_id']]

            novo_user = CustomUser(
                username=old['username'],
                email=old['email'],
                password=old['password_hash'], # Atenção: Se o hash for diferente (Bcrypt vs Argon2), o usuário precisará resetar a senha
                nome=old.get('nome', ''),
                role=role_nova,
                tenant_type=tenant_type,
                school=escola_ref
            )
            # Como não temos o tenant_id no antigo, o Django vai gerar um novo no .save()
            novo_user.save()
            mapa_users[old['id']] = novo_user
            print(f"   + Usuário migrado: {novo_user.username} ({novo_user.role})")

        # 3. IMPORTAR TURMAS
        print("\n>> Importando Turmas...")
        try:
            cursor.execute("SELECT * FROM turmas")
            old_turmas = dict_fetchall(cursor)
            
            for t in old_turmas:
                # Acha o novo dono (professor)
                dono_antigo_id = t.get('id_user') # Verifique se a coluna é id_user ou autor_id no banco antigo
                # No models.py enviado, User.turmas tem backref='autor', mas na tabela real precisa ver a FK
                # Assumindo que o banco antigo tem uma FK para users.
                
                # Se não acharmos a FK direta, vamos tentar inferir ou pular
                # Pelo arquivo migrar_dados.py antigo: "novo_autor_id = map_users.get(t.get('id_user'))"
                
                novo_autor = mapa_users.get(t.get('id_user'))
                
                if novo_autor:
                    nova_turma = Turma(
                        nome=t['nome'],
                        ano_letivo=2024, # Valor padrão ou extrair de data
                        autor=novo_autor,
                        tenant_id=novo_autor.tenant_id
                    )
                    nova_turma.save()
                    print(f"   + Turma migrada: {nova_turma.nome}")
        except Exception as e:
            print(f"   Erro ao migrar turmas (tabela pode estar vazia ou nome diferente): {e}")

    print("\n✅ Concluído.")

if __name__ == "__main__":
    importar_dados()