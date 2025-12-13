# niocortex_saas/core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, School

class CustomUserAdmin(UserAdmin):
    # Mostra os campos personalizados (role, tenant_id) no Admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informações SaaS', {'fields': ('role', 'tenant_type', 'tenant_id', 'school', 'imagem_perfil')}),
    )
    list_display = ('username', 'email', 'role', 'tenant_type', 'is_staff')
    list_filter = ('role', 'tenant_type', 'is_staff')

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tenant_id')
    readonly_fields = ('tenant_id',)

admin.site.register(CustomUser, CustomUserAdmin)