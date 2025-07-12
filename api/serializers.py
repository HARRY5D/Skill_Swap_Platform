"""
Serializers for API responses.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Skill, Profile, SwapRequest
from .constants import SwapStatus, ResponseStatus


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'description', 'category', 'difficulty_level',
            'availability', 'user', 'created_at'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model."""
    user = UserSerializer(read_only=True)
    skills_offered = SkillSerializer(many=True, read_only=True)
    skills_wanted = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'bio', 'location', 'phone', 
            'skills_offered', 'skills_wanted', 'availability',
            'is_public', 'visibility', 'created_at', 'updated_at'
        ]


class SwapRequestSerializer(serializers.ModelSerializer):
    """Serializer for SwapRequest model."""
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    skill_offered = SkillSerializer(read_only=True)
    skill_requested = SkillSerializer(read_only=True)
    
    class Meta:
        model = SwapRequest
        fields = [
            'id', 'sender', 'receiver', 'skill_offered', 'skill_requested',
            'status', 'message', 'created_at', 'updated_at'
        ]
        read_only_fields = ['sender', 'receiver', 'status', 'created_at', 'updated_at']


class CreateSwapRequestSerializer(serializers.Serializer):
    """Serializer for creating a new swap request."""
    receiver_id = serializers.IntegerField()
    skill_offered_id = serializers.IntegerField()
    skill_requested_id = serializers.IntegerField()
    message = serializers.CharField(required=False, allow_blank=True)
    
    def validate_receiver_id(self, value):
        """Validate receiver exists."""
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Receiver not found")
        return value
    
    def validate_skill_offered_id(self, value):
        """Validate skill offered exists."""
        try:
            Skill.objects.get(id=value)
        except Skill.DoesNotExist:
            raise serializers.ValidationError("Skill offered not found")
        return value
    
    def validate_skill_requested_id(self, value):
        """Validate skill requested exists."""
        try:
            Skill.objects.get(id=value)
        except Skill.DoesNotExist:
            raise serializers.ValidationError("Skill requested not found")
        return value


class SwapResponseSerializer(serializers.Serializer):
    """Serializer for responding to a swap request."""
    action = serializers.ChoiceField(choices=[
        ('accept', 'Accept'),
        ('reject', 'Reject'),
        ('delete', 'Delete')
    ])
    
    def validate_action(self, value):
        """Map action to status."""
        action_to_status = {
            'accept': SwapStatus.ACCEPTED,
            'reject': SwapStatus.REJECTED,
            'delete': SwapStatus.DELETED
        }
        return action_to_status.get(value)


class ProfileSearchSerializer(serializers.ModelSerializer):
    """Serializer for profile search results."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'location', 'phone']


class APIResponseSerializer(serializers.Serializer):
    """Generic API response serializer."""
    status = serializers.ChoiceField(choices=[
        (ResponseStatus.SUCCESS, 'Success'),
        (ResponseStatus.ERROR, 'Error'),
        (ResponseStatus.WARNING, 'Warning')
    ])
    message = serializers.CharField()
    data = serializers.JSONField(required=False)
    errors = serializers.ListField(child=serializers.CharField(), required=False)


class NotificationSerializer(serializers.Serializer):
    """Serializer for notifications."""
    id = serializers.IntegerField()
    action = serializers.CharField()
    timestamp = serializers.DateTimeField()
    swap_request = serializers.DictField() 