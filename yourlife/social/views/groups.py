from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# Tenta importar o modelo, se não existir, usa lista vazia para não quebrar
try:
    from yourlife.social.models import Grupo
except ImportError:
    Group = None

class GroupListView(LoginRequiredMixin, ListView):
    template_name = 'social/groups/list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        if Group:
            return Group.objects.all()
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Grupos do usuário
        if Group:
            context['groups'] = self.request.user.social_groups.all()
            # Sugestões: Grupos públicos que o usuário NÃO faz parte
            context['suggestions'] = Group.objects.filter(is_private=False).exclude(members=self.request.user)[:5]
        return context

def group_create(request):
    # Lógica de criação...
    return render(request, 'social/groups/create.html', {})

def group_detail(request, group_id):
    # Lógica de detalhe...
    return render(request, 'social/groups/detail.html', {'group_id': group_id})