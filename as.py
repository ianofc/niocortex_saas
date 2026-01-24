import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Configurar ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from core.models import CustomUser
from yourlife.social.models import Group, Event

def run():
    print("--- 🚀 INICIANDO A OPERAÇÃO 'VIDA SOCIAL' ---")

    # 1. Pegar o Admin para ser o dono do conteúdo
    try:
        admin = CustomUser.objects.get(username='iansantos')
        print(f"😎 Influencer Admin: {admin.first_name}")
    except CustomUser.DoesNotExist:
        print("❌ Admin 'iansantos' não encontrado. Crie o superuser primeiro.")
        return

    # ==============================================================================
    # 2. LIMPEZA (APAGAR OS CHATOS)
    # ==============================================================================
    print("\n🧹 Faxina: Removendo grupos e eventos antigos/acadêmicos...")
    deleted_groups = Group.objects.all().delete()
    deleted_events = Event.objects.all().delete()
    print(f"   - Grupos removidos: {deleted_groups[0]}")
    print(f"   - Eventos removidos: {deleted_events[0]}")

    # ==============================================================================
    # 3. LISTA DE 30 GRUPOS (VIBE FACEBOOK/INSTAGRAM)
    # ==============================================================================
    grupos_data = [
        # Hobbies & Games
        ("Gamers NioCortex 🎮", "Valorant, LoL, CS2, FIFA e o que mais tiver rank."),
        ("Otakus Fedidos (com carinho) 🍥", "Animes, Mangás e Cosplay."),
        ("RPG de Mesa & Magic 🎲", "Dungeons & Dragons, Tormenta e Commander."),
        ("Cinéfilos & Séries 🍿", "Discussão de estreias, Netflix e HBO."),
        ("Clube do Livro (Sem obrigação) 📚", "Livros que a gente lê por gosto, não pra prova."),
        ("Artistas de Caderno 🎨", "Desenhos, rabiscos e artes digitais."),
        ("K-Pop Stans 🎵", "BTS, Blackpink, Stray Kids e surtos coletivos."),
        
        # Lifestyle & Cotidiano
        ("Memes & Lendas 🤡", "Poste aqui o que não tem coragem de postar no feed."),
        ("Spotted & Crushes 💘", "Viu alguém interessante? Mande o recado (com respeito)."),
        ("Fofoca Edificante ☕", "Aquele babado que edifica a alma."),
        ("Confissões Anônimas 🤫", "O que acontece no campus, fica no grupo."),
        ("Pets da Galera 🐶", "Só fotos de bichinhos fofos para curar a depressão."),
        ("Moda & Look do Dia 👗", "Dicas de outfit, brechós e promoções."),
        ("Maquiagem & Skincare 💄", "Dicas de produtos e tutoriais."),
        ("Tatuagem & Piercing 💉", "Inspirações, cuidados e recomendações de estúdios."),
        ("Astrologia & Signos 🔮", "Culpe seu signo por tudo o que der errado."),
        
        # Esportes & Saúde
        ("Futebol de Quarta ⚽", "Organização das peladas semanais."),
        ("Fitness & Maromba 💪", "Dicas de treino, dieta e motivação (ou choro)."),
        ("Basquete de Rua 🏀", "Rachas na quadra externa."),
        ("Skatistas & Surfistas 🛹", "Rolês na pista e previsão das ondas."),
        ("Vôlei Misto 🏐", "Treinos e jogos amistosos."),
        
        # Rolês & Comida
        ("Gastronomia & Larica 🍔", "Melhores lugares pra comer e receitas fáceis."),
        ("Baladas & Festas 🎉", "Onde vai ser o fervo do fim de semana?"),
        ("Música & Vibe 🎧", "Compartilhe sua playlist e descubra sons novos."),
        ("Festival de Talentos 🎸", "Pra quem canta, toca ou faz mágica."),
        
        # Tech & Variedades
        ("Programadores da Madrugada 💻", "Café, bugs e código às 3 da manhã."),
        ("Empreendedores Jovens 🚀", "Ideias de negócios e startups."),
        ("Carros & Rebaixados 🚗", "Apaixonados por automotivo."),
        ("Fotografia Amadora 📸", "Fotos conceituais tiradas com o celular."),
        ("Debates Inúteis 🤔", "Biscoito ou Bolacha? Toddy ou Nescau?"),
    ]

    print("\n👥 Criando 30 Grupos novos...")
    for nome, desc in grupos_data:
        g, _ = Group.objects.get_or_create(
            name=nome,
            defaults={
                'description': desc,
                'is_private': False,
                'creator': admin
            }
        )
        g.members.add(admin)
    print("   ✅ Grupos criados com sucesso!")

    # ==============================================================================
    # 4. LISTA DE 30 EVENTOS (FESTAS, JOGOS E ROLÊS)
    # ==============================================================================
    eventos_data = [
        # Próximos dias
        ("Sextou: Resenha Pós-Aula 🍻", "Pizzaria do Centro", 0, "SOCIAL"),
        ("Campeonato de FIFA 26 ⚽", "Área de Convivência", 1, "SOCIAL"),
        ("Luau da Galera 🌙", "Praia / Parque", 2, "SOCIAL"),
        ("Workshop de Make 💄", "Sala Multiuso", 3, "SOCIAL"),
        ("Roda de Violão 🎸", "Jardim do Campus", 4, "SOCIAL"),
        
        # Próxima Semana
        ("Torneio de Truco Valendo Coxinha 🃏", "Cantina", 5, "SOCIAL"),
        ("Sessão Pipoca: Terror 🎃", "Auditório", 6, "SOCIAL"),
        ("Feira de Troca de Livros 📖", "Biblioteca", 7, "ACADEMIC"),
        ("Treinão de Crossfit ao Ar Livre 💪", "Quadra Externa", 8, "SOCIAL"),
        ("Batalha de Rima 🎤", "Pátio Central", 9, "SOCIAL"),
        ("Oficina de Fotografia Mobile 📱", "Lab de Artes", 10, "ACADEMIC"),
        
        # Próximo Mês
        ("Festa à Fantasia (Halloween) 👻", "Salão de Festas", 12, "SOCIAL"),
        ("Campeonato de LoL (Final) 🖥️", "Lab de Informática", 14, "SOCIAL"),
        ("Passeio Ciclístico 🚲", "Saída do Portão Principal", 15, "SOCIAL"),
        ("Show de Talentos 🌟", "Teatro", 18, "SOCIAL"),
        ("Churrasco da Turma 🍖", "Chácara do Tio", 20, "SOCIAL"),
        ("Feira de Profissões e Estágios 💼", "Ginásio", 22, "WORK"),
        ("Hackathon 24h ⚡", "Coworking", 25, "WORK"),
        ("Noite de Jogos de Tabuleiro ♟️", "Sala de Estudos", 27, "SOCIAL"),
        
        # Futuro
        ("Baile de Inverno ❄️", "Clube da Cidade", 35, "SOCIAL"),
        ("Gincana Solidária ❤️", "Escola toda", 40, "SOCIAL"),
        ("Festival de Bandas Independentes 🤘", "Estacionamento", 45, "SOCIAL"),
        ("Campeonato de Skate 🛹", "Pista Municipal", 50, "SOCIAL"),
        ("Maratona de Séries (Noite do Pijama) 😴", "Casa da Ana", 55, "SOCIAL"),
        ("Workshop de Investimentos 💰", "Auditório B", 60, "WORK"),
        ("Curso de Defesa Pessoal 🥋", "Dojo", 65, "SOCIAL"),
        ("Concurso de Cosplay 🦹", "Pátio", 70, "SOCIAL"),
        ("Pool Party de Encerramento 🏊", "Clube", 80, "SOCIAL"),
        ("Formatura (Expectativa) 🎓", "Arena", 90, "ACADEMIC"),
        ("Viagem de Férias 🚌", "Porto Seguro", 100, "SOCIAL"),
    ]

    print("\n📅 Criando 30 Eventos novos...")
    hoje = timezone.now()
    
    for titulo, local, dias, tipo in eventos_data:
        data_inicio = hoje + timedelta(days=dias)
        # Define hora aleatória entre 14h e 20h
        hora = random.randint(14, 20)
        data_inicio = data_inicio.replace(hour=hora, minute=0)
        
        e, _ = Event.objects.get_or_create(
            title=titulo,
            defaults={
                'description': f"Evento imperdível! Venha participar do {titulo}. Mais infos no grupo.",
                'location': local,
                'start_time': data_inicio,
                'end_time': data_inicio + timedelta(hours=4),
                'creator': admin,
                'event_type': tipo,
                'is_online': False
            }
        )
        e.participants.add(admin)
    
    print("   ✅ Eventos criados com sucesso!")
    print("\n🎉 CONCLUÍDO! O YourLife agora está bombando de conteúdo.")

if __name__ == "__main__":
    run()