from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from ..models import Evento

@login_required
def events_list(request):
    hoje = timezone.now()
    # Eventos futuros
    eventos = Evento.objects.filter(data_inicio__gte=hoje).order_by('data_inicio')
    return render(request, 'social/events/list.html', {'eventos': eventos})

@login_required
def calendar_view(request):
    # Lógica simples para calendário (pode ser expandida com JSON para FullCalendar)
    eventos = Evento.objects.all()
    return render(request, 'social/events/calendar.html', {'eventos': eventos})
