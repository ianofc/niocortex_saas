# hr/urls.py

from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    # Funcionários
    path('funcionarios/', views.listar_funcionarios, name='listar_funcionarios'),
    path('funcionarios/novo/', views.criar_funcionario, name='criar_funcionario'),
    
    # Departamentos
    path('departamentos/', views.listar_departamentos, name='listar_departamentos'),
    path('departamentos/novo/', views.criar_departamento, name='criar_departamento'),
    
    # Cargos
    path('cargos/', views.listar_cargos, name='listar_cargos'),
    path('cargos/novo/', views.criar_cargo, name='criar_cargo'),
]