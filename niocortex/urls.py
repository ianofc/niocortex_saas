# niocortex/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Rota Administrativa
    path('admin/', admin.site.urls),
    
    # Rotas do Core (Landing Page, Login, Dashboard)
    # A raiz ('') agora será controlada pelo core.urls -> views.index
    path('', include('core.urls')), 
    
    # Módulos do Sistema
    path('pedagogico/', include('pedagogical.urls')),
    path('rh/', include('hr.urls')),
    path('financial/', include('financial.urls')),
    path('crm/', include('crm_sales.urls')),
    path('secretaria/', include('secretariat.urls')),
    path('lumenio/', include('lumenio.plataforma.urls')),

    # Auth padrão
    path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)