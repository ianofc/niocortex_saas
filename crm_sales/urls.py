# niocortex/crm_sales/urls.py

from django.urls import path
from . import views

app_name = 'crm_sales'

urlpatterns = [
    path('', views.crm_dashboard, name='dashboard'),
]