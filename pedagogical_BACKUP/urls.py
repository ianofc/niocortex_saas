# niocortex/pedagogical/urls.py

from django.urls import path
from . import views

app_name = 'pedagogical'

urlpatterns = [
    # --- Gestão de Turmas ---
    path('turmas/', views.listar_turmas, name='listar_turmas'),
    
    # CORREÇÃO: O template chama 'criar_turma', mas a view é 'form_turmas'. 
    # Vamos adicionar o nome que o template espera.
    path('turmas/nova/', views.form_turmas, name='form_turmas'), 
    path('turmas/nova/alias/', views.form_turmas, name='criar_turma'), # Alias para evitar erro no template antigo

    path('turmas/<int:turma_id>/', views.detalhar_turma, name='detalhar_turma'),
    
    # CORREÇÃO: O nome da função na view provavelmente é 'excluir_turma', mas a url chamava 'exclusao_turmas'
    path('turmas/<int:turma_id>/excluir/', views.excluir_turma, name='excluir_turma'), 

    # --- Ferramentas Pedagógicas ---
    path('planejamento/gerador/', views.gerador_planejamentos, name='gerador_planejamentos'),
    
    # CORREÇÃO: Adicionada a rota da API que estava faltando e dando erro 500
    path('api/planejamento/gerar/', views.api_gerar_planejamento, name='api_gerar_planejamento'),
    
    path('atividades/gerador/', views.gerador_atividades, name='gerador_atividades'),
    path('provas/gerador/', views.gerador_provas, name='gerador_provas'),

    # --- Gradebook / Notas ---
    path('notas/', views.gradebook_view, name='gradebook'),
]
