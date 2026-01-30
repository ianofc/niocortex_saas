import os

# 1. Corrigindo yourlife/social/urls.py
# Garante que 'reels', 'meu_perfil', 'explore' e 'home' existam
urls_content = """from django.urls import path
from .views import feed, auth, profile, general, groups, events, interactions, chat

app_name = 'yourlife_social'

urlpatterns = [
    # Feed & Home
    path('', feed.home_feed_foryou, name='home'),
    path('feed/', feed.home_feed_foryou, name='feed_home'),
    path('feed/foryou/', feed.home_feed_foryou, name='home_feed_foryou'),
    path('feed/following/', feed.home_feed_following, name='home_feed_following'),
    
    # Recursos Extras
    path('reels/', feed.reels_view, name='reels'),
    path('explore/', feed.explore_view, name='explore'),
    path('talkio/', chat.talkio_view, name='talkio_app'),
    
    # Auth
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('register/', auth.register_view, name='register'),
    
    # Configurações
    path('settings/', general.settings_view, name='settings'),
    path('settings/p/', general.settings_view, name='settings_page'),
    path('settings/theme/', general.settings_theme, name='settings_theme'),
    path('support/', general.support_view, name='support'),
    path('support/p/', general.support_view, name='support_page'),
    
    # Perfil (ESSENCIAL PARA O ERRO ATUAL)
    path('profile/me/', profile.meu_perfil, name='meu_perfil'),
    path('profile/<str:username>/', profile.profile_detail, name='profile_detail'),
    
    # Interações
    path('post/<int:post_id>/like/', interactions.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', interactions.add_comment, name='add_comment'),

    path('groups/', groups.groups_list, name='groups_list'),
    path('events/', events.events_list, name='events_list'),
]
"""

# 2. Corrigindo yourlife/social/views/profile.py
# Garante que a view 'meu_perfil' exista
profile_views_content = """from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def meu_perfil(request):
    # Redireciona para o perfil do usuário logado
    return redirect('yourlife_social:profile_detail', username=request.user.username)

@login_required
def profile_detail(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_me = (request.user == profile_user)
    
    context = {
        'profile_user': profile_user,
        'is_me': is_me,
        # Adicione outros contextos necessários aqui
    }
    return render(request, 'social/profile/profile_detail.html', context)
"""

# 3. Corrigindo yourlife/social/views/feed.py
# Garante que 'reels_view' e 'explore_view' existam
feed_views_content = """from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Post

@login_required
def home_feed_foryou(request):
    # Tenta pegar posts, se o modelo existir
    try:
        posts = Post.objects.all().order_by('-created_at')
    except:
        posts = []
        
    return render(request, 'social/feed/home.html', {
        'posts': posts, 
        'filter_type': 'foryou'
    })

@login_required
def home_feed_following(request):
    return render(request, 'social/feed/home.html', {'filter_type': 'following', 'posts': []})

@login_required
def reels_view(request):
    return render(request, 'social/reels/index.html')

@login_required
def explore_view(request):
    return render(request, 'social/search/explore.html')
"""

# 4. Corrigindo navbar right (core/templates/core/components/navbar/right.html)
# Garante que o link aponte corretamente para 'yourlife_social:meu_perfil'
navbar_right_content = """{% load static %}

{% if '/social/' in request.path %}
    {% with zios_greeting="E aí! Eu sou o Zios AI. 😎 Pronto para ver o que tá rolando na YourLife?" zios_role="social" %}
    <div id="zios-context" data-greeting="{{ zios_greeting }}" data-role="{{ zios_role }}" style="display:none;"></div>
    {% endwith %}
{% else %}
    {% with zios_greeting="Bem-vindo ao NioCortex." zios_role="admin" %}
    <div id="zios-context" data-greeting="{{ zios_greeting }}" data-role="{{ zios_role }}" style="display:none;"></div>
    {% endwith %}
{% endif %}

<div class="flex items-center justify-end flex-1 gap-3 md:gap-4" x-data="{ profileOpen: false }">

    <button @click="$dispatch('toggle-switcher')" 
            class="flex items-center justify-center w-10 h-10 transition-all border rounded-full group bg-white/5 hover:bg-white/10 border-white/10 text-slate-400 hover:text-white"
            title="NioCortex Apps">
        <i class="text-lg transition-transform fas fa-th group-hover:rotate-90"></i>
    </button>

    <button @click="$store.nav.toggle('zios')" 
            class="flex items-center justify-center w-10 h-10 transition-all border rounded-full bg-white/5 hover:bg-white/10 border-white/10 group"
            title="Assistente IA">
        <i class="text-xl text-purple-400 transition fas fa-brain group-hover:text-purple-500 animate-pulse"></i>
    </button>

    <a href="{% url 'yourlife_social:talkio_app' %}" 
            class="flex items-center justify-center w-10 h-10 transition-all border rounded-full bg-white/5 hover:bg-white/10 border-white/10"
            title="Talkio Messenger">
        <img src="{% static 'imgs/talkio/Talkio_logo.png' %}" class="w-6 h-6 opacity-90 hover:opacity-100">
    </a>
    
    <div class="relative">
        <button @click="profileOpen = !profileOpen" 
                class="flex items-center gap-2 py-1 pl-1 pr-3 transition-all border rounded-full bg-white/5 hover:bg-white/10 border-white/10">
            
            <img src="{% if user.profile.avatar %}{{ user.profile.avatar.url }}{% else %}https://ui-avatars.com/api/?name={{ user.first_name }}&background=random&color=fff{% endif %}" 
                 class="object-cover w-8 h-8 border-2 rounded-full shadow-sm border-white/20">
            
            <i class="fas fa-chevron-down text-[10px] text-slate-400 transition-transform duration-300" 
               :class="profileOpen ? 'rotate-180' : ''"></i>
        </button>
        
        <div x-show="profileOpen" @click.away="profileOpen = false" x-cloak
             class="absolute top-14 right-0 w-72 bg-[#1A1F2C] rounded-2xl shadow-2xl z-[120] border border-white/10 overflow-hidden"
             x-transition:enter="transition ease-out duration-200"
             x-transition:enter-start="opacity-0 translate-y-2"
             x-transition:enter-end="opacity-100 translate-y-0">
             
            <div class="p-4 border-b border-white/5 bg-white/5">
                <p class="font-bold leading-tight text-white">{{ user.get_full_name }}</p>
                <a href="{% url 'yourlife_social:meu_perfil' %}" class="text-xs font-bold text-purple-400 hover:text-purple-300">Ver Perfil Social</a>
            </div>
            
            <div class="p-2 space-y-1">
                <a href="{% url 'yourlife_social:settings_page' %}" class="block px-3 py-2 text-sm font-medium hover:bg-white/5 rounded-xl text-slate-300 hover:text-white">
                    <i class="w-5 fas fa-cog text-slate-500"></i> Configurações
                </a>
                <a href="{% url 'yourlife_social:support_page' %}" class="block px-3 py-2 text-sm font-medium hover:bg-white/5 rounded-xl text-slate-300 hover:text-white">
                    <i class="w-5 fas fa-life-ring text-slate-500"></i> Suporte
                </a>
            </div>
            
            <div class="p-2 border-t border-white/5">
                <a href="{% url 'yourlife_social:logout' %}" class="flex items-center gap-2 px-3 py-2 text-sm font-medium text-red-400 hover:bg-red-500/10 rounded-xl">
                    <i class="fas fa-sign-out-alt"></i> Sair
                </a>
            </div>
        </div>
    </div>
</div>
<script src="{% static 'core/js/navbar.js' %}"></script>
"""

# Função auxiliar para escrever arquivos
def write_file(path, content):
    try:
        # Garante que o diretório exista
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Arquivo atualizado: {path}")
    except Exception as e:
        print(f"[ERRO] Falha ao escrever {path}: {str(e)}")

# Caminhos dos arquivos
base_dir = os.getcwd()
path_urls = os.path.join(base_dir, 'yourlife', 'social', 'urls.py')
path_views_profile = os.path.join(base_dir, 'yourlife', 'social', 'views', 'profile.py')
path_views_feed = os.path.join(base_dir, 'yourlife', 'social', 'views', 'feed.py')
path_navbar_right = os.path.join(base_dir, 'core', 'templates', 'core', 'components', 'navbar', 'right.html')

# Executando escritas
print("--- Iniciando correção automática de Rotas e Views ---")
write_file(path_urls, urls_content)
write_file(path_views_profile, profile_views_content)
write_file(path_views_feed, feed_views_content)
write_file(path_navbar_right, navbar_right_content)
print("--- Concluído. Reinicie o servidor Django. ---")