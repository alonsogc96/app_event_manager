import django_filters
from .models import Event
from datetime import datetime, time

class EventFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr='icontains', label='Título') 
    #fecha_hora = django_filters.DateTimeFilter(lookup_expr='exact', label='Fecha y hora') 
    fecha = django_filters.DateFilter(method='filter_date', label='Fecha')
    categoria = django_filters.ChoiceFilter(choices=Event.CATEGORIA_CHOICES, label='Categoría') 

    class Meta:
        model = Event
        fields = ['titulo', 'fecha', 'categoria', 'estado']

    def filter_date(self, queryset, name, value):
        """
        Filtra los eventos por fecha sin tener en cuenta la hora.
        """
        if value:
            start_date = datetime.combine(value, time.min)  
            end_date = datetime.combine(value, time.max) 
            return queryset.filter(fecha_hora__gte=start_date, fecha_hora__lte=end_date)
        return queryset