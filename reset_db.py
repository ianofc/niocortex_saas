import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

with connection.cursor() as cursor:
    print("Apagando tabelas conflitantes...")
    # Apaga tabelas financeiras e pedagógicas para recriar limpo
    cursor.execute("DROP TABLE IF EXISTS financial_transacao CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS financial_contratoaluno CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS financial_boletoaluno CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS financial_patrimonio CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS financial_fornecedor CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS financial_pedidocompra CASCADE;")

    cursor.execute("DROP TABLE IF EXISTS pedagogical_aluno CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS pedagogical_turma CASCADE;")

    # Limpa o histórico de migrações desses apps
    cursor.execute("DELETE FROM django_migrations WHERE app IN ('pedagogical', 'financial');")
    print("Tabelas limpas! Agora pode rodar o migrate.")