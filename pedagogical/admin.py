# niocortex/pedagogical/admin.py

from django.contrib import admin
from .models import Turma, Aluno, PlanoDeAula, Atividade, Nota, DiarioClasse, Frequencia

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    # 'escola' e 'autor' não existem mais no model, usamos tenant_id
    list_display = ('nome', 'ano_letivo', 'tenant_id') 
    list_filter = ('ano_letivo',)
    search_fields = ('nome', 'id')

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'turma', 'matricula_id')
    # Removemos 'turma__escola' pois Turma não tem mais relação direta com Escola (Model)
    list_filter = ('turma__ano_letivo',) 
    search_fields = ('nome', 'matricula_id')

# --- REGISTRO DOS NOVOS MODELS ---

@admin.register(PlanoDeAula)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'turma', 'data_prevista', 'status')
    list_filter = ('status', 'data_prevista')

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'turma', 'tipo', 'data_aplicacao', 'unidade')
    list_filter = ('tipo', 'unidade')

@admin.register(DiarioClasse)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ('data', 'turma', 'professor')
    list_filter = ('data',)

# Nota e Frequência são muitos dados, melhor deixar inline ou básico
admin.site.register(Nota)
admin.site.register(Frequencia)