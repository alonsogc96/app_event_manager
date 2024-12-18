from django.urls import path, include
from rest_framework import routers
from events import views

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet, 'event')

urlpatterns = [
    path('v1/', include(router.urls)),
]