"""
Team models for OctoFit Tracker.

This module contains models for teams, team memberships,
and team challenges.
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Team(models.Model):
    """
    Team model for group fitness challenges.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Team settings
    is_public = models.BooleanField(
        default=True,
        help_text="Whether other users can see and join this team"
    )
    requires_approval = models.BooleanField(
        default=False,
        help_text="Whether new members need approval to join"
    )
    max_members = models.PositiveIntegerField(
        default=50,
        validators=[MinValueValidator(2), MaxValueValidator(1000)]
    )
    
    # Team leader
    captain = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='led_teams'
    )
    
    # Team stats
    total_points = models.PositiveIntegerField(default=0)
    total_activities = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Visual customization
    color = models.CharField(max_length=7, default="#007bff")  # Hex color
    logo_url = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-total_points', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def member_count(self):
        """Get current number of team members."""
        return self.memberships.filter(is_active=True).count()
    
    @property
    def is_full(self):
        """Check if team has reached maximum capacity."""
        return self.member_count >= self.max_members
    
    def update_team_stats(self):
        """Update team statistics from member activities."""
        from octofit_tracker.apps.activities.models import Activity
        
        # Get all activities from active team members
        member_users = self.memberships.filter(is_active=True).values_list('user', flat=True)
        activities = Activity.objects.filter(user__in=member_users)
        
        # Calculate totals
        totals = activities.aggregate(
            total_points=models.Sum('points_earned'),
            total_activities=models.Count('id')
        )
        
        self.total_points = totals['total_points'] or 0
        self.total_activities = totals['total_activities'] or 0
        self.save(update_fields=['total_points', 'total_activities'])


class TeamMembership(models.Model):
    """
    Membership relationship between users and teams.
    """
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('captain', 'Captain'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='team_memberships'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)  # False if team requires approval
    
    # Dates
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'team']
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} in {self.team.name}"


class TeamChallenge(models.Model):
    """
    Challenges or competitions between teams.
    """
    CHALLENGE_TYPES = [
        ('points', 'Most Points'),
        ('activities', 'Most Activities'),
        ('duration', 'Total Duration'),
        ('consistency', 'Daily Consistency'),
        ('specific_activity', 'Specific Activity'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES)
    
    # Challenge parameters
    target_value = models.FloatField(null=True, blank=True)
    specific_activity_type = models.ForeignKey(
        'activities.ActivityType',
        on_delete=models.CASCADE,
        null=True, blank=True,
        help_text="Required for specific_activity challenges"
    )
    
    # Participating teams
    teams = models.ManyToManyField(Team, related_name='challenges')
    
    # Time frame
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Challenge settings
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    max_teams = models.PositiveIntegerField(default=10)
    
    # Rewards
    winner_points_bonus = models.PositiveIntegerField(default=100)
    participant_points_bonus = models.PositiveIntegerField(default=25)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_challenges'
    )
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name
    
    @property
    def is_ongoing(self):
        """Check if challenge is currently active."""
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.is_active
    
    @property
    def is_finished(self):
        """Check if challenge has ended."""
        from django.utils import timezone
        return timezone.now() > self.end_date
    
    def get_team_results(self):
        """Get challenge results for all participating teams."""
        from django.utils import timezone
        from octofit_tracker.apps.activities.models import Activity
        
        if not self.is_finished:
            return []
        
        results = []
        for team in self.teams.all():
            # Get team member activities during challenge period
            member_users = team.memberships.filter(is_active=True).values_list('user', flat=True)
            activities = Activity.objects.filter(
                user__in=member_users,
                activity_date__gte=self.start_date,
                activity_date__lte=self.end_date
            )
            
            # Calculate team score based on challenge type
            if self.challenge_type == 'points':
                score = activities.aggregate(total=models.Sum('points_earned'))['total'] or 0
            elif self.challenge_type == 'activities':
                score = activities.count()
            elif self.challenge_type == 'duration':
                score = activities.aggregate(total=models.Sum('duration_minutes'))['total'] or 0
            elif self.challenge_type == 'specific_activity':
                score = activities.filter(
                    activity_type=self.specific_activity_type
                ).aggregate(total=models.Sum('duration_minutes'))['total'] or 0
            else:
                score = 0
            
            results.append({
                'team': team,
                'score': score,
            })
        
        # Sort by score (descending)
        results.sort(key=lambda x: x['score'], reverse=True)
        return results


class TeamInvitation(models.Model):
    """
    Invitations to join teams.
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invitations')
    invited_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='team_invitations'
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_team_invitations'
    )
    
    message = models.TextField(blank=True)
    is_accepted = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['team', 'invited_user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invitation to {self.invited_user.username} for {self.team.name}"
    
    @property
    def is_pending(self):
        """Check if invitation is still pending."""
        return not self.is_accepted and not self.is_declined