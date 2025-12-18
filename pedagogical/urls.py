# niocortex/pedagogical/urls.py

from django.urls import path
from . import views

app_name = 'pedagogical'

urlpatterns = [
    # --- TURMAS ---
    # name='listar_turmas' alinhado com o redirect das views
    path('turmas/', views.listar_turmas_view, name='listar_turmas'),
    path('turmas/nova/', views.criar_turma_view, name='criar_turma'),
    
    path('turmas/<int:turma_id>/', views.detalhe_turma, name='detalhe_turma'),
    path('turmas/<int:turma_id>/editar/', views.editar_turma, name='editar_turma'),
    path('turmas/<int:turma_id>/excluir/', views.excluir_turma, name='excluir_turma'),

    # --- ALUNOS ---
    path('turmas/<int:turma_id>/alunos/novo/', views.adicionar_aluno, name='adicionar_aluno'),
    path('alunos/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('alunos/<int:aluno_id>/excluir/', views.excluir_aluno, name='excluir_aluno'),

    # --- API / IA (Integração com FastAPI) ---
    # Rota AJAX chamada pelo JavaScript para análise de desempenho
    path('api/analisar-aluno/<int:aluno_id>/', views.analisar_desempenho_aluno, name='analisar_aluno_ia'),

    # Gradebook (Já adicionado anteriormente)
    path('turma/<uuid:turma_id>/gradebook/', views.gradebook, name='gradebook'),
    path('api/notas/lancar/', views.api_lancar_nota, name='api_lancar_nota'),

    # --- GERADOR DE PROVAS (NOVO) ---
    path('ferramentas/gerador-provas/', views.view_gerador_provas, name='gerador_provas'),
    path('api/ferramentas/gerar-prova/', views.api_gerar_prova, name='api_gerar_prova'),

# --- FERRAMENTAS IA (COPILOTO) ---
    
    # 1. Provas
    path('ferramentas/provas/', views.view_gerador_provas, name='gerador_provas'),
    path('api/ferramentas/gerar-prova/', views.api_gerar_prova, name='api_gerar_prova'),
    
    # 2. Planejamentos (Planos de Aula)
    path('ferramentas/planejamentos/', views.view_gerador_planejamentos, name='gerador_planejamentos'),
    path('api/ferramentas/gerar-plano/', views.api_gerar_planejamento, name='api_gerar_planejamento'),
    
    # 3. Atividades (Exercícios)
    path('ferramentas/atividades/', views.view_gerador_atividades, name='gerador_atividades'),
    path('api/ferramentas/gerar-atividade/', views.api_gerar_atividade, name='api_gerar_atividade'),
]
