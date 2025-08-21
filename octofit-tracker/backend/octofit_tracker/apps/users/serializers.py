"""
Serializers for user-related models.

These serializers convert ObjectId fields to strings and handle
API serialization for the users app.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile, FitnessGoal


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm', 'date_of_birth', 'grade_level'
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profiles."""
    bmi = serializers.ReadOnlyField(source='user.bmi')
    
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'avatar_url', 'is_profile_public', 'show_real_name',
            'show_stats', 'email_notifications', 'weekly_summary',
            'team_updates', 'bmi'
        ]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details."""
    profile = UserProfileSerializer(read_only=True)
    bmi = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_of_birth', 'grade_level', 'height_cm', 'weight_kg',
            'fitness_goals', 'preferred_activities', 'total_points',
            'profile', 'bmi', 'date_joined'
        ]
        read_only_fields = ['id', 'total_points', 'date_joined']


class FitnessGoalSerializer(serializers.ModelSerializer):
    """Serializer for fitness goals."""
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = FitnessGoal
        fields = [
            'id', 'goal_type', 'description', 'target_value',
            'current_value', 'target_date', 'is_active',
            'is_achieved', 'progress_percentage', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'progress_percentage']


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Invalid username or password.')
        else:
            raise serializers.ValidationError('Must provide username and password.')
        
        return data