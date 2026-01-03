# niocortex/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Rota Administrativa (Django Admin)
    path('admin/', admin.site.urls),
    
    # 2. Rotas do Core (Landing Page, Auth, Dashboards)
    # A raiz ('') vai para o core
    path('', include('core.urls')), 
    
    # 3. Módulos do Sistema (ERP e AVA)
    # AVA (Lumenios) - Inclui Plataforma e Pedagógico
    path('lumenios/', include('lumenios.plataforma.urls')), 
    path('lumenios/pedagogico/', include('lumenios.pedagogico.urls')), 

    # ERP (Administrativo)
    path('rh/', include('hr.urls')),
    path('financial/', include('financial.urls')),
    path('crm/', include('crm_sales.urls')),
    path('secretaria/', include('secretariat.urls')),

    # 4. Auth Padrão (Reset de senha, etc)
    path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)