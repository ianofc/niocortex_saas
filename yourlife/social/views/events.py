from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Tente importar o modelo se ele existir, senão ignore para evitar erros
try:
    from yourlife.social.models import Event
except ImportError:
    Event = None

class EventListView(LoginRequiredMixin, ListView):
    template_name = 'social/events/list.html'
    context_object_name = 'events'

    def get_queryset(self):
        # Se o modelo existir, retorna os eventos, senão lista vazia
        if Event:
            try:
                return Event.objects.all()
            except:
                return []
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Event:
            # Eventos que participo
            context['my_events'] = self.request.user.participating_events.all()
            # Todos os eventos futuros (Agenda Global)
            from django.utils import timezone
            context['all_events'] = Event.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
        return context

@login_required
def event_create(request):
    # Lógica de criação de evento (stub)
    if request.method == 'POST':
        # Aqui viria o processamento do formulário
        pass
    return render(request, 'social/events/create.html')

@login_required
def event_detail(request, event_id):
    # Lógica de detalhe do evento (stub)
    event = None
    if Event:
        # event = get_object_or_404(Event, id=event_id)
        pass
    return render(request, 'social/events/detail.html', {'event': event})