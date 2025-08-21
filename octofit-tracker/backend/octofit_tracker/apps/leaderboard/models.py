"""
Leaderboard models for OctoFit Tracker.

This module contains models for various leaderboards and rankings.
"""
from django.db import models
from django.conf import settings


class LeaderboardEntry(models.Model):
    """
    Individual leaderboard entry for tracking user rankings.
    """
    LEADERBOARD_TYPES = [
        ('overall', 'Overall Points'),
        ('weekly', 'Weekly Points'),
        ('monthly', 'Monthly Points'),
        ('activities', 'Total Activities'),
        ('duration', 'Total Duration'),
        ('consistency', 'Consistency Score'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leaderboard_entries'
    )
    leaderboard_type = models.CharField(max_length=20, choices=LEADERBOARD_TYPES)
    score = models.FloatField()
    rank = models.PositiveIntegerField()
    
    # Time period for the leaderboard
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    # Metadata
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'leaderboard_type', 'period_start', 'period_end']
        ordering = ['rank']
        indexes = [
            models.Index(fields=['leaderboard_type', 'period_start', 'period_end', 'rank']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_leaderboard_type_display()} - Rank {self.rank}"


class Achievement(models.Model):
    """
    Achievements/badges that users can earn.
    """
    ACHIEVEMENT_TYPES = [
        ('points', 'Points Milestone'),
        ('activities', 'Activity Count'),
        ('consistency', 'Consistency'),
        ('social', 'Social Interaction'),
        ('challenge', 'Challenge Completion'),
        ('special', 'Special Event'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    
    # Requirements
    required_value = models.FloatField(
        help_text="Required value to earn this achievement"
    )
    required_activity_type = models.ForeignKey(
        'activities.ActivityType',
        on_delete=models.CASCADE,
        null=True, blank=True,
        help_text="Specific activity type required (optional)"
    )
    
    # Visual representation
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default="#ffd700")  # Gold color
    badge_url = models.URLField(blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    is_repeatable = models.BooleanField(
        default=False,
        help_text="Whether users can earn this achievement multiple times"
    )
    points_reward = models.PositiveIntegerField(
        default=50,
        help_text="Bonus points awarded for earning this achievement"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['achievement_type', 'required_value']
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """
    Achievements earned by users.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='achievements'
    )
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name='user_achievements'
    )
    
    earned_at = models.DateTimeField(auto_now_add=True)
    progress_value = models.FloatField(
        help_text="The value that triggered this achievement"
    )
    
    # Optional context
    related_activity = models.ForeignKey(
        'activities.Activity',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="Activity that triggered this achievement"
    )
    
    class Meta:
        unique_together = ['user', 'achievement', 'earned_at']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} earned {self.achievement.name}"


class WeeklyChallenge(models.Model):
    """
    Weekly fitness challenges for all users.
    """
    CHALLENGE_TYPES = [
        ('step_count', 'Step Count'),
        ('activity_minutes', 'Activity Minutes'),
        ('points', 'Points Goal'),
        ('activity_variety', 'Activity Variety'),
        ('consistency', 'Daily Consistency'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES)
    target_value = models.FloatField()
    
    # Time frame
    week_start = models.DateTimeField()
    week_end = models.DateTimeField()
    
    # Rewards
    completion_points = models.PositiveIntegerField(default=100)
    bonus_achievement = models.ForeignKey(
        Achievement,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="Optional achievement awarded for completion"
    )
    
    # Participation tracking
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='WeeklyChallengeParticipation',
        related_name='weekly_challenges'
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-week_start']
    
    def __str__(self):
        return f"{self.name} ({self.week_start.strftime('%Y-%m-%d')})"
    
    @property
    def is_current(self):
        """Check if this is the current week's challenge."""
        from django.utils import timezone
        now = timezone.now()
        return self.week_start <= now <= self.week_end


class WeeklyChallengeParticipation(models.Model):
    """
    User participation in weekly challenges.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    challenge = models.ForeignKey(
        WeeklyChallenge,
        on_delete=models.CASCADE
    )
    
    # Progress tracking
    current_value = models.FloatField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    joined_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'challenge']
        ordering = ['-last_updated']
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.name}"
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage towards challenge goal."""
        if self.challenge.target_value > 0:
            return min(100, (self.current_value / self.challenge.target_value) * 100)
        return 0
    
    def update_progress(self):
        """Update progress based on user's activities."""
        from django.utils import timezone
        from octofit_tracker.apps.activities.models import Activity
        
        challenge = self.challenge
        
        # Get user activities during challenge period
        activities = Activity.objects.filter(
            user=self.user,
            activity_date__gte=challenge.week_start,
            activity_date__lte=challenge.week_end
        )
        
        # Calculate progress based on challenge type
        if challenge.challenge_type == 'activity_minutes':
            self.current_value = activities.aggregate(
                total=models.Sum('duration_minutes')
            )['total'] or 0
        elif challenge.challenge_type == 'points':
            self.current_value = activities.aggregate(
                total=models.Sum('points_earned')
            )['total'] or 0
        elif challenge.challenge_type == 'activity_variety':
            self.current_value = activities.values('activity_type').distinct().count()
        elif challenge.challenge_type == 'consistency':
            # Count unique days with activities
            unique_days = activities.dates('activity_date', 'day').count()
            self.current_value = unique_days
        
        # Check if completed
        if not self.is_completed and self.current_value >= challenge.target_value:
            self.is_completed = True
            self.completed_at = timezone.now()
            
            # Award completion points
            self.user.total_points += challenge.completion_points
            self.user.save(update_fields=['total_points'])
        
        self.save()