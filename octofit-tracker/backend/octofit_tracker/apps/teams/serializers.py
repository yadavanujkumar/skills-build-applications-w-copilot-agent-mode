"""
Serializers for team-related models.
"""
from rest_framework import serializers
from django.utils import timezone
from .models import Team, TeamMembership, TeamChallenge, TeamInvitation


class TeamMembershipSerializer(serializers.ModelSerializer):
    """Serializer for team memberships."""
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = TeamMembership
        fields = [
            'id', 'user', 'user_name', 'user_full_name', 'role',
            'is_active', 'is_approved', 'joined_at'
        ]
        read_only_fields = ['id', 'joined_at']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for teams."""
    captain_name = serializers.CharField(source='captain.username', read_only=True)
    member_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    is_member = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()
    members = TeamMembershipSerializer(source='memberships', many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'is_public', 'requires_approval',
            'max_members', 'captain', 'captain_name', 'total_points',
            'total_activities', 'member_count', 'is_full', 'created_at',
            'color', 'logo_url', 'is_member', 'user_role', 'members'
        ]
        read_only_fields = ['id', 'total_points', 'total_activities', 'created_at']
    
    def get_is_member(self, obj):
        """Check if current user is a member of this team."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.memberships.filter(
                user=request.user, 
                is_active=True
            ).exists()
        return False
    
    def get_user_role(self, obj):
        """Get current user's role in this team."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            membership = obj.memberships.filter(
                user=request.user, 
                is_active=True
            ).first()
            return membership.role if membership else None
        return None


class TeamCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating teams."""
    
    class Meta:
        model = Team
        fields = [
            'name', 'description', 'is_public', 'requires_approval',
            'max_members', 'color', 'logo_url'
        ]
    
    def create(self, validated_data):
        """Create team with current user as captain."""
        request = self.context.get('request')
        team = Team.objects.create(captain=request.user, **validated_data)
        
        # Add creator as captain member
        TeamMembership.objects.create(
            user=request.user,
            team=team,
            role='captain',
            is_active=True,
            is_approved=True
        )
        
        return team


class TeamChallengeSerializer(serializers.ModelSerializer):
    """Serializer for team challenges."""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    participating_teams = TeamSerializer(source='teams', many=True, read_only=True)
    is_ongoing = serializers.ReadOnlyField()
    is_finished = serializers.ReadOnlyField()
    team_results = serializers.SerializerMethodField()
    
    class Meta:
        model = TeamChallenge
        fields = [
            'id', 'name', 'description', 'challenge_type', 'target_value',
            'specific_activity_type', 'start_date', 'end_date', 'is_active',
            'is_public', 'max_teams', 'winner_points_bonus',
            'participant_points_bonus', 'created_at', 'created_by',
            'created_by_name', 'participating_teams', 'is_ongoing',
            'is_finished', 'team_results'
        ]
        read_only_fields = ['id', 'created_at', 'created_by']
    
    def get_team_results(self, obj):
        """Get challenge results if challenge is finished."""
        if obj.is_finished:
            results = obj.get_team_results()
            return [
                {
                    'team_id': result['team'].id,
                    'team_name': result['team'].name,
                    'score': result['score'],
                    'rank': idx + 1
                }
                for idx, result in enumerate(results)
            ]
        return None
    
    def validate(self, data):
        """Validate challenge dates."""
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        
        if data['start_date'] < timezone.now():
            raise serializers.ValidationError("Start date cannot be in the past.")
        
        return data


class TeamInvitationSerializer(serializers.ModelSerializer):
    """Serializer for team invitations."""
    team_name = serializers.CharField(source='team.name', read_only=True)
    invited_by_name = serializers.CharField(source='invited_by.username', read_only=True)
    invited_user_name = serializers.CharField(source='invited_user.username', read_only=True)
    is_pending = serializers.ReadOnlyField()
    
    class Meta:
        model = TeamInvitation
        fields = [
            'id', 'team', 'team_name', 'invited_user', 'invited_user_name',
            'invited_by', 'invited_by_name', 'message', 'is_accepted',
            'is_declined', 'is_pending', 'created_at', 'responded_at'
        ]
        read_only_fields = [
            'id', 'invited_by', 'created_at', 'responded_at', 'is_pending'
        ]


class JoinTeamSerializer(serializers.Serializer):
    """Serializer for joining a team."""
    message = serializers.CharField(max_length=500, required=False, allow_blank=True)


class TeamStatsSerializer(serializers.Serializer):
    """Serializer for team statistics."""
    total_points = serializers.IntegerField()
    total_activities = serializers.IntegerField()
    member_count = serializers.IntegerField()
    avg_points_per_member = serializers.FloatField()
    most_active_member = serializers.CharField()
    this_week_points = serializers.IntegerField()
    this_week_activities = serializers.IntegerField()