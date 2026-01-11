import subprocess
import sys

def run_git_command(command, description):
    print(f"\n[GIT] {description}...")
    try:
        # Executa o comando e captura a saída
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        
        # Se houver saída padrão, mostre
        if result.stdout:
            print(result.stdout.strip())
            
        # Se houver erro e o código de retorno for diferente de 0, avise
        if result.returncode != 0:
            print(f"[ERRO] Falha ao {description.lower()}.")
            print(f"Detalhes: {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        print(f"[ERRO CRÍTICO] {e}")
        return False

def main():
    print("=== UNIFICADOR DE REPOSITÓRIO GITHUB ===")
    print("Este script vai preparar e enviar todo o seu projeto atual para o GitHub.\n")

    # 1. Adicionar todos os arquivos (Staging)
    if not run_git_command("git add .", "Adicionando todos os arquivos ao Git"):
        return

    # 2. Criar o Commit (O Pacote de Alterações)
    # Verifica se há algo para commitar antes
    status = subprocess.run("git status --porcelain", shell=True, text=True, capture_output=True)
    if status.stdout.strip():
        if not run_git_command('git commit -m "Unificação do Projeto: Navbar, Stories V10, Talkio Mobile e Rotas"', "Criando commit de unificação"):
            return
    else:
        print("[INFO] Nada para commitar (árvore de trabalho limpa). Seguindo para o push...")

    # 3. Renomear Branch para 'main' (Padrão moderno)
    if not run_git_command("git branch -M main", "Renomeando branch local para 'main'"):
        return

    # 4. Enviar para o GitHub (Push)
    print("\n[GIT] Enviando para o servidor remoto (origin main)...")
    push_cmd = subprocess.run("git push -u origin main", shell=True, text=True, capture_output=True)
    
    if push_cmd.returncode == 0:
        print(push_cmd.stdout)
        print("\n[SUCESSO] Projeto enviado e unificado com o GitHub!")
    else:
        print("[AVISO] O push padrão falhou. Tentando forçar a unificação (--force)...")
        # Tenta forçar o envio caso haja histórico desconexo
        force_push = subprocess.run("git push -u origin main --force", shell=True, text=True, capture_output=True)
        if force_push.returncode == 0:
            print(force_push.stdout)
            print("\n[SUCESSO] Projeto unificado forçadamente com o GitHub!")
        else:
            print("\n[ERRO FATAL] Não foi possível enviar para o GitHub.")
            print("Verifique se o repositório remoto está configurado corretamente com: git remote -v")
            print("Erro detalhado:")
            print(push_cmd.stderr)
            print(force_push.stderr)

if __name__ == "__main__":
    main()