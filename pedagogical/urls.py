from django.urls import path
from . import views

app_name = 'pedagogical'

urlpatterns = [
    # --- TURMAS ---
    path('turmas/', views.lista_turmas, name='lista_turmas'),
    path('turmas/nova/', views.criar_turma, name='criar_turma'),
    path('turmas/<int:turma_id>/', views.detalhe_turma, name='detalhe_turma'),
    path('turmas/<int:turma_id>/editar/', views.editar_turma, name='editar_turma'),
    path('turmas/<int:turma_id>/excluir/', views.excluir_turma, name='excluir_turma'),

    # --- ALUNOS ---
    path('turmas/<int:turma_id>/alunos/novo/', views.adicionar_aluno, name='adicionar_aluno'),
    path('alunos/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('alunos/<int:aluno_id>/excluir/', views.excluir_aluno, name='excluir_aluno'),
]