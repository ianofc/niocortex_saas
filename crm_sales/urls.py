from django.urls import path
from . import views

app_name = 'crm_sales'

urlpatterns = [
    path('', views.crm_dashboard, name='dashboard'),
    path('leads/', views.leads_list, name='leads'),
    path('opportunities/', views.opportunities_list, name='opportunities'),
]