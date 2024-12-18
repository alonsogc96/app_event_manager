from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    asistentes = serializers.IntegerField(source='usuarios.count', read_only=True)
    fecha_hora = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Event
        fields = ['id', 'titulo', 'descripcion', 'fecha_hora', 'duracion', 'lugar', 'categoria', 'estado', 'asistentes']