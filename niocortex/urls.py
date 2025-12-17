from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Redireciona a raiz (/) para o login
    path('', lambda request: redirect(reverse('core:login')), name='home'),
    
    path('admin/', admin.site.urls),
    
    # 🚨 ALTERAÇÃO AQUI: Mudamos de 'auth/' para '' (string vazia)
    # Isso faz as rotas do core (login, dashboard, etc.) ficarem na raiz do site.
    path('', include('core.urls')), 
    
    path('pedagogico/', include('pedagogical.urls')),

    path('rh/', include('hr.urls')),

    path('financial/', include('financial.urls')),

    path('crm/', include('crm_sales.urls')),

    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/', include('core.urls')),  # Inclui rotas de autenticação personalizadas

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)