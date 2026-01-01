import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pastas para restaurar (Do backup para a produção)
DIRS_TO_RESTORE = {
    'aluno_BACKUP_LEGADO': 'aluno',
    'professor_BACKUP_LEGADO': 'professor',
}

def restaurar_templates():
    print("🚑 Restaurando Interface Social (Core)...")
    
    templates_root = os.path.join(BASE_DIR, 'templates')
    
    for backup_name, target_name in DIRS_TO_RESTORE.items():
        backup_path = os.path.join(templates_root, backup_name)
        target_path = os.path.join(templates_root, target_name)
        
        if os.path.exists(backup_path):
            print(f"   📂 Restaurando '{target_name}' a partir de '{backup_name}'...")
            
            # Se a pasta destino não existir, copia tudo
            if not os.path.exists(target_path):
                shutil.copytree(backup_path, target_path)
                print(f"      ✅ Restaurado com sucesso!")
            else:
                # Se já existir (pode ter arquivos misturados), copia arquivos faltantes
                for root, dirs, files in os.walk(backup_path):
                    # Calcula o caminho relativo
                    rel_path = os.path.relpath(root, backup_path)
                    dest_dir = os.path.join(target_path, rel_path)
                    
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    
                    for file in files:
                        src_file = os.path.join(root, file)
                        dst_file = os.path.join(dest_dir, file)
                        
                        # Só restaura se não existir no destino (para não quebrar edições recentes)
                        if not os.path.exists(dst_file):
                            shutil.copy2(src_file, dst_file)
                            print(f"      📄 Recuperado: {file}")
                        else:
                            print(f"      ⏭️  Ignorado (já existe): {file}")
        else:
            print(f"   ⚠️ Backup '{backup_name}' não encontrado. Nada a restaurar.")

if __name__ == "__main__":
    restaurar_templates()
    print("\n✨ Restauração concluída! A Rede Social deve estar acessível novamente.")