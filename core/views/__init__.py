# Apenas o que é interno do sistema acadêmico
from .auth import dashboard_router_view
from .professor import professor_dashboard, corporate_dashboard, teacher_schedule
from .aluno import aluno_dashboard, student_profile, student_subjects, student_grades # etc...
from .ia import talkio_view, api_check_zios, api_chat_zios
