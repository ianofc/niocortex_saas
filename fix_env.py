import os

# Conteúdo limpo e estritamente ASCII/UTF-8
content = """GOOGLE_API_KEY=AIzaSyB6DwoSUU6k62S_FlAppARn4ZC15-h2_q4
DATABASE_URL=postgresql://postgres.qnknyonohlorjfhzkkpz:2511CorteXEduc@db.qnknyonohlorjfhzkkpz.supabase.co:5432/postgres
SECRET_KEY=django-insecure-&x%3al(7-!7@9)9#^9k!p1$q(0_u&n+m!5z)h&s+d$8@a
DEBUG=True
"""

file_path = os.path.join(os.getcwd(), '.env')

# Força a gravação em UTF-8 removendo qualquer formatação anterior
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content.strip())

print(f"✅ Arquivo .env recriado com sucesso (UTF-8) em: {file_path}")