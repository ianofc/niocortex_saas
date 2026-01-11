from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Configuração da listagem (Para você conferir se Ana é Universitária)
    list_display = ['username', 'email', 'first_name', 'role', 'nivel_ensino', 'fase_vida', 'is_staff']
    list_filter = ['role', 'nivel_ensino', 'fase_vida', 'tenant_type']
    
    # Correção dos campos de edição (Removido 'imagem_perfil', adicionado 'avatar')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações do NioCortex', {
            'fields': (
                'role', 
                'avatar',          # Corrigido de imagem_perfil para avatar
                'bio', 
                'cpf', 
                'telefone'
            )
        }),
        ('Contexto Educacional', {
            'fields': (
                'nivel_ensino',    # Essencial para a lógica da Ana
                'fase_vida',       # Essencial para a lógica da Ana
                'tenant_type', 
                'tenant_id', 
                'school',
                'turma'
            )
        }),
    )
    
    # Permitir edição desses campos na criação
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': (
                'email', 
                'first_name', 
                'last_name', 
                'role', 
                'nivel_ensino', 
                'fase_vida'
            )
        }),
    )

    search_fields = ['username', 'first_name', 'email']
