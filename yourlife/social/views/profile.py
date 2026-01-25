from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from ..models import Post, Friendship

User = get_user_model()

@login_required
def profile_detail(request, username=None):
    if getattr(request.user, 'nivel_ensino', '') == 'bebe':
        return redirect('core:daily_diary')

    if username:
        username = username.strip('@')

    if username and username != request.user.username:
        profile_user = get_object_or_404(User, username=username)
        is_own_profile = False
    else:
        profile_user = request.user
        is_own_profile = True

    posts = Post.objects.filter(autor=profile_user).order_by('-data_criacao')
    followers_count = Friendship.objects.filter(user_to=profile_user).count()
    following_count = Friendship.objects.filter(user_from=profile_user).count()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_own_profile': is_own_profile,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'social/profile/profile_detail.html', context)

@login_required
def my_profile(request):
    return profile_detail(request, username=None)

@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.save()
        return redirect('yourlife_social:meu_perfil')
    return render(request, 'social/profile/edit_profile_fb.html', {'user': user})

@login_required
def followers_list(request, username):
    target_user = get_object_or_404(User, username=username)
    friendships = Friendship.objects.filter(user_to=target_user).select_related('user_from')
    users = [f.user_from for f in friendships]
    return render(request, 'social/profile/partials/user_list_modal.html', {
        'users_list': users, 'title': 'Seguidores', 'empty_msg': 'Ninguém segue ainda.'
    })

@login_required
def following_list(request, username):
    target_user = get_object_or_404(User, username=username)
    friendships = Friendship.objects.filter(user_from=target_user).select_related('user_to')
    users = [f.user_to for f in friendships]
    return render(request, 'social/profile/partials/user_list_modal.html', {
        'users_list': users, 'title': 'Seguindo', 'empty_msg': 'Não segue ninguém ainda.'
    })
