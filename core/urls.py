# niocortex/core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # --- AUTENTICAÇÃO ---
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # --- DASHBOARDS (ROUTER) ---
    # A rota 'dashboard' é o cérebro que decide para onde o usuário vai
    path('dashboard/', views.dashboard_router_view, name='dashboard'),
    
    # Rotas específicas (protegidas por @login_required e verificação de Role)
    path('dashboard/professor/', views.professor_dashboard, name='professor_dashboard'),
    path('dashboard/aluno/', views.aluno_dashboard, name='aluno_dashboard'),
    path('dashboard/gestao/', views.corporate_dashboard, name='corporate_dashboard'),
    
    # Rota index opcional (pode redirecionar para login ou dashboard)
    path('', views.login_view, name='index'), 
]