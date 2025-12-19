# niocortex/core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # --- PÁGINAS PÚBLICAS (AURORA UI) ---
    path('', views.index, name='index'),          # Raiz do site
    path('planos/', views.pricing, name='pricing'),
    path('contato/', views.contact, name='contact'),
    path('demo/', views.demo, name='demo'),

    # --- AUTENTICAÇÃO ---
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # --- DASHBOARDS (ÁREA LOGADA) ---
    path('dashboard/', views.dashboard_router_view, name='dashboard'),
    path('dashboard/professor/', views.professor_dashboard, name='professor_dashboard'),
    path('dashboard/aluno/', views.aluno_dashboard, name='aluno_dashboard'),
    path('dashboard/gestao/', views.corporate_dashboard, name='corporate_dashboard'),

    path('checkout/', views.checkout, name='checkout'),
    
    # Rota que PROCESSA o formulário (POST)
    path('checkout/processar/', views.processar_pagamento, name='processar_pagamento'),
    
    # Rotas de Retorno
    path('checkout/sucesso/', views.checkout_sucesso, name='checkout_sucesso'),
]