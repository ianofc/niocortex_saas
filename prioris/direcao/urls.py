from django.urls import path
from . import views

app_name = 'prioris_direcao'

urlpatterns = [
    path('', views.dashboard_direcao, name='dashboard'),
    # Futuras rotas: path('metas/nova', views.criar_meta, ...),
]