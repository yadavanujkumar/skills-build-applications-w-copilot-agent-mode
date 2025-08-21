"""
URL configuration for teams app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.TeamViewSet, basename='team')
router.register(r'challenges', views.TeamChallengeViewSet, basename='teamchallenge')
router.register(r'invitations', views.TeamInvitationViewSet, basename='teaminvitation')

urlpatterns = [
    path('', include(router.urls)),
]