from django.urls import path
from . import views

app_name = 'lumenios'

urlpatterns = [
    # --- Rota do Aluno (Consumo) ---
    path('sala/painel/', views.aluno_painel_cursos, name='aluno_painel'),
    path('sala/<int:sala_id>/', views.aluno_player, name='aluno_player'),
    path('api/concluir/<int:material_id>/', views.marcar_concluido, name='api_concluir'),

    # --- Rota do Professor (Gestão) ---
    path('gestao/painel/', views.professor_painel, name='professor_painel'),
    path('gestao/editor/<int:sala_id>/', views.professor_editor, name='professor_editor'),
    path('gestao/criar_modulo/<int:sala_id>/', views.criar_modulo, name='criar_modulo'),
    path('gestao/upload_material/<int:modulo_id>/', views.upload_material, name='upload_material'),
]
