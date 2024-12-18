from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .serializers import EventSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EventFilter
from rest_framework.pagination import PageNumberPagination
from .services import EventService

class EventPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = EventService.get_all_objects()
    filter_backends = (DjangoFilterBackend,) 
    filterset_class = EventFilter 
    pagination_class = EventPagination 

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        """
        Lista todos los eventos. Con el uso del parámetro "page", muestra 10 eventos por página
        """
        paginator = self.pagination_class()
        queryset = self.filter_queryset(self.get_queryset())
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Permite actualizar un evento siempre en cuando no haya sido cancelado o ya se encuentre finalizado.
        """
        event = self.get_object() 

        if event.estado in ['cancelado', 'finalizado'] and 'estado' in request.data and request.data['estado'] not in ['activo']:
            return Response(
                {'detail': 'No es posible modificar este evento porque ya está cancelado o finalizado, excepto para reactivarlo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Acción personalizada para obtener los eventos a los que el usuario está registrado
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def user_events(self, request):
        """
        Retorna los eventos a los que el usuario está registrado.
        """
        user = request.user  # Usuario autenticado
        events = EventService.get_user_events(user)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        """
        Permite que el usuario se registre en un evento, siempre y cuando no se cruce el horario con otro evento
        ya registrado.
        """
        event = self.get_object()
        user = request.user 

        try:
            EventService.register_user_in_event(user, event)
            return Response({'detail': 'Te has registrado exitosamente en el evento.'}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_409_CONFLICT)