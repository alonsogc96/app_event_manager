# events/services.py

from django.utils import timezone
from django.db.models import F
from .models import Event

class EventService:
    @staticmethod
    def get_all_objects():
        return Event.objects.all()
    
    @staticmethod
    def get_user_events(user):
        return Event.objects.filter(usuarios=user)

    @staticmethod
    def check_event_status(event):
        """
        Verifica si el evento está cancelado o finalizado.
        """
        if event.estado == 'cancelado':
            raise ValueError('Este evento ha sido cancelado, no puedes registrarte.')
        
        event_end_time = event.fecha_hora + event.duracion
        if event_end_time <= timezone.now() or event.estado == 'finalizado':
            raise ValueError('Este evento ya ha finalizado, no puedes registrarte.')

    @staticmethod
    def check_user_registered(event, user):
        """
        Verifica si el usuario ya está registrado en el evento.
        """
        if event.usuarios.filter(id=user.id).exists():
            raise ValueError('Ya estás registrado en este evento.')

    @staticmethod
    def check_event_overlap(event, user):
        """
        Verifica si el evento al que el usuario desea registrarse se superpone
        con otro evento en el que ya está registrado.
        """
        overlapping_end_time = event.fecha_hora + event.duracion

        overlapping_events = Event.objects.filter(usuarios=user).annotate(
            overlapping_end_time=F('fecha_hora') + F('duracion')
        ).filter(
            fecha_hora__lt=overlapping_end_time,
            overlapping_end_time__gt=event.fecha_hora 
        )

        if overlapping_events.exists():
            raise ValueError('El horario de este evento se cruza con otro evento en el que ya estás registrado.')


    @staticmethod
    def register_user_in_event(user, event):
        """
        Registra al usuario en el evento después de pasar todas las validaciones.
        """
        EventService.check_event_status(event)
        EventService.check_user_registered(event, user)
        EventService.check_event_overlap(event, user)

        event.usuarios.add(user)
        return event
