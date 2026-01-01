import os
import shutil
import sys

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Apps que devem ter suas migrações resetadas
APPS_TO_RESET = [
    'core',
    'financial',
    'hr',
    'secretariat',
    'crm_sales',
    'lumenios/plataforma',
    'lumenios/pedagogico'
]

def clear_migrations():
    print("🧹 Limpando arquivos de migração antigos...")
    
    for app_path in APPS_TO_RESET:
        # Corrige caminho para Windows/Linux
        full_path = os.path.join(BASE_DIR, *app_path.split('/'), 'migrations')
        
        if os.path.exists(full_path):
            for filename in os.listdir(full_path):
                if filename != '__init__.py' and filename.endswith('.py'):
                    file_to_remove = os.path.join(full_path, filename)
                    try:
                        os.remove(file_to_remove)
                        print(f"   🗑️ Removido: {app_path}/migrations/{filename}")
                    except Exception as e:
                        print(f"   ❌ Erro ao remover {filename}: {e}")
            
            # Remove cache se existir
            pycache = os.path.join(full_path, '__pycache__')
            if os.path.exists(pycache):
                shutil.rmtree(pycache)
        else:
            # Cria a pasta migrations se não existir (para apps novos)
            os.makedirs(full_path, exist_ok=True)
            with open(os.path.join(full_path, '__init__.py'), 'w') as f:
                pass
            print(f"   ✨ Criada pasta migrations para: {app_path}")

def fix_dependencies():
    """
    Remove dependências quebradas manualmente se necessário.
    Neste caso, apagar os arquivos (etapa anterior) já resolve, 
    pois o makemigrations vai recriar as dependências corretas.
    """
    pass

def run_makemigrations():
    print("\n⚙️ Gerando novas migrações (Clean Slate)...")
    # Ordem importa para evitar dependências circulares
    
    # 1. Apps Base (Sem dependências externas fortes)
    os.system("python manage.py makemigrations core")
    os.system("python manage.py makemigrations hr")
    
    # 2. Apps do AVA (Lumenios)
    # Importante: Pedagogico vem antes ou depois? Depende de quem usa quem.
    # Plataforma usa Auth (Core). Pedagogico usa Auth.
    os.system("python manage.py makemigrations pedagogico") # Label do app é 'pedagogico'
    os.system("python manage.py makemigrations plataforma") # Label do app é 'plataforma' ou 'lumenios_plataforma'?
    
    # OBS: Se o label for composto, o comando acima pode falhar. 
    # Vamos tentar o genérico para pegar tudo o que falta.
    os.system("python manage.py makemigrations")

def run_migrate():
    print("\n📦 Aplicando migrações ao banco de dados...")
    os.system("python manage.py migrate")

if __name__ == "__main__":
    print("🚀 INICIANDO RESET DE MIGRAÇÕES\n")
    
    clear_migrations()
    run_makemigrations()
    
    print("\n---------------------------------------------------------")
    print("⚠️  Se houver erros de 'dependency' acima, rode 'python manage.py migrate' agora.")
    print("   Se o banco estiver sujo, rode 'python reset_db.py' antes de migrar.")
    print("---------------------------------------------------------")