"""
Views for user-related endpoints.

This module contains viewsets and views for user registration,
authentication, profiles, and fitness goals.
"""
from rest_framework import generics, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login

from .models import User, UserProfile, FitnessGoal
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserProfileSerializer,
    FitnessGoalSerializer, LoginSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """View for user registration."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """View for user login."""
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user)
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user management."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter users based on permissions."""
        if self.action == 'list':
            # Only show public profiles
            return User.objects.filter(profile__is_profile_public=True)
        return super().get_queryset()
    
    @action(detail=False, methods=['get', 'put'])
    def me(self, request):
        """Get or update current user profile."""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = self.get_serializer(
                request.user, 
                data=request.data, 
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get user fitness statistics."""
        user = self.get_object()
        
        # Check privacy settings
        if (user != request.user and 
            not user.profile.show_stats and 
            not user.profile.is_profile_public):
            return Response(
                {'detail': 'User stats are private.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        stats = {
            'total_points': user.total_points,
            'bmi': user.bmi,
            'active_goals': user.fitness_goals.filter(is_active=True).count(),
            'achieved_goals': user.fitness_goals.filter(is_achieved=True).count(),
        }
        
        return Response(stats)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profile management."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Users can only access their own profile."""
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Associate profile with current user."""
        serializer.save(user=self.request.user)


class FitnessGoalViewSet(viewsets.ModelViewSet):
    """ViewSet for fitness goal management."""
    queryset = FitnessGoal.objects.all()
    serializer_class = FitnessGoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Users can only access their own goals."""
        return FitnessGoal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Associate goal with current user."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_achieved(self, request, pk=None):
        """Mark a goal as achieved."""
        goal = self.get_object()
        goal.is_achieved = True
        goal.is_active = False
        goal.save()
        
        return Response({
            'message': 'Goal marked as achieved!',
            'goal': self.get_serializer(goal).data
        })