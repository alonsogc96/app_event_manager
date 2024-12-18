from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_hora', 'lugar', 'categoria')
    list_filter = ('categoria', 'fecha_hora') 
    search_fields = ('titulo', 'categoria')
    filter_horizontal = ('usuarios',)
