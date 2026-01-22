from django.urls import path
from .views import professor, aluno, ia, auth

app_name = 'core'

urlpatterns = [
    # O Router 'app/' ainda existe para redirecionar quem tentar acessar direto,
    # mas agora ele vai mandar para o social por padrão.
    path('app/', auth.dashboard_router_view, name='dashboard'),

    # --- Dashboards Específicos (Lumenios) ---
    path('app/gestao/', professor.corporate_dashboard, name='corporate_dashboard'),
    path('app/professor/', professor.professor_dashboard, name='professor_dashboard'),
    path('app/professor/horario/', professor.teacher_schedule, name='teacher_schedule'),
    path('app/aluno/', aluno.aluno_dashboard, name='aluno_dashboard'),

    # --- Funcionalidades do Aluno (Mantém igual) ---
    path('app/aluno/perfil/', aluno.student_profile, name='student_profile'),
    path('app/aluno/disciplinas/', aluno.student_subjects, name='student_subjects'),
    path('app/aluno/boletim/', aluno.student_grades, name='student_grades'),
    path('app/aluno/agenda/', aluno.student_calendar, name='student_calendar'),
    path('app/aluno/horario/', aluno.student_timetable, name='student_timetable'),
    path('app/aluno/arquivos/', aluno.student_files, name='student_files'),
    path('app/aluno/aula/', aluno.student_lesson, name='student_lesson'),
    path('app/aluno/atividade/', aluno.student_activity, name='student_activity'),
    
    path('app/aluno/financeiro/', aluno.student_financial, name='student_financial'),
    path('app/aluno/servicos/', aluno.student_services, name='student_services'),
    path('identidade/', aluno.student_id_card, name='carteirinha'),
    
    path('app/aluno/diario/', aluno.daily_diary, name='daily_diary'),
    path('app/aluno/loja/', aluno.gamification_store, name='gamification_store'),
    path('app/aluno/biblioteca/', aluno.student_library, name='student_library'),
    path('app/aluno/carreira/', aluno.career_center, name='career_center'),
    path('app/aluno/tcc/', aluno.thesis_manager, name='thesis_manager'),


    # --- IA ---
    path('talkio/', ia.talkio_view, name='talkio'),
    path('api/ia/check/', ia.api_check_zios, name='api_check_zios'),
    path('api/ia/chat/', ia.api_chat_zios, name='api_chat_zios'),
]