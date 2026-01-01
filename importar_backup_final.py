import os
import sys
import django
import sqlite3
import uuid

# ==============================================================================
# 1. CONFIGURAÇÃO DO AMBIENTE DJANGO (DESTINO: SUPABASE)
# ==============================================================================
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from core.models import CustomUser
from lumenios.pedagogico.models import Turma, Aluno

# ==============================================================================
# 2. CONFIGURAÇÃO DA FONTE (ORIGEM: BACKUP SQLITE)
# ==============================================================================
BACKUP_PATH = r"C:\Users\Ian Santos\Desktop\VSCODE\MultiVerso IO\niocortex_saas\backup_cortex_2025-11-27_07-10\gestao_alunos.db"

def conectar_sqlite():
    if not os.path.exists(BACKUP_PATH):
        print(f"❌ Erro: Backup não encontrado em: {BACKUP_PATH}")
        return None
    try:
        conn = sqlite3.connect(BACKUP_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ Erro ao abrir backup: {e}")
        return None

def get_coluna_nome(cursor, tabela, opcoes):
    """Descobre qual o nome da coluna de 'nome' na tabela (ex: nome, name, fullname)"""
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [c['name'] for c in cursor.fetchall()]
    for op in opcoes:
        if op in colunas:
            return op
    return None

def importar_dados():
    print("🚀 INICIANDO IMPORTAÇÃO (SQLITE LOCAL -> SUPABASE)...")
    
    conn = conectar_sqlite()
    if not conn: return
    cursor = conn.cursor()

    try:
        # --- 1. GARANTIR USUÁRIO 'IAN' (PROFESSOR) ---
        print("\n👤 Configurando Professor 'ian' no Supabase...")
        tenant_id = uuid.uuid4()
        
        # Cria ou recupera o usuário 'ian'
        professor, created = CustomUser.objects.get_or_create(
            username='ian',
            defaults={
                'email': 'ian@niocortex.com',
                'first_name': 'Ian',
                'last_name': 'Professor',
                'role': 'PROFESSOR_CORP',
                'is_staff': True,
                'tenant_id': tenant_id,
                'tenant_type': 'INDIVIDUAL'
            }
        )
        if created:
            professor.set_password('123456')
            professor.save()
            print("   ✅ Usuário 'ian' criado.")
        else:
            print("   ℹ️  Usuário 'ian' já existe. Usaremos ele.")
            tenant_id = professor.tenant_id

        # --- 2. IMPORTAR TURMAS ---
        print("\n🏫 Buscando Turmas no Backup...")
        
        # Identifica usuário antigo (Ian Santos)
        col_nome_user = get_coluna_nome(cursor, 'users', ['nome', 'name', 'username'])
        if col_nome_user:
            cursor.execute(f"SELECT id FROM users WHERE {col_nome_user} LIKE '%Ian%' OR username = 'iansantos' LIMIT 1")
            user_old = cursor.fetchone()
            id_old = user_old['id'] if user_old else 1
        else:
            id_old = 1 # Fallback

        # Identifica coluna de FK nas turmas
        cursor.execute("PRAGMA table_info(turmas)")
        cols_turma = [c['name'] for c in cursor.fetchall()]
        fk_col = next((c for c in ['user_id', 'autor_id', 'id_user', 'professor_id'] if c in cols_turma), None)

        if fk_col:
            cursor.execute(f"SELECT * FROM turmas WHERE {fk_col} = ?", (id_old,))
        else:
            cursor.execute("SELECT * FROM turmas") # Pega todas se não achar FK
            
        turmas_old = cursor.fetchall()
        print(f"   Encontradas {len(turmas_old)} turmas para importar.")

        mapa_turmas = {} # ID Antigo -> ID Novo (Supabase)

        for t in turmas_old:
            col_nome_turma = get_coluna_nome(cursor, 'turmas', ['nome', 'titulo', 'identificacao'])
            nome_turma = t[col_nome_turma] if col_nome_turma else f"Turma {t['id']}"
            
            nova_turma, _ = Turma.objects.get_or_create(
                nome=nome_turma,
                tenant_id=tenant_id,
                professor_regente=professor,
                defaults={'ano_letivo': 2025}
            )
            mapa_turmas[t['id']] = nova_turma.id
            print(f"   + Importada: {nome_turma}")

        # --- 3. IMPORTAR ALUNOS ---
        print("\n🎓 Importando Alunos...")
        if not mapa_turmas:
            print("   ⚠️ Nenhuma turma importada. Pulando alunos.")
        else:
            ids_turmas = list(mapa_turmas.keys())
            placeholders = ','.join('?' * len(ids_turmas))
            cursor.execute(f"SELECT * FROM alunos WHERE id_turma IN ({placeholders})", ids_turmas)
            alunos_old = cursor.fetchall()
            
            print(f"   Processando {len(alunos_old)} alunos...")
            
            count = 0
            for a in alunos_old:
                col_nome_aluno = get_coluna_nome(cursor, 'alunos', ['nome', 'name', 'nome_completo'])
                if not col_nome_aluno: continue
                
                nome_aluno = a[col_nome_aluno]
                turma_nova_id = mapa_turmas.get(a['id_turma'])
                
                # Campos opcionais
                matricula = str(a['matricula']) if 'matricula' in a.keys() and a['matricula'] else None
                
                if not Aluno.objects.filter(nome=nome_aluno, turma_id=turma_nova_id).exists():
                    Aluno.objects.create(
                        nome=nome_aluno,
                        turma_id=turma_nova_id,
                        tenant_id=tenant_id,
                        matricula_id=matricula
                    )
                    count += 1
            
            print(f"   ✅ {count} alunos importados com sucesso!")

    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()
        print("\n✨ Processo Finalizado! Acesse o Dashboard.")

if __name__ == "__main__":
    importar_dados()