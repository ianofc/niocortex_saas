from django.urls import path
from . import views

app_name = 'orbit_coordenacao'

urlpatterns = [
    path('', views.dashboard_coordenacao, name='dashboard'),
]