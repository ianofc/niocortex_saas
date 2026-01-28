import os

def print_msg(msg):
    print(f"   [⚙️] {msg}")

def patch_settings():
    """Adiciona django_htmx no settings.py se não existir."""
    settings_path = os.path.join("niocortex", "settings.py")
    
    with open(settings_path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 1. Adicionar aos INSTALLED_APPS
    if "'django_htmx'" not in content and '"django_htmx"' not in content:
        print_msg("Adicionando 'django_htmx' aos INSTALLED_APPS...")
        # Procura o final da lista INSTALLED_APPS
        if "INSTALLED_APPS = [" in content:
            content = content.replace("INSTALLED_APPS = [", "INSTALLED_APPS = [\n    'django_htmx',")
            modified = True

    # 2. Adicionar ao MIDDLEWARE (logo após CommonMiddleware)
    if "django_htmx.middleware.HtmxMiddleware" not in content:
        print_msg("Adicionando HtmxMiddleware...")
        target = "django.middleware.common.CommonMiddleware',"
        if target in content:
            content = content.replace(target, target + "\n    'django_htmx.middleware.HtmxMiddleware',")
            modified = True
        else:
            # Tenta sem a vírgula no final caso seja o último (raro para Common)
            target = "django.middleware.common.CommonMiddleware"
            if target in content:
                content = content.replace(target, target + ",\n    'django_htmx.middleware.HtmxMiddleware'")
                modified = True

    if modified:
        with open(settings_path, "w", encoding="utf-8") as f:
            f.write(content)
        print_msg("✅ settings.py atualizado com sucesso!")
    else:
        print_msg("✅ settings.py já estava configurado.")

def fix_feed_view():
    """Recria o arquivo feed.py com a lógica HTMX correta."""
    print_msg("Atualizando views/feed.py...")
    path = os.path.join("yourlife", "social", "views", "feed.py")
    
    code = """from django.shortcuts import render, redirect, get_object_or_404
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
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

def fix_views_init():
    print_msg("Corrigindo imports em views/__init__.py...")
    path = os.path.join("yourlife", "social", "views", "__init__.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write("from . import feed, auth, profile, general, groups, events, interactions")

def fix_urls():
    print_msg("Sincronizando urls.py...")
    path = os.path.join("yourlife", "social", "urls.py")
    code = """from django.urls import path
from .views import feed, auth, profile, general, groups, events, interactions

app_name = 'yourlife_social'

urlpatterns = [
    path('feed/', feed.home_feed_foryou, name='home'),
    path('feed/foryou/', feed.home_feed_foryou, name='home_feed_foryou'),
    path('feed/following/', feed.home_feed_following, name='home_feed_following'),
    
    path('login/', auth.login_view, name='login'),
    path('register/', auth.register_view, name='register'),
    path('logout/', auth.logout_view, name='logout'),

    path('settings/', general.settings_view, name='settings'),
    path('settings/theme/', general.settings_theme, name='settings_theme'),
    path('settings/accessibility/', general.settings_accessibility, name='settings_accessibility'),
    path('support/', general.support_view, name='support'),
    path('explore/', general.search_pinterest, name='explore'),

    path('profile/<str:username>/', profile.profile_detail, name='profile_detail'),
    path('groups/', groups.groups_list, name='groups_list'),
    path('events/', events.events_list, name='events_list'),
    
    path('post/<int:post_id>/like/', interactions.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', interactions.add_comment, name='add_comment'),
]
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

def main():
    print("="*40)
    print("   AUTOMAÇÃO DE CONFIGURAÇÃO FINAL")
    print("="*40)
    patch_settings()
    fix_feed_view()
    fix_views_init()
    fix_urls()
    print("\n✅ Concluído! O atributo 'request.htmx' agora estará disponível.")
    print("👉 Execute: python manage.py runserver")

if __name__ == "__main__":
    main()