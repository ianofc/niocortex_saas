# niocortex_saas/core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Autenticação
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Redirecionamento de Dashboard (A Home principal após login)
    path('dashboard/', views.dashboard_router_view, name='dashboard'),
    
    # Rotas base para Redirecionamento (PLACEHOLDERS)
    path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('aluno/dashboard/', views.aluno_dashboard, name='aluno_dashboard'),
    path('admin_corp/', views.corporate_admin_dashboard, name='corporate_admin_dashboard'),
]