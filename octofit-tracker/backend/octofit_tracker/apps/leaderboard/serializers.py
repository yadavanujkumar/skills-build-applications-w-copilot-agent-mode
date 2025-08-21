"""
Serializers for leaderboard-related models.
"""
from rest_framework import serializers
from .models import LeaderboardEntry, Achievement, UserAchievement, WeeklyChallenge, WeeklyChallengeParticipation


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    """Serializer for leaderboard entries."""
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = LeaderboardEntry
        fields = [
            'id', 'user', 'user_name', 'user_full_name', 'leaderboard_type',
            'score', 'rank', 'period_start', 'period_end', 'calculated_at'
        ]
        read_only_fields = ['id', 'calculated_at']


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for achievements."""
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'name', 'description', 'achievement_type', 'required_value',
            'required_activity_type', 'icon', 'color', 'badge_url',
            'is_active', 'is_repeatable', 'points_reward'
        ]
        read_only_fields = ['id']


class UserAchievementSerializer(serializers.ModelSerializer):
    """Serializer for user achievements."""
    achievement_name = serializers.CharField(source='achievement.name', read_only=True)
    achievement_description = serializers.CharField(source='achievement.description', read_only=True)
    achievement_icon = serializers.CharField(source='achievement.icon', read_only=True)
    achievement_color = serializers.CharField(source='achievement.color', read_only=True)
    points_reward = serializers.IntegerField(source='achievement.points_reward', read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = [
            'id', 'achievement', 'achievement_name', 'achievement_description',
            'achievement_icon', 'achievement_color', 'points_reward',
            'earned_at', 'progress_value'
        ]
        read_only_fields = ['id', 'earned_at']


class WeeklyChallengeSerializer(serializers.ModelSerializer):
    """Serializer for weekly challenges."""
    is_current = serializers.ReadOnlyField()
    participant_count = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()
    user_participation = serializers.SerializerMethodField()
    
    class Meta:
        model = WeeklyChallenge
        fields = [
            'id', 'name', 'description', 'challenge_type', 'target_value',
            'week_start', 'week_end', 'completion_points', 'is_active',
            'is_current', 'participant_count', 'completion_rate', 'user_participation'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_participant_count(self, obj):
        """Get number of participants."""
        return obj.participants.count()
    
    def get_completion_rate(self, obj):
        """Get challenge completion rate."""
        total_participants = obj.participants.count()
        if total_participants == 0:
            return 0
        
        completed = WeeklyChallengeParticipation.objects.filter(
            challenge=obj,
            is_completed=True
        ).count()
        
        return round((completed / total_participants) * 100, 1)
    
    def get_user_participation(self, obj):
        """Get current user's participation in this challenge."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            participation = WeeklyChallengeParticipation.objects.filter(
                challenge=obj,
                user=request.user
            ).first()
            
            if participation:
                return WeeklyChallengeParticipationSerializer(participation).data
        
        return None


class WeeklyChallengeParticipationSerializer(serializers.ModelSerializer):
    """Serializer for weekly challenge participation."""
    challenge_name = serializers.CharField(source='challenge.name', read_only=True)
    challenge_target = serializers.FloatField(source='challenge.target_value', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = WeeklyChallengeParticipation
        fields = [
            'id', 'challenge', 'challenge_name', 'challenge_target',
            'current_value', 'progress_percentage', 'is_completed',
            'completed_at', 'joined_at', 'last_updated'
        ]
        read_only_fields = [
            'id', 'joined_at', 'last_updated', 'completed_at', 'progress_percentage'
        ]


class LeaderboardSummarySerializer(serializers.Serializer):
    """Serializer for leaderboard summary data."""
    overall_rank = serializers.IntegerField()
    overall_score = serializers.FloatField()
    weekly_rank = serializers.IntegerField()
    weekly_score = serializers.FloatField()
    total_achievements = serializers.IntegerField()
    recent_achievements = UserAchievementSerializer(many=True)


class UserRankingSerializer(serializers.Serializer):
    """Serializer for user ranking information."""
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    full_name = serializers.CharField()
    rank = serializers.IntegerField()
    score = serializers.FloatField()
    change_from_last_period = serializers.IntegerField(allow_null=True)