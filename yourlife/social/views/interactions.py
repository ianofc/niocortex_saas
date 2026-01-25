from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from ..models import Post, Like, Comentario

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
        delta = -1
    else:
        liked = True
        delta = 1

    icon_class = "fas fa-heart text-red-500 animate-pulse" if liked else "far fa-heart text-gray-800 hover:text-gray-500"
    
    html = f'''
        <button hx-post="/social/like/{post.id}/" hx-swap="outerHTML" hx-target="#like-btn-{post.id}" id="like-btn-{post.id}" class="text-2xl transition transform active:scale-75 hover:scale-110 focus:outline-none">
            <i class="{icon_class}"></i>
        </button>
        <script>
            var countEl = document.getElementById('likes-val-{post.id}');
            if(countEl) countEl.innerText = parseInt(countEl.innerText) + ({delta});
        </script>
    '''
    return HttpResponse(html)

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    conteudo = request.POST.get('conteudo')
    
    if conteudo:
        Comentario.objects.create(user=request.user, post=post, conteudo=conteudo)
        return HttpResponse(status=204)
    
    return HttpResponse(status=400)

# --- Placeholders para evitar erro de importação ---

@login_required
def share_post(request, post_id):
    # Lógica de compartilhamento futura
    return JsonResponse({'status': 'shared'})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, autor=request.user)
    post.delete()
    return redirect('yourlife_social:home')

@login_required
def edit_post(request, post_id):
    return HttpResponse("Edição ainda não implementada.")

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comentario, id=comment_id, user=request.user)
    comment.delete()
    return HttpResponse(status=204)
