from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Exists, OuterRef, Prefetch, Q
from django.utils import timezone
from ..models import Post, Story, Like, Comentario
from datetime import datetime
import random

# --- CONFIGURAÇÃO DE IMAGENS PADRÃO (SIMULANDO IA) ---
# DICA: Salve imagens reais nessas pastas em 'yourlife/social/static/social/img/system/'
# Isso evita custos de API e geração infinita, mantendo a personalização.
SYSTEM_IMAGES = {
    'welcome': {
        'M': ['welcome_male_1.jpg', 'welcome_male_2.jpg'], # Ex: Homem olhando horizonte futurista
        'F': ['welcome_female_1.jpg', 'welcome_female_2.jpg'], # Ex: Mulher em ambiente criativo
        'N': ['welcome_neutral.jpg'] # Ex: Logo 3D do App
    },
    'birthday': {
        'M': ['bday_male.jpg'],
        'F': ['bday_female.jpg'],
        'N': ['bday_cake.jpg']
    },
    'location': {
        'M': ['travel_male.jpg'], # Ex: Homem mochileiro
        'F': ['travel_female.jpg'], # Ex: Mulher turista
        'N': ['travel_map.jpg']
    },
    'career': {
        'M': ['work_male.jpg'],
        'F': ['work_female.jpg'],
        'N': ['work_office.jpg']
    }
}

def get_smart_image(event_type, user):
    """
    Seleciona uma imagem estática baseada no gênero do perfil e tipo de evento.
    Retorna o caminho URL estático.
    """
    # 1. Tenta detectar gênero (Padrão: Neutro)
    gender = 'N'
    if hasattr(user, 'profile') and user.profile.genero:
        # Assume que o campo genero pode ser 'Masculino', 'M', 'Feminino', 'F'
        g = str(user.profile.genero).upper()
        if g.startswith('M'): 
            gender = 'M'
        elif g.startswith('F'): 
            gender = 'F'
    
    # 2. Busca a lista de imagens para esse contexto
    # Se não achar o tipo de evento ou gênero, usa fallback para lista Neutra
    images_list = SYSTEM_IMAGES.get(event_type, {}).get(gender)
    
    if not images_list:
        images_list = SYSTEM_IMAGES.get(event_type, {}).get('N', ['default_card.jpg'])
    
    # 3. Escolhe aleatoriamente para dar sensação de novidade
    selected_img = random.choice(images_list)
    
    return f"/static/social/img/system/{selected_img}"

# --- CLASSE AUXILIAR PARA EVENTOS DO SISTEMA ---
class SystemEventPost:
    """
    Simula um objeto 'Post' completo para ser exibido quando o feed está vazio.
    """
    def __init__(self, user, content, date, event_type=None, force_image=None):
        self.autor = user
        self.conteudo = content
        self.data_criacao = date
        
        # Lógica de Imagem: Se forçada, usa ela. Se não, usa a IA simulada.
        if force_image:
            self.imagem = force_image
        elif event_type:
            self.imagem = get_smart_image(event_type, user)
        else:
            self.imagem = None
            
        self.video = None
        
        # Campos virtuais para compatibilidade com o template (Evita erros de atributo)
        self.pk = 0
        self.id = 0
        self.total_likes = 0
        self.total_comentarios = 0
        self.user_liked = False
        self.is_system_event = True # Flag crucial para o template

@login_required
def home_feed(request):
    """
    Feed Principal Otimizado.
    1. Bloqueia acesso de 'Bebê'.
    2. Processa novos posts.
    3. Busca posts reais com alta performance.
    4. Se vazio, gera eventos visuais baseados no perfil.
    """
    user = request.user

    # --- 1. BLOQUEIO DE SEGURANÇA (PERFIL INFANTIL) ---
    nivel_ensino = getattr(user, 'nivel_ensino', '')
    fase_vida = getattr(user, 'fase_vida', '')
    
    if nivel_ensino == 'bebe' or fase_vida == 'BEBE':
        return redirect('core:daily_diary')

    # --- 2. CRIAÇÃO RÁPIDA DE POST ---
    if request.method == 'POST':
        texto = request.POST.get('texto')
        imagem = request.FILES.get('imagem')
        video = request.FILES.get('video')
        
        if texto or imagem or video:
            Post.objects.create(
                autor=user,
                conteudo=texto,
                imagem=imagem,
                video=video
            )
        return redirect('yourlife_social:home')

    # --- 3. QUERY OTIMIZADA (POSTS REAIS) ---
    
    # Subquery: Verifica se EU curti (evita loop no template)
    user_has_liked = Like.objects.filter(
        post=OuterRef('pk'),
        user=user
    )

    # Filtro: Meus posts + Quem eu sigo
    try:
        following_users = user.following.all()
        filtro_posts = Q(autor=user) | Q(autor__in=following_users)
    except AttributeError:
        filtro_posts = Q(autor=user) # Fallback se não tiver sistema de follow

    posts = Post.objects.filter(filtro_posts).select_related(
        'autor',
        # 'autor__profile' 
    ).annotate(
        total_likes=Count('curtidas', distinct=True),
        total_comentarios=Count('comentarios', distinct=True),
        user_liked=Exists(user_has_liked)
    ).order_by('-data_criacao')[:50]

    # --- 4. LÓGICA DE FEED VAZIO (PREENCHIMENTO COM IA SIMULADA) ---
    if not posts.exists():
        system_posts = []
        
        # Evento A: Boas-vindas (Sempre acontece para user novo)
        system_posts.append(SystemEventPost(
            user=user,
            content=f"🚀 Nova jornada iniciada!\n\n{user.first_name} acaba de chegar ao YourLife. O futuro começa agora.",
            date=user.date_joined,
            event_type='welcome' # Vai buscar welcome_male.jpg ou welcome_female.jpg
        ))

        # Evento B: Aniversário (Se perfil tiver data)
        if hasattr(user, 'profile') and user.profile.birth_date:
            bday = user.profile.birth_date
            # Cria data no ano atual para ordenar corretamente
            current_bday = datetime(timezone.now().year, bday.month, bday.day)
            
            system_posts.append(SystemEventPost(
                user=user,
                content=f"🎂 Celebrando a vida!\n\n{user.first_name} completa mais um ciclo em {bday.strftime('%d/%m')}.",
                date=user.date_joined, 
                event_type='birthday'
            ))

        # Evento C: Localização (Se perfil tiver cidade)
        if hasattr(user, 'profile') and getattr(user.profile, 'location', None):
            system_posts.append(SystemEventPost(
                user=user,
                content=f"📍 Marcando presença em {user.profile.location}.\n\nO mundo é pequeno para quem sonha grande.",
                date=user.date_joined,
                event_type='location'
            ))
            
        # Evento D: Cargo/Bio (Se perfil tiver)
        if hasattr(user, 'profile') and getattr(user.profile, 'bio', None):
             system_posts.append(SystemEventPost(
                user=user,
                content=f"💼 Atualização de Perfil:\n\n\"{user.profile.bio}\"",
                date=user.date_joined,
                event_type='career'
            ))

        posts = system_posts

    # --- 5. STORIES (Últimas 24h) ---
    time_threshold = timezone.now() - timezone.timedelta(hours=24)
    stories = Story.objects.filter(
        data_criacao__gte=time_threshold
    ).select_related('autor').order_by('-data_criacao')

    context = {
        'posts': posts,
        'stories': stories,
    }

    return render(request, 'social/feed/home.html', context)

@login_required
def reels_view(request):
    nivel_ensino = getattr(request.user, 'nivel_ensino', '')
    if nivel_ensino == 'bebe':
        return redirect('core:daily_diary')
        
    return render(request, 'social/reels/index.html')

@login_required
def create_story(request):
    if request.method == 'POST':
        imagem = request.FILES.get('imagem')
        video = request.FILES.get('video')
        legenda = request.POST.get('legenda')
        
        if imagem or video:
            Story.objects.create(
                autor=request.user,
                imagem=imagem,
                video=video,
                legenda=legenda
            )
            return redirect('yourlife_social:home')
            
    return render(request, 'social/create/create_story.html')