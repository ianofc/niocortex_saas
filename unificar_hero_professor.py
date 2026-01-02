import os
import shutil
import sys
import subprocess

# Mapeamento: O que o Django está pedindo (Antigo) <- Onde pode estar agora (Novo)
RESTORE_MAP = {
    'hr': ['humaniox', 'humanex', 'talentios', 'humaniox/hr'],
    'financial': ['finexio', 'ledger', 'financios', 'capitalios', 'finexio/financial'],
    'secretariat': ['cognios', 'hub', 'iodesk', 'secretariat', 'cognios/secretariat'],
    'coordenacao': ['pedagiox', 'orbit', 'pedagogico_gestao', 'pedagiox/coordenacao'],
    'crm_sales': ['vionex', 'vionex/crm_sales'],
    'direcao': ['prioris', 'prioris/direcao']
}

def restore_legacy_names():
    print(">>> RESTAURANDO NOMES ANTIGOS PARA PERMITIR O BACKUP <<<")
    
    for legacy_name, possible_new_names in RESTORE_MAP.items():
        # Se a pasta antiga já existe na raiz, está tudo bem
        if os.path.exists(legacy_name):
            print(f"✅ Pasta '{legacy_name}' já existe.")
            continue
            
        found = False
        for candidate in possible_new_names:
            # Verifica se o candidato existe
            if os.path.exists(candidate):
                print(f"♻️  Renomeando/Movendo: '{candidate}' -> '{legacy_name}'")
                try:
                    # Se for subpasta (ex: humaniox/hr), move para a raiz
                    if '/' in candidate or '\\' in candidate:
                        shutil.move(candidate, legacy_name)
                    else:
                        # Se for renomeação direta (ex: humaniox -> hr)
                        os.rename(candidate, legacy_name)
                    found = True
                    break
                except Exception as e:
                    print(f"   [ERRO] Falha ao mover {candidate}: {e}")
        
        if not found:
            print(f"⚠️  ALERTA: Não encontrei a pasta para '{legacy_name}'. O backup pode falhar.")

def run_backup():
    print("\n>>> EXECUTANDO BACKUP AGORA <<<")
    output_file = "backup_seguro.json"
    
    cmd = [sys.executable, "manage.py", "dumpdata", 
           "--exclude", "auth.permission", 
           "--exclude", "contenttypes", 
           "--exclude", "admin.logentry", 
           "--exclude", "sessions.session", 
           "--indent", "2"]
    
    try:
        with open(output_file, "w", encoding='utf-8') as f:
            subprocess.run(cmd, stdout=f, check=True)
        print(f"\n✅✅✅ BACKUP REALIZADO COM SUCESSO: {output_file}")
        print("Agora você pode prosseguir com a migração final das marcas.")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Ainda deu erro no Backup.")
        print("DICA: Verifique se existe alguma pasta 'hr', 'financial' faltando na raiz.")
        return False

if __name__ == "__main__":
    # 1. Traz as pastas de volta pro nome velho
    restore_legacy_names()
    
    # 2. Tenta o backup
    success = run_backup()
    
    if not success:
        print("\nTentativa de correção forçada de imports...")
        # Se falhar, é porque tem imports quebrados no código.
        # Mas geralmente, restaurar as pastas resolve o ModuleNotFoundError.