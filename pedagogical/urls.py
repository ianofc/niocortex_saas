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
]