from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Exists, OuterRef, Q
from django.utils import timezone
from ..models import Post, Story, Like
from datetime import datetime
import random

# --- CONFIG DE IMAGENS ---
SYSTEM_IMAGES = {
    'welcome': {'M': ['welcome_male_1.jpg'], 'F': ['welcome_female_1.jpg'], 'N': ['welcome_neutral.jpg']},
    'birthday': {'M': ['bday_male.jpg'], 'F': ['bday_female.jpg'], 'N': ['bday_cake.jpg']},
    'location': {'M': ['travel_male.jpg'], 'F': ['travel_female.jpg'], 'N': ['travel_map.jpg']},
    'career': {'M': ['work_male.jpg'], 'F': ['work_female.jpg'], 'N': ['work_office.jpg']}
}

def get_smart_image(event_type, user):
    gender = 'N'
    if hasattr(user, 'profile') and user.profile.genero:
        g = str(user.profile.genero).upper()
        if g.startswith('M'): gender = 'M'
        elif g.startswith('F'): gender = 'F'
    images_list = SYSTEM_IMAGES.get(event_type, {}).get(gender, ['default_card.jpg'])
    if not images_list: images_list = ['default_card.jpg']
    return f"/static/social/img/system/{random.choice(images_list)}"

class SystemEventPost:
    def __init__(self, user, content, date, event_type=None):
        self.autor = user
        self.conteudo = content
        self.data_criacao = date
        self.imagem = get_smart_image(event_type, user) if event_type else None
        self.video = None
        self.pk = 0
        self.id = 0
        self.total_likes = 0
        self.total_comentarios = 0
        self.user_liked = False
        self.is_system_event = True 

def get_feed_posts(user, filter_type='foryou'):
    if filter_type == 'following':
        try:
            following = user.following.all()
            q_filter = Q(autor__in=following)
        except: q_filter = Q(pk=0)
    else:
        try:
            following = user.following.all()
            q_filter = Q(autor=user) | Q(autor__in=following)
        except: q_filter = Q(autor=user)
            
    posts = Post.objects.filter(q_filter).select_related('autor').order_by('-data_criacao')[:50]

    if not posts.exists() and filter_type == 'foryou':
         return [SystemEventPost(
            user=user,
            content=f"🚀 Bem-vindo ao YourLife, {user.first_name}!",
            date=user.date_joined,
            event_type='welcome'
        )]
    return posts

@login_required
def home_feed_foryou(request):
    if request.method == 'POST':
        if request.POST.get('texto') or request.FILES.get('imagem'):
            Post.objects.create(
                autor=request.user, 
                conteudo=request.POST.get('texto'), 
                imagem=request.FILES.get('imagem'), 
                video=request.FILES.get('video')
            )
        return redirect('yourlife_social:home')

    context = {'posts': get_feed_posts(request.user, 'foryou'), 'filter_type': 'foryou'}
    
    # SE FOR HTMX (Aba), retorna apenas a lista parcial
    if getattr(request, 'htmx', False):
        return render(request, 'social/components/home/feed_list_content.html', context)
        
    # Acesso normal: carrega stories e página completa
    time_threshold = timezone.now() - timezone.timedelta(hours=24)
    context['stories'] = Story.objects.filter(data_criacao__gte=time_threshold).order_by('-data_criacao')
    return render(request, 'social/feed/home.html', context)

@login_required
def home_feed_following(request):
    # Esta view SEMPRE é chamada via HTMX pelas abas
    context = {'posts': get_feed_posts(request.user, 'following'), 'filter_type': 'following'}
    return render(request, 'social/components/home/feed_list_content.html', context)

@login_required
def reels_view(request): return render(request, 'social/reels/index.html')

@login_required
def create_story(request): return render(request, 'social/create/create_story.html')
