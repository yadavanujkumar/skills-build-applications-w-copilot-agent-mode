"""
Views for team-related endpoints.
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta

from .models import Team, TeamMembership, TeamChallenge, TeamInvitation
from .serializers import (
    TeamSerializer, TeamCreateSerializer, TeamMembershipSerializer,
    TeamChallengeSerializer, TeamInvitationSerializer, JoinTeamSerializer,
    TeamStatsSerializer
)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for team management."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter teams based on visibility."""
        if self.action == 'list':
            return Team.objects.filter(is_public=True)
        return Team.objects.all()
    
    def get_serializer_class(self):
        """Use different serializer for creation."""
        if self.action == 'create':
            return TeamCreateSerializer
        return TeamSerializer
    
    def perform_update(self, serializer):
        """Only team captain can update team details."""
        team = serializer.instance
        user = self.request.user
        
        # Check if user is team captain
        if team.captain != user:
            membership = team.memberships.filter(user=user, is_active=True).first()
            if not membership or membership.role not in ['captain', 'moderator']:
                raise PermissionDenied("Only team captains and moderators can update team details.")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Only team captain can delete team."""
        if instance.captain != self.request.user:
            raise PermissionDenied("Only team captains can delete teams.")
        instance.delete()
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a team."""
        team = self.get_object()
        user = request.user
        
        # Check if user is already a member
        if team.memberships.filter(user=user, is_active=True).exists():
            return Response(
                {'detail': 'You are already a member of this team.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if team is full
        if team.is_full:
            return Response(
                {'detail': 'Team is full.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = JoinTeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create membership
        membership = TeamMembership.objects.create(
            user=user,
            team=team,
            role='member',
            is_active=True,
            is_approved=not team.requires_approval
        )
        
        if team.requires_approval:
            message = "Join request sent. Waiting for approval."
        else:
            message = "Successfully joined team!"
            # Update team stats
            team.update_team_stats()
        
        return Response({
            'message': message,
            'membership': TeamMembershipSerializer(membership).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a team."""
        team = self.get_object()
        user = request.user
        
        membership = team.memberships.filter(user=user, is_active=True).first()
        if not membership:
            return Response(
                {'detail': 'You are not a member of this team.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Captain cannot leave if there are other members
        if membership.role == 'captain' and team.member_count > 1:
            return Response(
                {'detail': 'Team captain must transfer leadership before leaving.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        membership.is_active = False
        membership.left_at = timezone.now()
        membership.save()
        
        # Update team stats
        team.update_team_stats()
        
        return Response({'message': 'Successfully left team.'})
    
    @action(detail=True, methods=['post'])
    def invite(self, request, pk=None):
        """Invite a user to join the team."""
        team = self.get_object()
        user = request.user
        
        # Check permissions
        membership = team.memberships.filter(user=user, is_active=True).first()
        if not membership or membership.role not in ['captain', 'moderator']:
            raise PermissionDenied("Only team captains and moderators can invite users.")
        
        serializer = TeamInvitationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        invited_user = serializer.validated_data['invited_user']
        
        # Check if user is already a member
        if team.memberships.filter(user=invited_user, is_active=True).exists():
            return Response(
                {'detail': 'User is already a member of this team.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if invitation already exists
        if team.invitations.filter(invited_user=invited_user, is_accepted=False, is_declined=False).exists():
            return Response(
                {'detail': 'Invitation already sent to this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        invitation = TeamInvitation.objects.create(
            team=team,
            invited_user=invited_user,
            invited_by=user,
            message=serializer.validated_data.get('message', '')
        )
        
        return Response({
            'message': 'Invitation sent successfully.',
            'invitation': TeamInvitationSerializer(invitation).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get team statistics."""
        team = self.get_object()
        
        # Basic stats
        member_count = team.member_count
        avg_points = team.total_points / member_count if member_count > 0 else 0
        
        # Most active member
        from octofit_tracker.apps.activities.models import Activity
        member_users = team.memberships.filter(is_active=True).values_list('user', flat=True)
        
        most_active = Activity.objects.filter(
            user__in=member_users
        ).values('user__username').annotate(
            activity_count=Count('id')
        ).order_by('-activity_count').first()
        
        # This week stats
        week_start = timezone.now() - timedelta(days=7)
        this_week = Activity.objects.filter(
            user__in=member_users,
            activity_date__gte=week_start
        ).aggregate(
            week_points=Sum('points_earned'),
            week_activities=Count('id')
        )
        
        stats_data = {
            'total_points': team.total_points,
            'total_activities': team.total_activities,
            'member_count': member_count,
            'avg_points_per_member': round(avg_points, 2),
            'most_active_member': most_active['user__username'] if most_active else 'None',
            'this_week_points': this_week['week_points'] or 0,
            'this_week_activities': this_week['week_activities'] or 0,
        }
        
        serializer = TeamStatsSerializer(data=stats_data)
        serializer.is_valid()
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_teams(self, request):
        """Get teams the current user is a member of."""
        user = request.user
        team_ids = TeamMembership.objects.filter(
            user=user, 
            is_active=True
        ).values_list('team_id', flat=True)
        
        teams = Team.objects.filter(id__in=team_ids)
        serializer = self.get_serializer(teams, many=True)
        return Response(serializer.data)


class TeamChallengeViewSet(viewsets.ModelViewSet):
    """ViewSet for team challenge management."""
    serializer_class = TeamChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter challenges based on visibility."""
        return TeamChallenge.objects.filter(is_public=True)
    
    def perform_create(self, serializer):
        """Associate challenge with current user."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def join_challenge(self, request, pk=None):
        """Join a team challenge."""
        challenge = self.get_object()
        user = request.user
        
        # Get user's teams where they are captain or moderator
        user_teams = Team.objects.filter(
            memberships__user=user,
            memberships__is_active=True,
            memberships__role__in=['captain', 'moderator']
        )
        
        if not user_teams.exists():
            return Response(
                {'detail': 'You must be a team captain or moderator to join challenges.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get team from request data or use first available team
        team_id = request.data.get('team_id')
        if team_id:
            team = user_teams.filter(id=team_id).first()
            if not team:
                return Response(
                    {'detail': 'Invalid team or insufficient permissions.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            team = user_teams.first()
        
        # Check if team is already participating
        if challenge.teams.filter(id=team.id).exists():
            return Response(
                {'detail': 'Team is already participating in this challenge.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check challenge capacity
        if challenge.teams.count() >= challenge.max_teams:
            return Response(
                {'detail': 'Challenge is full.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        challenge.teams.add(team)
        
        return Response({
            'message': f"Team {team.name} successfully joined the challenge!",
            'challenge': self.get_serializer(challenge).data
        })


class TeamInvitationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for team invitation management."""
    serializer_class = TeamInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Show invitations for current user."""
        return TeamInvitation.objects.filter(invited_user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a team invitation."""
        invitation = self.get_object()
        
        if invitation.is_accepted or invitation.is_declined:
            return Response(
                {'detail': 'Invitation has already been responded to.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if team is full
        if invitation.team.is_full:
            return Response(
                {'detail': 'Team is full.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Accept invitation and create membership
        invitation.is_accepted = True
        invitation.responded_at = timezone.now()
        invitation.save()
        
        TeamMembership.objects.create(
            user=invitation.invited_user,
            team=invitation.team,
            role='member',
            is_active=True,
            is_approved=True
        )
        
        # Update team stats
        invitation.team.update_team_stats()
        
        return Response({'message': 'Invitation accepted! Welcome to the team!'})
    
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        """Decline a team invitation."""
        invitation = self.get_object()
        
        if invitation.is_accepted or invitation.is_declined:
            return Response(
                {'detail': 'Invitation has already been responded to.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        invitation.is_declined = True
        invitation.responded_at = timezone.now()
        invitation.save()
        
        return Response({'message': 'Invitation declined.'})