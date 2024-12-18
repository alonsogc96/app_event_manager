from django.db import models
from django.contrib.auth.models import User 
from datetime import timedelta

class Event(models.Model):

    titulo = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField()
    duracion = models.DurationField(default=timedelta(hours=2))
    lugar = models.CharField(max_length=255)
    CATEGORIA_CHOICES = [
        ('concierto', 'Concierto'),
        ('conferencia', 'Conferencia'),
        ('feria', 'Feria'),
        ('congreso', 'Congreso'),
        ('otro', 'Otro'),
    ]
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='otro')
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('cancelado', 'Cancelado'),
        ('finalizado', 'Finalizado'),
    ]
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='activo',
    )
    usuarios = models.ManyToManyField(User, related_name='events', blank=True)

    def __str__(self):
        return self.titulo