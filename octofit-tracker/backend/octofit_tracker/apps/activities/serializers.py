"""
Serializers for activity-related models.
"""
from rest_framework import serializers
from .models import ActivityType, Activity, WorkoutSession, ActivityPhoto


class ActivityTypeSerializer(serializers.ModelSerializer):
    """Serializer for activity types."""
    
    class Meta:
        model = ActivityType
        fields = [
            'id', 'name', 'description', 'category', 'points_per_minute',
            'difficulty_multiplier', 'icon', 'color', 'is_active'
        ]
        read_only_fields = ['id']


class ActivityPhotoSerializer(serializers.ModelSerializer):
    """Serializer for activity photos."""
    
    class Meta:
        model = ActivityPhoto
        fields = ['id', 'image_url', 'caption', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for activities."""
    activity_type_name = serializers.CharField(source='activity_type.name', read_only=True)
    activity_type_category = serializers.CharField(source='activity_type.category', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    photos = ActivityPhotoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 'name', 'description', 'activity_type', 'activity_type_name',
            'activity_type_category', 'duration_minutes', 'intensity',
            'distance_km', 'calories_burned', 'heart_rate_avg',
            'points_earned', 'date_logged', 'activity_date',
            'is_public', 'notes', 'user_name', 'photos'
        ]
        read_only_fields = ['id', 'points_earned', 'date_logged', 'user_name']
    
    def validate_activity_date(self, value):
        """Ensure activity date is not in the future."""
        from django.utils import timezone
        if value > timezone.now():
            raise serializers.ValidationError("Activity date cannot be in the future.")
        return value


class ActivityCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating activities."""
    
    class Meta:
        model = Activity
        fields = [
            'name', 'activity_type', 'duration_minutes', 'intensity',
            'distance_km', 'calories_burned', 'heart_rate_avg',
            'activity_date', 'is_public', 'notes'
        ]
    
    def validate_activity_date(self, value):
        """Ensure activity date is not in the future."""
        from django.utils import timezone
        if value > timezone.now():
            raise serializers.ValidationError("Activity date cannot be in the future.")
        return value


class WorkoutSessionSerializer(serializers.ModelSerializer):
    """Serializer for workout sessions."""
    activities = ActivitySerializer(many=True, read_only=True)
    activity_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = WorkoutSession
        fields = [
            'id', 'name', 'description', 'activities', 'activity_ids',
            'total_duration_minutes', 'total_points', 'date_created',
            'workout_date', 'is_template', 'is_public', 'user_name'
        ]
        read_only_fields = [
            'id', 'total_duration_minutes', 'total_points', 
            'date_created', 'user_name'
        ]
    
    def create(self, validated_data):
        """Create workout session with activities."""
        activity_ids = validated_data.pop('activity_ids', [])
        workout = WorkoutSession.objects.create(**validated_data)
        
        if activity_ids:
            # Filter activities to only include user's own activities
            user_activities = Activity.objects.filter(
                id__in=activity_ids,
                user=validated_data['user']
            )
            workout.activities.set(user_activities)
            workout.calculate_totals()
            workout.save()
        
        return workout
    
    def update(self, instance, validated_data):
        """Update workout session."""
        activity_ids = validated_data.pop('activity_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if activity_ids is not None:
            # Filter activities to only include user's own activities
            user_activities = Activity.objects.filter(
                id__in=activity_ids,
                user=instance.user
            )
            instance.activities.set(user_activities)
            instance.calculate_totals()
        
        instance.save()
        return instance


class ActivitySummarySerializer(serializers.Serializer):
    """Serializer for activity summary statistics."""
    total_activities = serializers.IntegerField()
    total_duration_minutes = serializers.IntegerField()
    total_points = serializers.IntegerField()
    average_intensity = serializers.FloatField()
    most_common_activity = serializers.CharField()
    this_week_activities = serializers.IntegerField()
    this_week_points = serializers.IntegerField()