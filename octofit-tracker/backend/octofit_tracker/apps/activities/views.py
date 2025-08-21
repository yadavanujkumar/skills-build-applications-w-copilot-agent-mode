"""
Views for activity-related endpoints.
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta

from .models import ActivityType, Activity, WorkoutSession
from .serializers import (
    ActivityTypeSerializer, ActivitySerializer, ActivityCreateSerializer,
    WorkoutSessionSerializer, ActivitySummarySerializer
)


class ActivityTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for activity types (read-only)."""
    queryset = ActivityType.objects.filter(is_active=True)
    serializer_class = ActivityTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for activity management."""
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter activities based on user and privacy settings."""
        if self.action == 'list':
            # Show user's own activities plus public activities from others
            return Activity.objects.filter(
                models.Q(user=self.request.user) | 
                models.Q(is_public=True)
            ).select_related('activity_type', 'user')
        
        # For detail views, show all activities the user has access to
        return Activity.objects.filter(
            models.Q(user=self.request.user) | 
            models.Q(is_public=True)
        ).select_related('activity_type', 'user')
    
    def get_serializer_class(self):
        """Use different serializer for creation."""
        if self.action == 'create':
            return ActivityCreateSerializer
        return ActivitySerializer
    
    def perform_create(self, serializer):
        """Associate activity with current user."""
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Only allow users to update their own activities."""
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You can only edit your own activities.")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Only allow users to delete their own activities."""
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own activities.")
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """Get current user's activities only."""
        activities = Activity.objects.filter(user=request.user)
        
        # Filter by date range if provided
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        if date_from:
            activities = activities.filter(activity_date__gte=date_from)
        if date_to:
            activities = activities.filter(activity_date__lte=date_to)
        
        # Filter by activity type if provided
        activity_type = request.query_params.get('activity_type')
        if activity_type:
            activities = activities.filter(activity_type_id=activity_type)
        
        page = self.paginate_queryset(activities)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get activity summary statistics for current user."""
        user = request.user
        activities = Activity.objects.filter(user=user)
        
        # Calculate summary statistics
        total_stats = activities.aggregate(
            total_activities=Count('id'),
            total_duration=Sum('duration_minutes'),
            total_points=Sum('points_earned'),
            avg_intensity=Avg('intensity')
        )
        
        # Get most common activity type
        most_common = activities.values('activity_type__name').annotate(
            count=Count('id')
        ).order_by('-count').first()
        
        # This week's statistics
        week_start = timezone.now() - timedelta(days=7)
        this_week = activities.filter(activity_date__gte=week_start).aggregate(
            week_activities=Count('id'),
            week_points=Sum('points_earned')
        )
        
        summary_data = {
            'total_activities': total_stats['total_activities'] or 0,
            'total_duration_minutes': total_stats['total_duration'] or 0,
            'total_points': total_stats['total_points'] or 0,
            'average_intensity': round(total_stats['avg_intensity'] or 0, 2),
            'most_common_activity': most_common['activity_type__name'] if most_common else 'None',
            'this_week_activities': this_week['week_activities'] or 0,
            'this_week_points': this_week['week_points'] or 0,
        }
        
        serializer = ActivitySummarySerializer(data=summary_data)
        serializer.is_valid()
        return Response(serializer.data)


class WorkoutSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for workout session management."""
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter workout sessions based on user and privacy settings."""
        if self.action == 'list':
            # Show user's own sessions plus public sessions from others
            return WorkoutSession.objects.filter(
                models.Q(user=self.request.user) | 
                models.Q(is_public=True)
            ).select_related('user').prefetch_related('activities')
        
        return WorkoutSession.objects.filter(
            models.Q(user=self.request.user) | 
            models.Q(is_public=True)
        ).select_related('user').prefetch_related('activities')
    
    def perform_create(self, serializer):
        """Associate workout session with current user."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def templates(self, request):
        """Get workout templates."""
        templates = WorkoutSession.objects.filter(
            models.Q(user=request.user, is_template=True) |
            models.Q(is_template=True, is_public=True)
        )
        
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def use_template(self, request, pk=None):
        """Create a new workout session from a template."""
        template = self.get_object()
        
        # Create new workout session based on template
        new_workout = WorkoutSession.objects.create(
            user=request.user,
            name=f"{template.name} (Copy)",
            description=template.description,
            workout_date=timezone.now(),
            is_template=False,
            is_public=False
        )
        
        # Copy activities from template (create new activity instances)
        for activity in template.activities.all():
            new_activity = Activity.objects.create(
                user=request.user,
                activity_type=activity.activity_type,
                name=activity.name,
                description=activity.description,
                duration_minutes=activity.duration_minutes,
                intensity=activity.intensity,
                activity_date=timezone.now(),
                is_public=False
            )
            new_workout.activities.add(new_activity)
        
        new_workout.calculate_totals()
        new_workout.save()
        
        serializer = self.get_serializer(new_workout)
        return Response(serializer.data, status=status.HTTP_201_CREATED)