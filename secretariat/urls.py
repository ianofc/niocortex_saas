# secretariat/urls.py

from django.urls import path
from . import views

app_name = 'secretariat'

urlpatterns = [
    # Modelos
    path('modelos/', views.listar_modelos, name='listar_modelos'),
    path('modelos/novo/', views.criar_modelo, name='criar_modelo'),
    
    # Emissão
    path('emitir/', views.selecionar_aluno_emissao, name='selecionar_aluno'),
    path('emitir/<uuid:aluno_id>/', views.gerar_documento, name='gerar_documento'),
    path('visualizar/<uuid:doc_id>/', views.visualizar_documento, name='visualizar_documento'),
]