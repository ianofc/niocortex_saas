import os
import shutil
from pathlib import Path

# Configuração Base
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / 'templates'
CORE_DIR = BASE_DIR / 'core'

# 1. Mapeamento de Movimentação de Templates (Origem -> Destino)
# O script cria as pastas de destino automaticamente
TEMPLATE_MOVES = {
    # --- ALUNO ---
    'aluno/grades.html': 'aluno/academico/boletim.html',
    'aluno/subjects.html': 'aluno/academico/disciplinas.html',
    'aluno/lesson_viewer.html': 'aluno/academico/sala_aula.html',
    'aluno/activity_detail.html': 'aluno/academico/atividade.html',
    'aluno/files.html': 'aluno/academico/arquivos.html',
    'aluno/timetable.html': 'aluno/academico/grade_horaria.html',
    
    'aluno/financial.html': 'aluno/administrativo/financeiro.html',
    'aluno/student_services.html': 'aluno/administrativo/secretaria.html',
    'aluno/services.html': 'aluno/administrativo/secretaria_old.html', # Backup se duplicado
    'aluno/student_id_card.html': 'aluno/administrativo/carteirinha.html',
    
    'aluno/library.html': 'aluno/extras/biblioteca.html',
    'aluno/career_center.html': 'aluno/extras/carreira.html',
    'aluno/thesis_manager.html': 'aluno/extras/tcc.html',
    'aluno/gamification_store.html': 'aluno/extras/loja.html',
    'aluno/daily_diary.html': 'aluno/extras/diario_infantil.html',
    
    'aluno/profile.html': 'aluno/dashboard/perfil.html',
    'aluno/dashboard.html': 'aluno/dashboard/home.html', # Se existir solto
    'core/aluno_dashboard_base.html': 'aluno/base.html', # Movendo base para pasta do aluno
    
    'aluno/premium.html': 'aluno/premium/landing.html',
    'aluno/premium_stats.html': 'aluno/premium/stats.html',

    # --- PROFESSOR ---
    'professor/turma/gradebook.html': 'professor/turmas/notas.html',
    'professor/turma/chamada.html': 'professor/turmas/chamada.html',
    'professor/turma/diario_classe.html': 'professor/turmas/diario.html',
    'professor/turma/visao_geral.html': 'professor/turmas/visao_geral.html',
    'professor/turma/editar_alunos_massa.html': 'professor/turmas/editar_massa.html',
    
    'professor/planejamento/todos_planos.html': 'professor/planejamento/meus_planos.html',
    # Arquivos novos sugeridos (se você já criou, descomente)
    # 'teacher_schedule.html': 'professor/planejamento/grade_horaria.html',
    # 'material_manager.html': 'professor/planejamento/materiais.html',
    # 'class_analytics.html': 'professor/administrativo/analytics.html',
    # 'teacher_services.html': 'professor/administrativo/secretaria.html',

    'professor/atividades/listar_atividades.html': 'professor/avaliacoes/lista.html',
    'professor/atividades/nova_atividade.html': 'professor/avaliacoes/criar.html',
    'professor/atividades/editar_atividade.html': 'professor/avaliacoes/editar.html',
    'professor/atividades/gerador_provas.html': 'professor/avaliacoes/gerador_provas.html',

    'core/professor_dashboard_base.html': 'professor/base.html',

    # --- LIMPEZA DA PASTA EDIT (Jogando para Admin/Secretaria) ---
    'edit/edit_escola.html': 'admin/configuracoes/editar_escola.html',
    'edit/edit_turma.html': 'pedagogical/turmas/editar.html',
    'edit/edit_aluno.html': 'secretariat/alunos/editar.html',
    'edit/edit_professor.html': 'hr/funcionarios/editar_professor.html',
    'edit/edit_coordenador.html': 'hr/funcionarios/editar_coordenador.html',
}

def organizar_templates():
    print("📂 Iniciando organização dos TEMPLATES...")
    
    for src, dest in TEMPLATE_MOVES.items():
        src_path = TEMPLATES_DIR / src
        dest_path = TEMPLATES_DIR / dest
        
        if src_path.exists():
            # Criar pasta de destino se não existir
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Mover arquivo
            try:
                shutil.move(str(src_path), str(dest_path))
                print(f"✅ Movido: {src} -> {dest}")
            except Exception as e:
                print(f"❌ Erro ao mover {src}: {e}")
        else:
            print(f"⚠️  Arquivo não encontrado (ignorado): {src}")

    # Remover pastas vazias antigas
    dirs_to_clean = [
        TEMPLATES_DIR / 'aluno',
        TEMPLATES_DIR / 'professor/turma',
        TEMPLATES_DIR / 'professor/atividades',
        TEMPLATES_DIR / 'edit'
    ]
    
    for d in dirs_to_clean:
        if d.exists() and not any(d.iterdir()):
            d.rmdir()
            print(f"🗑️ Pasta vazia removida: {d}")

def estruturar_views_core():
    print("\n🐍 Reestruturando CORE/VIEWS (Backend)...")
    
    views_package = CORE_DIR / 'views'
    old_views_file = CORE_DIR / 'views.py'
    
    # Criar pacote views se não existir
    if not views_package.exists():
        views_package.mkdir()
        print("✅ Pasta core/views/ criada.")
        
        # Criar __init__.py
        (views_package / '__init__.py').touch()
        
        # Criar os arquivos módulos vazios para você preencher
        modules = ['public.py', 'auth.py', 'aluno.py', 'professor.py', 'ia.py', 'checkout.py']
        for mod in modules:
            (views_package / mod).touch()
            print(f"   📄 Criado: core/views/{mod}")
            
    # Renomear o views.py gigante para backup
    if old_views_file.exists():
        backup_file = CORE_DIR / 'views_old_backup.py'
        shutil.move(str(old_views_file), str(backup_file))
        print(f"📦 core/views.py renomeado para {backup_file.name} (Copie o código dele para os novos módulos!)")

if __name__ == '__main__':
    confirmation = input("Este script vai mover arquivos e alterar a estrutura do projeto. Tem certeza? (s/n): ")
    if confirmation.lower() == 's':
        organizar_templates()
        estruturar_views_core()
        print("\n✨ Organização concluída! Lembre-se de atualizar os caminhos no 'urls.py' e nos 'render()'.")
    else:
        print("Cancelado.")