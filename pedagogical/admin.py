# niocortex_saas/pedagogical/admin.py

from django.contrib import admin
from .models import Turma, Aluno

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano_letivo', 'escola', 'autor_email')
    list_filter = ('ano_letivo', 'escola')
    search_fields = ('nome',)

    def autor_email(self, obj):
        return obj.autor.email
    autor_email.short_description = 'Professor/Autor'

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'turma_nome', 'matricula_id')
    list_filter = ('turma__escola', 'turma__ano_letivo')
    search_fields = ('nome', 'matricula_id')

    def turma_nome(self, obj):
        return obj.turma.nome
    turma_nome.short_description = 'Turma'