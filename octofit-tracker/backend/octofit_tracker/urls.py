"""
URL configuration for octofit_tracker project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('octofit_tracker.apps.users.urls')),
    path('api/activities/', include('octofit_tracker.apps.activities.urls')),
    path('api/teams/', include('octofit_tracker.apps.teams.urls')),
    path('api/leaderboard/', include('octofit_tracker.apps.leaderboard.urls')),
]