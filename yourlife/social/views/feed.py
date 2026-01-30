from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Post

@login_required
def home_feed_foryou(request):
    """
    Retorna o feed global. 
    Se a requisição for HTMX, retorna apenas a lista de posts.
    """
    try:
        posts = Post.objects.all().order_by('-data_criacao')
    except:
        posts = []
    
    context = {
        'posts': posts,
        'filter_type': 'foryou'
    }

    # SEGREDO DO HTMX: Se for uma requisição do HTMX, envia apenas o fragmento
    if request.headers.get('HX-Request'):
        return render(request, 'social/components/home/feed_list_content.html', context)
    
    # Se for um carregamento normal de página (F5 ou link direto)
    return render(request, 'social/feed/home.html', context)

@login_required
def home_feed_following(request):
    """
    Retorna o feed de quem o usuário segue.
    """
    try:
        # Pega os IDs dos perfis que o usuário segue
        following_ids = request.user.profile.following.values_list('user_id', flat=True)
        posts = Post.objects.filter(autor_id__in=following_ids).order_by('-data_criacao')
    except:
        posts = []

    context = {
        'posts': posts,
        'filter_type': 'following'
    }

    if request.headers.get('HX-Request'):
        return render(request, 'social/components/home/feed_list_content.html', context)
        
    return render(request, 'social/feed/home.html', context)

@login_required
def reels_view(request):
    # Caso queira usar HTMX nos reels também no futuro
    context = {'active_tab': 'reels'}
    return render(request, 'social/reels/index.html', context)

@login_required
def explore_view(request):
    context = {'active_tab': 'explore'}
    return render(request, 'social/search/explore.html', context)