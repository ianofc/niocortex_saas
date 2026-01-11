from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import social 

urlpatterns = [
    # Rota Global Única para Identidade
    path('identidade-digital/', social.global_id_card, name='global_id_card'),
    
    path('admin/', admin.site.urls),
    path('', include('stage.publico.urls')),
    path('social/', include('yourlife.social.urls')),
    path('core/', include('core.urls')),
    path('lumenios/', include('lumenios.pedagogico.urls')),
    path('plataforma/', include('lumenios.plataforma.urls')),
    path('direcao/', include('prioris.direcao.urls')),
    path('financeiro/', include('ledger.financeiro.urls')),
    path('rh/', include('humanex.rh.urls')),
    path('secretaria/', include('hub.secretaria.urls')),
    path('coordenacao/', include('orbit.coordenacao.urls')),
    path('crm/', include('vionex.crm.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
