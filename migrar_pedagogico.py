import os
import shutil

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos
OLD_APP_DIR = os.path.join(BASE_DIR, 'pedagogical')
OLD_TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates', 'pedagogical')

NEW_APP_DIR = os.path.join(BASE_DIR, 'lumenios', 'pedagogico')
NEW_TEMPLATES_DIR = os.path.join(BASE_DIR, 'lumenios', 'templates', 'pedagogico')

# ==============================================================================
# 1. CÓDIGO DO BACKEND (LUMENIOS.PEDAGOGICO)
# ==============================================================================

apps_py = """
from django.apps import AppConfig

class PedagogicoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lumenios.pedagogico'
    verbose_name = 'Gestão Pedagógica (Lumenios)'
"""

models_py = """
from django.db import models
from django.conf import settings

# Exemplo de Modelo de Turma Integrado
class Turma(models.Model):
    nome = models.CharField(max_length=100)
    ano_letivo = models.IntegerField(default=2025)
    professor_regente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='turmas_regente')
    
    def __str__(self):
        return f"{self.nome} ({self.ano_letivo})"

class AlunoTurma(models.Model):
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matriculas_turma')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='alunos')
    data_matricula = models.DateField(auto_now_add=True)
"""

views_py = """
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# --- GESTÃO DE ALUNOS ---
@login_required
def listar_alunos(request):
    return render(request, 'pedagogico/alunos/listar_alunos.html')

@login_required
def form_alunos(request):
    return render(request, 'pedagogico/alunos/form_alunos.html')

# --- GESTÃO DE TURMAS ---
@login_required
def listar_turmas(request):
    return render(request, 'pedagogico/turmas/listar_turmas.html')

@login_required
def detalhar_turma(request, turma_id):
    return render(request, 'pedagogico/turmas/detalhar_turmas.html')

# --- FERRAMENTAS PEDAGÓGICAS ---
@login_required
def gradebook(request):
    return render(request, 'pedagogico/gradebook/gradebook.html')

@login_required
def gerador_atividades(request):
    return render(request, 'pedagogico/ferramentas/gerador_atividades.html')
"""

urls_py = """
from django.urls import path
from . import views

app_name = 'pedagogico'

urlpatterns = [
    # Alunos
    path('alunos/', views.listar_alunos, name='listar_alunos'),
    path('alunos/novo/', views.form_alunos, name='novo_aluno'),
    
    # Turmas
    path('turmas/', views.listar_turmas, name='listar_turmas'),
    path('turmas/<int:turma_id>/', views.detalhar_turma, name='detalhar_turma'),
    
    # Ferramentas
    path('gradebook/', views.gradebook, name='gradebook'),
    path('ferramentas/atividades/', views.gerador_atividades, name='gerador_atividades'),
]
"""

# ==============================================================================
# 2. FUNÇÕES DO SCRIPT
# ==============================================================================

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Criado: {path}")

def mover_templates():
    print(f"\n📦 Movendo templates de '{OLD_TEMPLATES_DIR}' para '{NEW_TEMPLATES_DIR}'...")
    
    if not os.path.exists(OLD_TEMPLATES_DIR):
        print("⚠️ Pasta de templates antiga não encontrada. Criando estrutura nova vazia.")
        os.makedirs(NEW_TEMPLATES_DIR, exist_ok=True)
        return

    # Copia a estrutura de pastas
    if os.path.exists(NEW_TEMPLATES_DIR):
        shutil.rmtree(NEW_TEMPLATES_DIR)
    
    shutil.copytree(OLD_TEMPLATES_DIR, NEW_TEMPLATES_DIR)
    
    # Renomeia a pasta antiga para backup
    backup_path = OLD_TEMPLATES_DIR + "_BACKUP"
    if os.path.exists(backup_path):
        shutil.rmtree(backup_path)
    os.rename(OLD_TEMPLATES_DIR, backup_path)
    
    print("✅ Templates movidos com sucesso!")

def configurar_nova_app():
    print(f"\n⚙️ Configurando nova app 'lumenios.pedagogico'...")
    
    # Cria a estrutura da app
    create_file(os.path.join(NEW_APP_DIR, '__init__.py'), "")
    create_file(os.path.join(NEW_APP_DIR, 'apps.py'), apps_py)
    create_file(os.path.join(NEW_APP_DIR, 'models.py'), models_py)
    create_file(os.path.join(NEW_APP_DIR, 'views.py'), views_py)
    create_file(os.path.join(NEW_APP_DIR, 'urls.py'), urls_py)
    
    # Desativa a app antiga na raiz se existir
    if os.path.exists(OLD_APP_DIR):
        backup_app = OLD_APP_DIR + "_BACKUP"
        if os.path.exists(backup_app):
            shutil.rmtree(backup_app)
        os.rename(OLD_APP_DIR, backup_app)
        print("✅ App antiga 'pedagogical' renomeada para backup.")

def atualizar_settings_urls_principais():
    print("\n🔗 Atualizando configurações principais...")
    
    # 1. Settings (Adicionar lumenios.pedagogico)
    settings_path = os.path.join(BASE_DIR, 'niocortex', 'settings.py')
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "'lumenios.pedagogico'" not in content:
        # Tenta substituir a antiga ou adicionar a nova
        if "'pedagogical.apps.PedagogicalConfig'" in content:
            content = content.replace("'pedagogical.apps.PedagogicalConfig'", "'lumenios.pedagogico'")
        elif "'pedagogical'" in content:
            content = content.replace("'pedagogical'", "'lumenios.pedagogico'")
        else:
            # Adiciona no final de INSTALLED_APPS se não achar a antiga
            content = content.replace("INSTALLED_APPS = [", "INSTALLED_APPS = [\n    'lumenios.pedagogico',")
        
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ settings.py atualizado.")

    # 2. URLs Principal (Incluir rotas pedagógicas)
    urls_path = os.path.join(BASE_DIR, 'niocortex', 'urls.py')
    with open(urls_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "lumenios.pedagogico.urls" not in content:
        # Adiciona a rota
        new_path = "\n    path('lumenios/pedagogico/', include('lumenios.pedagogico.urls')),"
        content = content.replace("urlpatterns = [", "urlpatterns = [" + new_path)
        
        with open(urls_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ urls.py principal atualizado.")

# ==============================================================================
# EXECUÇÃO
# ==============================================================================

def main():
    print("🚀 Migrando Módulo Pedagógico para o AVA Lumenios...\n")
    mover_templates()
    configurar_nova_app()
    atualizar_settings_urls_principais()
    print("\n✨ Migração Concluída!")
    print("⚠️ IMPORTANTE: Como mudamos os modelos de lugar, rode:")
    print("   python manage.py makemigrations lumenios")
    print("   python manage.py migrate")

if __name__ == "__main__":
    main()