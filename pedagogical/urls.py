# niocortex/pedagogical/urls.py

from django.urls import path
from . import views

app_name = 'pedagogical'

urlpatterns = [
    # Gestão de Turmas
    path('turmas/', views.listar_turmas, name='listar_turmas'),
    path('turmas/nova/', views.form_turmas, name='criar_turma'),  # Alterado para 'criar_turma'
    path('turmas/<int:turma_id>/', views.detalhar_turma, name='detalhar_turma'),
    path('turmas/<int:turma_id>/excluir/', views.excluir_turma, name='excluir_turma'),

    # Ferramentas Pedagógicas
    path('planejamento/gerador/', views.gerador_planejamentos, name='gerador_planejamentos'),
    path('api/planejamento/gerar/', views.api_gerar_planejamento, name='api_gerar_planejamento'),  # Adicionado
    path('atividades/gerador/', views.gerador_atividades, name='gerador_atividades'),
    path('provas/gerador/', views.gerador_provas, name='gerador_provas'),

    # Gradebook e Diário
    path('notas/', views.gradebook_view, name='gradebook'),
]
