# niocortex/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Redireciona a raiz (/) para o login
    path('', lambda request: redirect(reverse('core:login')), name='home'),
    
    # Rota Administrativa (Mantenha APENAS UMA)
    path('admin/', admin.site.urls),
    
    # Rotas do Core (Login, Dashboard)
    # Nota: Removemos a duplicata 'accounts/' apontando para core.urls
    path('', include('core.urls')), 
    
    # Módulos do Sistema
    path('pedagogico/', include('pedagogical.urls')),
    path('rh/', include('hr.urls')),
    path('financial/', include('financial.urls')),
    path('crm/', include('crm_sales.urls')),
    path('secretaria/', include('secretariat.urls')),

    # Auth padrão do Django (Reset de senha, etc)
    path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)