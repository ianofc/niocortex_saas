# niocortex/core/urls.py

from django.urls import path, include
from .views.professor import professor_dashboard, corporate_dashboard
from .views.aluno import (
    aluno_dashboard, student_profile, student_subjects, student_grades, student_calendar,
    student_timetable, student_files, student_lesson, student_activity, student_financial,
    student_services, student_id_card, daily_diary, gamification_store, student_library,
    career_center, thesis_manager, student_premium, student_premium_stats
)
from .views.public import (
    index, about, pricing, contact, demo, feature_financial, feature_diary, system_status,
    help_center, privacy_policy, terms_of_use, login_view, register_view, logout_view,
    dashboard_router_view, talkio_view, api_check_conscios, api_chat_conscios, checkout,
    processar_pagamento, checkout_sucesso
)

app_name = 'core'

urlpatterns = [
    # ==========================================================================
    # 1. PÁGINAS PÚBLICAS (INSTITUCIONAL)
    # ==========================================================================
    path('', index, name='index'),
    path('sobre/', about, name='about'),
    path('planos/', pricing, name='pricing'),
    path('contato/', contact, name='contact'),
    path('demo/', demo, name='demo'),

    # --- Landing Pages de Funcionalidades ---
    path('funcionalidades/financeiro/', feature_financial, name='feature_financial'),
    path('funcionalidades/diario/', feature_diary, name='feature_diary'),

    # --- Suporte, Status e Legal ---
    path('status/', system_status, name='system_status'),
    path('ajuda/', help_center, name='help_center'),
    path('privacidade/', privacy_policy, name='privacy_policy'),
    path('termos/', terms_of_use, name='terms_of_use'),


    # ==========================================================================
    # 2. AUTENTICAÇÃO
    # ==========================================================================
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),


    # ==========================================================================
    # 3. DASHBOARDS (ÁREA LOGADA)
    # ==========================================================================
    path('dashboard/', dashboard_router_view, name='dashboard'),
    path('dashboard/gestao/', corporate_dashboard, name='corporate_dashboard'),
    path('dashboard/professor/', professor_dashboard, name='professor_dashboard'),
    
    # --- Dashboard Principal do Aluno ---
    path('dashboard/aluno/', aluno_dashboard, name='aluno_dashboard'),


    # ==========================================================================
    # 4. PORTAL DO ALUNO (FUNCIONALIDADES)
    # ==========================================================================
    
    # --- Essenciais ---
    path('dashboard/aluno/perfil/', student_profile, name='student_profile'),
    path('dashboard/aluno/disciplinas/', student_subjects, name='student_subjects'),
    path('dashboard/aluno/boletim/', student_grades, name='student_grades'),
    path('dashboard/aluno/agenda/', student_calendar, name='student_calendar'),
    path('dashboard/aluno/horario/', student_timetable, name='student_timetable'), # <--- NOVA ROTA
    path('dashboard/aluno/arquivos/', student_files, name='student_files'),
    path('dashboard/aluno/aula/', student_lesson, name='student_lesson'),
    path('dashboard/aluno/atividade/', student_activity, name='student_activity'),
    
    # --- Administrativo ---
    path('dashboard/aluno/financeiro/', student_financial, name='student_financial'),
    path('dashboard/aluno/servicos/', student_services, name='student_services'),
    path('dashboard/aluno/carteirinha/', student_id_card, name='student_id_card'),
    
    # --- Módulos Específicos (Novos) ---
    path('dashboard/aluno/diario/', daily_diary, name='daily_diary'),           # Infantil
    path('dashboard/aluno/loja/', gamification_store, name='gamification_store'), # Gamificação
    path('dashboard/aluno/biblioteca/', student_library, name='student_library'), # Todos
    path('dashboard/aluno/carreira/', career_center, name='career_center'),     # Superior
    path('dashboard/aluno/tcc/', thesis_manager, name='thesis_manager'),        # Pós/Superior

    # --- Premium ---
    path('dashboard/aluno/premium/', student_premium, name='student_premium'),
    path('dashboard/aluno/premium/stats/', student_premium_stats, name='student_premium_stats'),


    # ==========================================================================
    # 5. COMUNICAÇÃO & IA
    # ==========================================================================
    path('talkio/', talkio_view, name='talkio'), # Chat Full Screen
    path('api/ia/check/', api_check_conscios, name='api_check_conscios'),
    path('api/ia/chat/', api_chat_conscios, name='api_chat_conscios'),


    # ==========================================================================
    # 6. CHECKOUT & PAGAMENTOS
    # ==========================================================================
    path('checkout/', checkout, name='checkout'),
    path('checkout/processar/', processar_pagamento, name='processar_pagamento'),
    path('checkout/sucesso/', checkout_sucesso, name='checkout_sucesso'),
    
    # Rotas de fallback para evitar erro 404 no retorno do MP
    path('checkout/erro/', pricing, name='checkout_erro'),
    path('checkout/pendente/', pricing, name='checkout_pendente'),

    # ==========================================================================
    # INCLUSÃO DE URLs DOS NOVOS APPS
    # ==========================================================================
    path('pedagogical/', include('pedagogical.urls')),
    path('financial/', include('financial.urls')),
    path('hr/', include('hr.urls')),
    path('secretariat/', include('secretariat.urls')),
    path('crm_sales/', include('crm_sales.urls')),
]