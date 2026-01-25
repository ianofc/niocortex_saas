from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Exists, OuterRef, Prefetch
from django.utils import timezone
from ..models import Post, Story, Like, Comentario

@login_required
def home_feed(request):
    """
    Feed Principal otimizado para alta performance.
    Resolve o problema de lentidão usando 'select_related' e 'annotate'.
    """
    
    # --- BLOQUEIO DE BEBÊ (Seguro) ---
    nivel_ensino = getattr(request.user, 'nivel_ensino', '')
    fase_vida = getattr(request.user, 'fase_vida', '')
    
    if nivel_ensino == 'bebe' or fase_vida == 'BEBE':
        return redirect('core:daily_diary')
    # ---------------------------------

    # Processamento do Formulário de Criação Rápida
    if request.method == 'POST':
        texto = request.POST.get('texto')
        imagem = request.FILES.get('imagem')
        video = request.FILES.get('video')
        
        if texto or imagem or video:
            Post.objects.create(
                autor=request.user,
                conteudo=texto,
                imagem=imagem,
                video=video
            )
        return redirect('yourlife_social:home')

    # --- OTIMIZAÇÃO DE PERFORMANCE (REDIS/SQL) ---
    
    # 1. Subquery para verificar se O USUÁRIO ATUAL curtiu o post
    # Isso evita ter que fazer um loop no template
    user_has_liked = Like.objects.filter(
        post=OuterRef('pk'),
        user=request.user
    )

    # 2. Query Principal Otimizada
    posts = Post.objects.select_related(
        'autor',              # Traz dados do User (username, first_name)
        # 'autor__profile'    # Descomente se Profile for um modelo separado OneToOne
    ).annotate(
        total_likes=Count('curtidas', distinct=True),        # Conta likes no banco
        total_comentarios=Count('comentarios', distinct=True), # Conta comentários no banco
        user_liked=Exists(user_has_liked)                    # Retorna True/False se eu curti
    ).order_by('-data_criacao')[:50] # Limita aos 50 últimos para não travar o carregamento

    # 3. Stories (Apenas os das últimas 24h)
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