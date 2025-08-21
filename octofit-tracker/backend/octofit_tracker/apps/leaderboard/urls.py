"""
URL configuration for leaderboard app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.LeaderboardViewSet, basename='leaderboard')
router.register(r'achievements', views.AchievementViewSet, basename='achievement')
router.register(r'challenges', views.WeeklyChallengeViewSet, basename='weeklychallenge')

urlpatterns = [
    path('', include(router.urls)),
]