"""
Activity models for OctoFit Tracker.

This module contains models for activity types, user activities,
and workout sessions.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class ActivityType(models.Model):
    """
    Predefined activity types with point calculations.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=20,
        choices=[
            ('cardio', 'Cardiovascular'),
            ('strength', 'Strength Training'),
            ('flexibility', 'Flexibility'),
            ('sports', 'Sports'),
            ('outdoor', 'Outdoor Activities'),
            ('other', 'Other'),
        ],
        default='other'
    )
    
    # Point calculation
    points_per_minute = models.FloatField(
        default=1.0,
        help_text="Base points awarded per minute of activity"
    )
    difficulty_multiplier = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(5.0)],
        help_text="Multiplier based on activity difficulty"
    )
    
    # Display settings
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default="#007bff")  # Hex color
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name
    
    def calculate_points(self, duration_minutes, intensity=1.0):
        """Calculate points for this activity."""
        base_points = duration_minutes * self.points_per_minute
        return int(base_points * self.difficulty_multiplier * intensity)


class Activity(models.Model):
    """
    User activity log entry.
    """
    INTENSITY_CHOICES = [
        (0.5, 'Light'),
        (1.0, 'Moderate'),
        (1.5, 'Vigorous'),
        (2.0, 'Very Vigorous'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    activity_type = models.ForeignKey(
        ActivityType,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    
    # Activity details
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(600)]
    )
    intensity = models.FloatField(
        choices=INTENSITY_CHOICES,
        default=1.0
    )
    
    # Optional metrics
    distance_km = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    calories_burned = models.PositiveIntegerField(null=True, blank=True)
    heart_rate_avg = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(40), MaxValueValidator(220)]
    )
    
    # Points and tracking
    points_earned = models.PositiveIntegerField(default=0)
    date_logged = models.DateTimeField(auto_now_add=True)
    activity_date = models.DateTimeField()
    
    # Social features
    is_public = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-activity_date']
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    def save(self, *args, **kwargs):
        """Calculate points when saving."""
        if not self.points_earned:
            self.points_earned = self.activity_type.calculate_points(
                self.duration_minutes, 
                self.intensity
            )
        super().save(*args, **kwargs)
        
        # Update user's total points
        total_points = self.user.activities.aggregate(
            total=models.Sum('points_earned')
        )['total'] or 0
        self.user.total_points = total_points
        self.user.save(update_fields=['total_points'])


class WorkoutSession(models.Model):
    """
    A workout session containing multiple activities.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workout_sessions'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    activities = models.ManyToManyField(Activity, related_name='workout_sessions')
    
    total_duration_minutes = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    
    date_created = models.DateTimeField(auto_now_add=True)
    workout_date = models.DateTimeField()
    
    is_template = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-workout_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    def calculate_totals(self):
        """Calculate total duration and points from activities."""
        totals = self.activities.aggregate(
            duration=models.Sum('duration_minutes'),
            points=models.Sum('points_earned')
        )
        self.total_duration_minutes = totals['duration'] or 0
        self.total_points = totals['points'] or 0


class ActivityPhoto(models.Model):
    """
    Photos attached to activities for verification or sharing.
    """
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    image_url = models.URLField()
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.activity.name}"