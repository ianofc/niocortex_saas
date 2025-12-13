# niocortex_saas/niocortex/urls.py (APENAS TRECHOS CHAVE)

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.urls import reverse

urlpatterns = [
    # 1. Rota raiz: Redireciona para a página de Login
    path('', lambda request: redirect(reverse('core:login')), name='home'),
    
    # 2. Django Admin (Super-Admin)
    path('admin/', admin.site.urls),
    
    # 3. Core Service URLs (Auth, Dashboards, etc.)
    path('', include('core.urls')),
    
    # ... Futuras inclusões dos outros Apps/Serviços
]