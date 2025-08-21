"""
User models for OctoFit Tracker.

This module contains the user-related models including user profiles,
authentication, and fitness preferences.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """
    Extended user model for OctoFit Tracker.
    
    Adds fitness-specific fields to the standard Django User model.
    """
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    grade_level = models.CharField(
        max_length=2,
        choices=[
            ('9', '9th Grade'),
            ('10', '10th Grade'),
            ('11', '11th Grade'),
            ('12', '12th Grade'),
        ],
        null=True,
        blank=True
    )
    
    # Fitness metrics
    height_cm = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(100), MaxValueValidator(250)]
    )
    weight_kg = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(200)]
    )
    
    # Preferences
    fitness_goals = models.TextField(blank=True)
    preferred_activities = models.TextField(
        blank=True,
        help_text="Comma-separated list of preferred activities"
    )
    
    # Tracking
    total_points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"
    
    @property
    def bmi(self):
        """Calculate Body Mass Index if height and weight are available."""
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            return round(self.weight_kg / (height_m * height_m), 1)
        return None


class UserProfile(models.Model):
    """
    Extended profile information for users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar_url = models.URLField(blank=True)
    
    # Privacy settings
    is_profile_public = models.BooleanField(default=True)
    show_real_name = models.BooleanField(default=True)
    show_stats = models.BooleanField(default=True)
    
    # Notifications
    email_notifications = models.BooleanField(default=True)
    weekly_summary = models.BooleanField(default=True)
    team_updates = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"


class FitnessGoal(models.Model):
    """
    Individual fitness goals for users.
    """
    GOAL_TYPES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('endurance', 'Endurance'),
        ('strength', 'Strength'),
        ('flexibility', 'Flexibility'),
        ('general_fitness', 'General Fitness'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fitness_goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    description = models.TextField()
    target_value = models.FloatField(null=True, blank=True)
    current_value = models.FloatField(default=0)
    target_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_achieved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_goal_type_display()}"
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage towards goal."""
        if self.target_value and self.target_value > 0:
            return min(100, (self.current_value / self.target_value) * 100)
        return 0