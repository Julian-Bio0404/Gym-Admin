"""Users URLs."""

#Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

#Views
from .views import TrainingReserveViewSet 


router = DefaultRouter()
router.register(r'reserves', TrainingReserveViewSet, basename='reserves')

urlpatterns = [
    path('', include(router.urls))
]