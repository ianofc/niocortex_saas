from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from yourlife.social.models import Post, Friendship

User = get_user_model()

@login_required
def profile_detail(request, username=None):
    # --- BLOQUEIO DE BEBÊ ---
    # Bebês não têm perfil social público nem privado
    # Usa getattr para evitar erro se o campo não existir em superusers ou testes
    nivel_ensino = getattr(request.user, 'nivel_ensino', '')
    fase_vida = getattr(request.user, 'fase_vida', '')
    
    if nivel_ensino == 'bebe' or fase_vida == 'BEBE':
        return redirect('core:daily_diary')
    # ------------------------

    # Tratamento do Username
    if username:
        username = username.strip('@')

    # Define quem é o dono do perfil que está sendo visualizado
    if username and username != request.user.username:
        profile_user = get_object_or_404(User, username=username)
        is_own_profile = False
    else:
        profile_user = request.user
        is_own_profile = True

    # Busca os posts do usuário
    posts = Post.objects.filter(autor=profile_user).order_by('-data_criacao')
    
    # Contagens de Conexões (Lógica de Seguidor/Seguindo)
    # Quem segue o perfil (user_to = profile_user)
    followers_count = Friendship.objects.filter(user_to=profile_user).count()
    # Quem o perfil segue (user_from = profile_user)
    following_count = Friendship.objects.filter(user_from=profile_user).count()

    context = {
        'user': request.user,
        'profile_user': profile_user,
        'posts': posts,
        'is_own_profile': is_own_profile,
        'posts_count': posts.count(),
        'followers_count': followers_count,
        'following_count': following_count,
        # Mantendo friends_count para compatibilidade se o template usar
        'friends_count': followers_count, 
        'is_university': getattr(profile_user, 'nivel_ensino', '') == 'superior',
        'is_baby': getattr(profile_user, 'fase_vida', '') == 'BEBE',
    }

    return render(request, 'social/profile/profile_detail.html', context)

@login_required
def my_profile(request):
    return profile_detail(request, username=None)

@login_required
def user_profile(request, username):
    return profile_detail(request, username=username)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        
        # Assume que o campo bio está no modelo User ou no perfil relacionado
        # Se for um campo direto no User:
        if hasattr(user, 'bio'):
            user.bio = request.POST.get('bio', user.bio)
        # Se usar um modelo OneToOne 'profile':
        elif hasattr(user, 'profile'):
            user.profile.bio = request.POST.get('bio', user.profile.bio)
            user.profile.save()
        
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        if 'capa' in request.FILES:
            user.capa = request.FILES['capa']
            
        user.save()
        return redirect('yourlife_social:meu_perfil')
        
    return render(request, 'social/profile/edit_profile_fb.html', {'user': request.user})

# --- VIEWS PARA O MODAL DE SEGUIDORES/SEGUINDO (AJAX) ---

@login_required
def followers_list(request, username):
    """Retorna o HTML parcial com a lista de quem segue o usuário"""
    target_user = get_object_or_404(User, username=username)
    # user_to = alvo (quem recebe o follow)
    friendships = Friendship.objects.filter(user_to=target_user).select_related('user_from')
    users = [f.user_from for f in friendships]
    
    return render(request, 'social/profile/partials/user_list_modal.html', {
        'users_list': users,
        'title': 'Seguidores',
        'empty_msg': 'Ninguém segue este usuário ainda.'
    })

@login_required
def following_list(request, username):
    """Retorna o HTML parcial com a lista de quem o usuário segue"""
    target_user = get_object_or_404(User, username=username)
    # user_from = alvo (quem realiza o follow)
    friendships = Friendship.objects.filter(user_from=target_user).select_related('user_to')
    users = [f.user_to for f in friendships]
    
    return render(request, 'social/profile/partials/user_list_modal.html', {
        'users_list': users,
        'title': 'Seguindo',
        'empty_msg': 'Este usuário não segue ninguém ainda.'
    })