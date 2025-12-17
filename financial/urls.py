# niocortex/financial/urls.py

from django.urls import path
from . import views

app_name = 'financial'

urlpatterns = [
    # Dashboard Financeiro
    path('', views.dashboard_financeiro, name='dashboard'),

    # --- Património & Almoxarifado ---
    path('patrimonio/', views.listar_patrimonio, name='listar_patrimonio'),
    path('patrimonio/novo/', views.novo_patrimonio, name='novo_patrimonio'),
    
    path('fornecedores/', views.listar_fornecedores, name='listar_fornecedores'),
    path('fornecedores/novo/', views.novo_fornecedor, name='novo_fornecedor'),

    # --- Gestão de Contratos ---
    path('contratos/', views.listar_contratos, name='listar_contratos'),
    path('contratos/novo/', views.criar_contrato, name='criar_contrato'),
    
    # --- Gestão de Boletos (Receitas) ---
    path('boletos/', views.listar_boletos, name='listar_boletos'),
    
    # Ação 1: Gerar Mensalidade Padrão (Lógica Automática do Contrato)
    path('boletos/gerar-mensalidade/<uuid:contrato_id>/', views.gerar_mensalidade_manual, name='gerar_mensalidade'),
    
    # Ação 2: Gerar Boleto Avulso (Formulário Customizado)
    path('boletos/avulso/<uuid:contrato_id>/', views.gerar_boleto_avulso, name='gerar_boleto_avulso'),
    
    # Ação 3: Baixar Boleto (Registrar Pagamento)
    path('boletos/baixar/<uuid:boleto_id>/', views.baixar_boleto, name='baixar_boleto'),
]