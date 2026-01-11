from django.contrib import admin
from .models import Funcionario, Departamento, Cargo

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'responsavel', 'tenant_id')

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'salario_base', 'tenant_id')

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cargo', 'departamento', 'email_corporativo', 'ativo')
    list_filter = ('cargo', 'departamento', 'ativo')