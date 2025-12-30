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
    path('ferramentas/provas/', views.gerador_provas, name='gerador_provas'),
]