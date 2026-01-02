
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rotas Organizadas por Marca
    path('direcao/', include('prioris.direcao.urls')),
    path('rh/', include('humanex.rh.urls')),
    path('financeiro/', include('ledger.financeiro.urls')),
    path('secretaria/', include('hub.secretaria.urls')),
    path('coordenacao/', include('orbit.coordenacao.urls')),
    path('crm/', include('vionex.crm.urls')),
    path('social/', include('yourlife.social.urls')),
    path('', include('stage.publico.urls')), # Home/Site
    path('core/', include('core.base.urls')),
    
    # Lumenios
    path('lumenios/', include('lumenios.pedagogico.urls')),
    path('plataforma/', include('lumenios.plataforma.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
