# niocortex/core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # ==========================================================================
    # 1. PÁGINAS PÚBLICAS (INSTITUCIONAL)
    # ==========================================================================
    path('', views.index, name='index'),
    path('sobre/', views.about, name='about'),
    path('planos/', views.pricing, name='pricing'),
    path('contato/', views.contact, name='contact'),
    path('demo/', views.demo, name='demo'),

    # --- Landing Pages de Funcionalidades ---
    path('funcionalidades/financeiro/', views.feature_financial, name='feature_financial'),
    path('funcionalidades/diario/', views.feature_diary, name='feature_diary'),

    # --- Suporte, Status e Legal ---
    path('status/', views.system_status, name='system_status'),
    path('ajuda/', views.help_center, name='help_center'),
    path('privacidade/', views.privacy_policy, name='privacy_policy'),
    path('termos/', views.terms_of_use, name='terms_of_use'),


    # ==========================================================================
    # 2. AUTENTICAÇÃO
    # ==========================================================================
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),


    # ==========================================================================
    # 3. DASHBOARDS (ÁREA LOGADA)
    # ==========================================================================
    path('dashboard/', views.dashboard_router_view, name='dashboard'),
    path('dashboard/gestao/', views.corporate_dashboard, name='corporate_dashboard'),
    path('dashboard/professor/', views.professor_dashboard, name='professor_dashboard'),
    
    # --- Dashboard Principal do Aluno ---
    path('dashboard/aluno/', views.aluno_dashboard, name='aluno_dashboard'),


    # ==========================================================================
    # 4. PORTAL DO ALUNO (SUB-PÁGINAS)
    # ==========================================================================
    path('dashboard/aluno/perfil/', views.student_profile, name='student_profile'),
    path('dashboard/aluno/disciplinas/', views.student_subjects, name='student_subjects'),
    path('dashboard/aluno/boletim/', views.student_grades, name='student_grades'),
    path('dashboard/aluno/agenda/', views.student_calendar, name='student_calendar'),
    path('dashboard/aluno/arquivos/', views.student_files, name='student_files'),
    path('dashboard/aluno/aula/', views.student_lesson, name='student_lesson'),
    path('dashboard/aluno/atividade/', views.student_activity, name='student_activity'),
    path('dashboard/aluno/financeiro/', views.student_financial, name='student_financial'),
    path('dashboard/aluno/servicos/', views.student_services, name='student_services'),


    # ==========================================================================
    # 5. INTEGRAÇÃO IA (IO CONSCIOS)
    # ==========================================================================
    path('api/ia/check/', views.api_check_conscios, name='api_check_conscios'),
    path('api/ia/chat/', views.api_chat_conscios, name='api_chat_conscios'),


    # ==========================================================================
    # 6. CHECKOUT & PAGAMENTOS
    # ==========================================================================
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/processar/', views.processar_pagamento, name='processar_pagamento'),
    path('checkout/sucesso/', views.checkout_sucesso, name='checkout_sucesso'),
    
    # Rotas de fallback para evitar erro 404 no retorno do MP
    path('checkout/erro/', views.pricing, name='checkout_erro'),
    path('checkout/pendente/', views.pricing, name='checkout_pendente'),
]