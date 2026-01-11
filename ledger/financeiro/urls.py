from django.urls import path
from . import views

app_name = 'ledger_financeiro'

urlpatterns = [
    path('', views.dashboard_financeiro, name='dashboard'),
    
    path('patrimonio/', views.listar_patrimonio, name='listar_patrimonio'),
    path('patrimonio/novo/', views.novo_patrimonio, name='novo_patrimonio'),
    
    path('fornecedores/', views.listar_fornecedores, name='listar_fornecedores'),
    path('fornecedores/novo/', views.novo_fornecedor, name='novo_fornecedor'),

    path('contratos/', views.listar_contratos, name='listar_contratos'),
    path('contratos/novo/', views.criar_contrato, name='criar_contrato'),
    
    path('boletos/', views.listar_boletos, name='listar_boletos'),
    path('boletos/gerar-mensalidade/<uuid:contrato_id>/', views.gerar_mensalidade_manual, name='gerar_mensalidade'),
    path('boletos/avulso/<uuid:contrato_id>/', views.gerar_boleto_avulso, name='gerar_boleto_avulso'),
    path('boletos/baixar/<uuid:boleto_id>/', views.baixar_boleto, name='baixar_boleto'),

    path('webhook/mercadopago/', views.mercadopago_webhook, name='mp_webhook'),
]