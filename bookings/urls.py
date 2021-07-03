"""Bookings URLs."""

#Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

#Views
from .views import TrainingReserveViewSet, AppointmentViewSet


router = DefaultRouter()
router2 = DefaultRouter()
router.register(r'reserves', TrainingReserveViewSet, basename='reserves')
router2.register(r'appointments', AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router2.urls))
]