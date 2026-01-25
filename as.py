import os
from pathlib import Path

# Define o caminho
path = Path("yourlife/social/migrations")

# Cria a pasta se não existir
if not path.exists():
    os.makedirs(path)
    print(f"✅ Pasta criada: {path}")

# Cria o arquivo __init__.py obrigatório
init_file = path / "__init__.py"
with open(init_file, 'w') as f:
    pass # Cria arquivo vazio

print(f"✅ Arquivo criado: {init_file}")
print("\nAgora o Django vai reconhecer o app!")