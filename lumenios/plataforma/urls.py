from django.urls import path
from . import views

app_name = 'lumenios'

urlpatterns = [
    # Aluno
    path('aluno/home/', views.dashboard_aluno, name='dashboard_aluno'),
    
    path('aluno/biblioteca/', views.biblioteca_aluno, name='biblioteca'),
    path('aluno/disciplinas/', views.listar_disciplinas, name='disciplinas'),
    
    path('curso/<int:curso_id>/aula/', views.sala_de_aula, name='sala_de_aula'),
    
    path('aluno/conscios/', views.conscios_investigate, name='conscios'),
    
    path('extras/aula/demo/', views.sala_de_aula_demo, name='sala_de_aula_demo'),

    path('aluno/desempenho/', views.desempenho_analytics, name='desempenho'),
    
    path('extras/complementar/', views.ensino_complementar, name='complementar'),

    path('extras/avaliacoes/', views.avaliacoes_aluno, name='avaliacoes'),
    
    # Professor
    path('professor/gestao/', views.dashboard_professor, name='dashboard_professor'),
    path('professor/novo-curso/', views.criar_curso, name='criar_curso'),
]