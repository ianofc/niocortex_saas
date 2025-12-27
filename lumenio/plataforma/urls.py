from django.urls import path
from . import views

urlpatterns = [
    # Aluno
    path('aluno/home/', views.dashboard_aluno, name='dashboard_aluno'),
    path('curso/<int:curso_id>/aula/', views.sala_de_aula, name='sala_de_aula'),
    
    # Professor
    path('professor/gestao/', views.dashboard_professor, name='dashboard_professor'),
    path('professor/novo-curso/', views.criar_curso, name='criar_curso'),
]