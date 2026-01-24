from django.contrib import admin
from .models import Post, Comentario, Group, Event, UserMedia, Album, Notification, Story, Denuncia

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('autor', 'data_criacao', 'visibilidade')
    list_filter = ('visibilidade', 'data_criacao')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_private', 'get_member_count')
    search_fields = ('name',)
    def get_member_count(self, obj): return obj.members.count()
    get_member_count.short_description = 'Membros'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'location', 'event_type')
    list_filter = ('event_type', 'start_time')

# Registre os demais modelos simples
admin.site.register(Comentario)
admin.site.register(UserMedia)
admin.site.register(Album)
admin.site.register(Notification)
admin.site.register(Story)
admin.site.register(Denuncia)