from django.urls import path
from . import views

app_name = 'vionex_crm'

urlpatterns = [
    path('', views.dashboard_crm, name='dashboard'),
    
    # Leads
    path('leads/', views.listar_leads, name='listar_leads'),
    path('leads/novo/', views.novo_lead, name='novo_lead'),
    
    # Oportunidades
    path('oportunidade/<uuid:op_id>/', views.detalhe_oportunidade, name='detalhe_oportunidade'),
]