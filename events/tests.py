from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Event
from datetime import timedelta
from django.utils import timezone

class EventViewSetTest(APITestCase):

    def setUp(self):
        """
        Configura los datos necesarios para las pruebas.
        Crea un usuario admin y un usuario regular.
        """
        self.user = User.objects.create_user(username='testuser', password='password')

        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword')

        self.token_url = reverse('token_obtain_pair')  # Usar la ruta personalizada

        response = self.client.post(self.token_url, {'username': 'adminuser', 'password': 'adminpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admin_access_token = response.data['access']

        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_access_token = response.data['access']
        self.url = reverse('event-list')  # Asumiendo que esta es la URL para listar eventos
        self.client = APIClient()

    def test_create_event(self):
        """
        Verifica que un usuario admin pueda crear un evento.
        """
        new_event_data = {
            'titulo': 'Nuevo Evento',
            'descripcion': 'Este es un nuevo evento de prueba.',
            'fecha_hora': timezone.now() + timedelta(days=2),  # El evento ocurre dentro de 2 días
            'duracion': timedelta(hours=3),
            'lugar': 'Lima',
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_access_token)

        response = self.client.post(self.url, new_event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertGreaterEqual(Event.objects.count(), 1)  # Deberíamos tener 1 evento en total
        self.assertEqual(response.data['titulo'], new_event_data['titulo'])

    def test_create_event_without_permission(self):
        """
        Verifica que un usuario regular no pueda crear un evento.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_access_token)

        new_event_data = {
            'titulo': 'Evento sin permisos',
            'descripcion': 'Este es un evento creado por un usuario regular.',
            'fecha_hora': timezone.now() + timedelta(days=2),
            'duracion': timedelta(hours=3),
        }

        response = self.client.post(self.url, new_event_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # El usuario regular no debería poder crear un evento

    def test_list_events(self):
        """
        Verifica que los eventos se puedan listar correctamente.
        """
        event_data = {
            'titulo': 'Test Event',
            'descripcion': 'Este es un evento de prueba.',
            'fecha_hora': timezone.now() + timedelta(days=1),  # El evento ocurre mañana
            'duracion': timedelta(hours=2),
        }
        event = Event.objects.create(**event_data)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_access_token)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Deberíamos tener al menos un evento
        self.assertEqual(response.data['results'][0]['titulo'], event_data['titulo'])

    def test_update_event(self):
        """
        Verifica que se pueda actualizar un evento que no está cancelado o finalizado.
        """
        event = Event.objects.create(
            titulo="Test Event",
            descripcion="Evento de prueba para actualización",
            fecha_hora=timezone.now() + timedelta(days=1),
            duracion=timedelta(hours=2),
        )

        updated_data = {
            'titulo': 'Updated Test Event',
            'descripcion': 'Este es un evento actualizado.',
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_access_token)

        response = self.client.put(reverse('event-detail', args=[event.id]), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event.refresh_from_db()  # Recargar el evento desde la base de datos
        self.assertEqual(event.titulo, updated_data['titulo'])
        self.assertEqual(event.descripcion, updated_data['descripcion'])

    def test_register_user_in_event(self):
        """
        Verifica que un usuario pueda registrarse correctamente en un evento.
        """
        event = Event.objects.create(
            titulo="Test Event",
            descripcion="Evento de prueba para registro",
            fecha_hora=timezone.now() + timedelta(days=1),
            duracion=timedelta(hours=2),
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_access_token)

        response = self.client.post(reverse('event-register', args=[event.id]))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.user, event.usuarios.all())

    def test_register_user_in_cancelled_event(self):
        """
        Verifica que no se pueda registrar un usuario en un evento cancelado.
        """
        event = Event.objects.create(
            titulo="Test Event",
            descripcion="Evento cancelado",
            fecha_hora=timezone.now() + timedelta(days=1),
            duracion=timedelta(hours=2),
            estado="cancelado"
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_access_token)

        response = self.client.post(reverse('event-register', args=[event.id]))

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['detail'], 'Este evento ha sido cancelado, no puedes registrarte.')

    def test_register_user_in_overlapping_event(self):
        """
        Verifica que no se pueda registrar un usuario en un evento que se cruce en horario con otro evento.
        """
        event_1 = Event.objects.create(
            titulo="Test Event 1",
            descripcion="Evento de prueba 1",
            fecha_hora=timezone.now() + timedelta(days=1),
            duracion=timedelta(hours=2),
        )

        event_2 = Event.objects.create(
            titulo="Test Event 2",
            descripcion="Evento de prueba 2 (superpuesto)",
            fecha_hora=event_1.fecha_hora + timedelta(hours=1),  # Se cruza con el primero
            duracion=timedelta(hours=2),
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_access_token)
        response = self.client.post(reverse('event-register', args=[event_1.id]))
        response = self.client.post(reverse('event-register', args=[event_2.id]))
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['detail'], 'El horario de este evento se cruza con otro evento en el que ya estás registrado.')