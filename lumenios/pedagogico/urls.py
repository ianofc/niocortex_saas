from django.urls import path
from . import views

app_name = 'pedagogico'

urlpatterns = [
    # Turmas (IDs corrigidos para UUID)
    path('turmas/', views.listar_turmas, name='listar_turmas'),
    path('turmas/nova/', views.criar_turma, name='form_turmas'),
    path('turmas/<uuid:turma_id>/', views.detalhar_turma, name='detalhar_turma'),
    path('turmas/<uuid:turma_id>/adicionar-aluno/', views.adicionar_aluno_turma, name='adicionar_aluno_turma'),
    
    # Alunos
    path('alunos/', views.listar_alunos, name='listar_alunos'),
    path('alunos/novo/', views.criar_aluno, name='criar_aluno'),
    
    # Gradebook
    path('gradebook/', views.gradebook_view, name='gradebook'),
    
    # Ferramentas
    path('ferramentas/atividades/', views.gerador_atividades, name='gerador_atividades'),
    path('api/gerar-atividade/', views.api_gerar_atividade, name='api_gerar_atividade'),
    
    path('ferramentas/provas/', views.gerador_provas, name='gerador_provas'),
    path('ferramentas/provas/gerar-docx/', views.gerar_prova_docx, name='gerar_prova_docx'),
    
    path('ferramentas/planejamento/', views.gerador_planejamentos, name='gerador_planejamentos'),
    path('api/gerar-planejamento/', views.api_gerar_planejamento, name='api_gerar_planejamento'),
]
