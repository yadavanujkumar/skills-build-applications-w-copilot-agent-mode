"""
Views for leaderboard-related endpoints.
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta, datetime

from .models import LeaderboardEntry, Achievement, UserAchievement, WeeklyChallenge, WeeklyChallengeParticipation
from .serializers import (
    LeaderboardEntrySerializer, AchievementSerializer, UserAchievementSerializer,
    WeeklyChallengeSerializer, WeeklyChallengeParticipationSerializer,
    LeaderboardSummarySerializer, UserRankingSerializer
)


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for leaderboard data."""
    serializer_class = LeaderboardEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get leaderboard entries based on filters."""
        queryset = LeaderboardEntry.objects.select_related('user')
        
        # Filter by leaderboard type
        leaderboard_type = self.request.query_params.get('type', 'overall')
        queryset = queryset.filter(leaderboard_type=leaderboard_type)
        
        # Filter by time period
        period = self.request.query_params.get('period', 'current')
        if period == 'current':
            # Get the most recent period for this leaderboard type
            latest_entry = LeaderboardEntry.objects.filter(
                leaderboard_type=leaderboard_type
            ).order_by('-period_end').first()
            
            if latest_entry:
                queryset = queryset.filter(
                    period_start=latest_entry.period_start,
                    period_end=latest_entry.period_end
                )
        
        return queryset.order_by('rank')
    
    @action(detail=False, methods=['get'])
    def overall(self, request):
        """Get overall points leaderboard."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Get top users by total points
        users = User.objects.filter(
            profile__is_profile_public=True
        ).order_by('-total_points')[:50]
        
        leaderboard_data = []
        for idx, user in enumerate(users, 1):
            leaderboard_data.append({
                'user_id': user.id,
                'username': user.username,
                'full_name': user.get_full_name() if user.profile.show_real_name else user.username,
                'rank': idx,
                'score': float(user.total_points),
                'change_from_last_period': None  # Could be calculated from historical data
            })
        
        serializer = UserRankingSerializer(leaderboard_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def weekly(self, request):
        """Get weekly points leaderboard."""
        from django.contrib.auth import get_user_model
        from octofit_tracker.apps.activities.models import Activity
        
        User = get_user_model()
        
        # Calculate weekly points (last 7 days)
        week_start = timezone.now() - timedelta(days=7)
        
        # Get users with their weekly points
        weekly_points = Activity.objects.filter(
            activity_date__gte=week_start,
            user__profile__is_profile_public=True
        ).values(
            'user__id', 'user__username', 'user__first_name', 'user__last_name'
        ).annotate(
            weekly_points=Sum('points_earned')
        ).order_by('-weekly_points')[:50]
        
        leaderboard_data = []
        for idx, data in enumerate(weekly_points, 1):
            user = User.objects.get(id=data['user__id'])
            full_name = f"{data['user__first_name']} {data['user__last_name']}".strip()
            
            leaderboard_data.append({
                'user_id': data['user__id'],
                'username': data['user__username'],
                'full_name': full_name if user.profile.show_real_name else data['user__username'],
                'rank': idx,
                'score': float(data['weekly_points']),
                'change_from_last_period': None
            })
        
        serializer = UserRankingSerializer(leaderboard_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def teams(self, request):
        """Get team leaderboard."""
        from octofit_tracker.apps.teams.models import Team
        
        teams = Team.objects.filter(
            is_public=True
        ).order_by('-total_points')[:20]
        
        team_data = []
        for idx, team in enumerate(teams, 1):
            team_data.append({
                'team_id': team.id,
                'team_name': team.name,
                'rank': idx,
                'score': float(team.total_points),
                'member_count': team.member_count,
                'captain': team.captain.username
            })
        
        return Response(team_data)
    
    @action(detail=False, methods=['get'])
    def my_ranking(self, request):
        """Get current user's ranking across different leaderboards."""
        user = request.user
        
        # Overall ranking
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        overall_rank = User.objects.filter(
            total_points__gt=user.total_points,
            profile__is_profile_public=True
        ).count() + 1
        
        # Weekly ranking
        from octofit_tracker.apps.activities.models import Activity
        week_start = timezone.now() - timedelta(days=7)
        
        user_weekly_points = Activity.objects.filter(
            user=user,
            activity_date__gte=week_start
        ).aggregate(total=Sum('points_earned'))['total'] or 0
        
        weekly_rank = Activity.objects.filter(
            activity_date__gte=week_start,
            user__profile__is_profile_public=True
        ).values('user').annotate(
            weekly_points=Sum('points_earned')
        ).filter(
            weekly_points__gt=user_weekly_points
        ).count() + 1
        
        # Recent achievements
        recent_achievements = UserAchievement.objects.filter(
            user=user
        ).order_by('-earned_at')[:5]
        
        summary_data = {
            'overall_rank': overall_rank,
            'overall_score': float(user.total_points),
            'weekly_rank': weekly_rank,
            'weekly_score': float(user_weekly_points),
            'total_achievements': user.achievements.count(),
            'recent_achievements': recent_achievements
        }
        
        serializer = LeaderboardSummarySerializer(summary_data)
        return Response(serializer.data)


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for achievements."""
    queryset = Achievement.objects.filter(is_active=True)
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_achievements(self, request):
        """Get current user's achievements."""
        achievements = UserAchievement.objects.filter(
            user=request.user
        ).order_by('-earned_at')
        
        serializer = UserAchievementSerializer(achievements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get achievements user hasn't earned yet."""
        user = request.user
        earned_achievement_ids = user.achievements.values_list('achievement_id', flat=True)
        
        available_achievements = Achievement.objects.filter(
            is_active=True
        ).exclude(id__in=earned_achievement_ids)
        
        serializer = self.get_serializer(available_achievements, many=True)
        return Response(serializer.data)


class WeeklyChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for weekly challenges."""
    serializer_class = WeeklyChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get weekly challenges ordered by most recent."""
        return WeeklyChallenge.objects.filter(is_active=True).order_by('-week_start')
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current week's challenge."""
        current_challenge = WeeklyChallenge.objects.filter(
            is_active=True,
            week_start__lte=timezone.now(),
            week_end__gte=timezone.now()
        ).first()
        
        if current_challenge:
            serializer = self.get_serializer(current_challenge)
            return Response(serializer.data)
        else:
            return Response({'message': 'No current weekly challenge'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a weekly challenge."""
        challenge = self.get_object()
        user = request.user
        
        # Check if challenge is current
        if not challenge.is_current:
            return Response(
                {'detail': 'Challenge is not currently active.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is already participating
        participation, created = WeeklyChallengeParticipation.objects.get_or_create(
            user=user,
            challenge=challenge
        )
        
        if not created:
            return Response(
                {'detail': 'You are already participating in this challenge.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update progress immediately
        participation.update_progress()
        
        serializer = WeeklyChallengeParticipationSerializer(participation)
        return Response({
            'message': 'Successfully joined weekly challenge!',
            'participation': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def my_participations(self, request):
        """Get current user's challenge participations."""
        participations = WeeklyChallengeParticipation.objects.filter(
            user=request.user
        ).order_by('-challenge__week_start')
        
        serializer = WeeklyChallengeParticipationSerializer(participations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        """Get leaderboard for a specific weekly challenge."""
        challenge = self.get_object()
        
        participations = WeeklyChallengeParticipation.objects.filter(
            challenge=challenge
        ).order_by('-current_value')[:50]
        
        leaderboard_data = []
        for idx, participation in enumerate(participations, 1):
            leaderboard_data.append({
                'user_id': participation.user.id,
                'username': participation.user.username,
                'full_name': participation.user.get_full_name(),
                'rank': idx,
                'score': participation.current_value,
                'is_completed': participation.is_completed,
                'progress_percentage': participation.progress_percentage
            })
        
        return Response(leaderboard_data)