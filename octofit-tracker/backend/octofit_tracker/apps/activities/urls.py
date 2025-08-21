"""
URL configuration for activities app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'types', views.ActivityTypeViewSet, basename='activitytype')
router.register(r'', views.ActivityViewSet, basename='activity')
router.register(r'workouts', views.WorkoutSessionViewSet, basename='workoutsession')

urlpatterns = [
    path('', include(router.urls)),
]