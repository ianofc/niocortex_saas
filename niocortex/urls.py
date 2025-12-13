from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.urls import reverse

urlpatterns = [
    path('', lambda request: redirect(reverse('core:login')), name='home'),
    path('admin/', admin.site.urls),
    
    # Apps
    path('auth/', include('core.urls')), # Prefixo auth/ para login/registro
    path('pedagogico/', include('pedagogical.urls')), # 🚨 NOVA ROTA
]