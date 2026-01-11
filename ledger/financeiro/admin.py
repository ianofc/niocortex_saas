from django.contrib import admin
from .models import PlanoSaaS, AssinaturaEscola, ContratoAluno, BoletoAluno, Fornecedor, Patrimonio, Transacao

@admin.register(PlanoSaaS)
class PlanoSaaSAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_base', 'limite_alunos')

@admin.register(ContratoAluno)
class ContratoAlunoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'valor_mensalidade', 'ativo', 'tenant_id')

@admin.register(BoletoAluno)
class BoletoAlunoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'vencimento', 'status', 'tenant_id')

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj', 'categoria')

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('email_cliente', 'plano', 'status', 'created_at')