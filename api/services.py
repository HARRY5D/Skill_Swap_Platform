"""
Service layer for business logic and workflow management.
This module contains all the core business logic for the Skill Swap Platform.
"""

from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models import Q

from .models import Skill, Profile, SwapRequest
from .constants import (
    SwapStatus, Availability, ProfileVisibility, 
    ErrorMessages, SuccessMessages
)


class SwapValidationService:
    """Service for validating swap requests and business rules."""
    
    @staticmethod
    def validate_swap_creation(sender, receiver, skill_offered, skill_requested):
        """
        Validate a new swap request creation.
        
        Args:
            sender: User sending the swap request
            receiver: User receiving the swap request
            skill_offered: Skill being offered by sender
            skill_requested: Skill being requested by sender
            
        Raises:
            ValidationError: If validation fails
        """
        # Check if sender is trying to swap with themselves
        if sender == receiver:
            raise ValidationError(ErrorMessages.SWAP_TO_SELF)
        
        # Check if receiver has a public profile
        try:
            receiver_profile = Profile.objects.get(user=receiver)
            if not receiver_profile.is_available_for_swap:
                raise ValidationError(ErrorMessages.PROFILE_NOT_PUBLIC)
        except Profile.DoesNotExist:
            raise ValidationError(ErrorMessages.PROFILE_NOT_FOUND)
        
        # Check if sender has the skill they're offering
        sender_profile = Profile.objects.get(user=sender)
        if skill_offered not in sender_profile.skills_offered.all():
            raise ValidationError(f"You don't have the skill '{skill_offered.name}' to offer")
        
        # Check if receiver has the skill they're being asked to offer
        if skill_requested not in receiver_profile.skills_offered.all():
            raise ValidationError(f"Receiver doesn't have the skill '{skill_requested.name}' to offer")
        
        # Check for existing pending swap
        existing_pending = SwapRequest.objects.filter(
            Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender),
            status=SwapStatus.PENDING
        ).exists()
        
        if existing_pending:
            raise ValidationError(ErrorMessages.DUPLICATE_PENDING)
    
    @staticmethod
    def validate_swap_response(swap_request, user, new_status):
        """
        Validate a swap response (accept/reject/delete).
        
        Args:
            swap_request: The SwapRequest object
            user: User performing the action
            new_status: New status to transition to
            
        Raises:
            ValidationError: If validation fails
            PermissionDenied: If user is not authorized
        """
        # Check if status transition is valid
        if not swap_request.can_transition_to(new_status):
            raise ValidationError(ErrorMessages.INVALID_STATUS_TRANSITION)
        
        # Check authorization based on action
        if new_status == SwapStatus.DELETED:
            if user != swap_request.sender:
                raise PermissionDenied(ErrorMessages.UNAUTHORIZED_ACTION)
        elif new_status in [SwapStatus.ACCEPTED, SwapStatus.REJECTED]:
            if user != swap_request.receiver:
                raise PermissionDenied(ErrorMessages.UNAUTHORIZED_ACTION)


class SwapWorkflowService:
    """Service for managing swap workflow and state transitions."""
    
    @staticmethod
    @transaction.atomic
    def create_swap_request(sender, receiver, skill_offered, skill_requested, message=""):
        """
        Create a new swap request with full validation.
        
        Args:
            sender: User sending the request
            receiver: User receiving the request
            skill_offered: Skill being offered
            skill_requested: Skill being requested
            message: Optional message from sender
            
        Returns:
            SwapRequest: The created swap request
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate the swap request
        SwapValidationService.validate_swap_creation(
            sender, receiver, skill_offered, skill_requested
        )
        
        # Create the swap request
        swap_request = SwapRequest.objects.create(
            sender=sender,
            receiver=receiver,
            skill_offered=skill_offered,
            skill_requested=skill_requested,
            message=message,
            status=SwapStatus.PENDING
        )
        
        return swap_request
    
    @staticmethod
    @transaction.atomic
    def respond_to_swap(swap_request, user, new_status):
        """
        Respond to a swap request (accept/reject/delete).
        
        Args:
            swap_request: The SwapRequest object
            user: User performing the action
            new_status: New status to transition to
            
        Returns:
            SwapRequest: The updated swap request
            
        Raises:
            ValidationError: If validation fails
            PermissionDenied: If user is not authorized
        """
        # Validate the response
        SwapValidationService.validate_swap_response(swap_request, user, new_status)
        
        # Update the status
        swap_request.status = new_status
        swap_request.save()
        
        return swap_request


class ProfileService:
    """Service for profile-related operations."""
    
    @staticmethod
    def get_public_profiles():
        """Get all public profiles available for swaps."""
        return Profile.objects.filter(
            is_public=True,
            visibility=ProfileVisibility.PUBLIC
        ).select_related('user').prefetch_related('skills_offered', 'skills_wanted')
    
    @staticmethod
    def search_profiles_by_skill(skill_name):
        """
        Search public profiles by skill name.
        
        Args:
            skill_name: Name of the skill to search for
            
        Returns:
            QuerySet: Profiles that offer the specified skill
        """
        return Profile.objects.filter(
            is_public=True,
            visibility=ProfileVisibility.PUBLIC,
            skills_offered__name__icontains=skill_name
        ).select_related('user').prefetch_related('skills_offered', 'skills_wanted')
    
    @staticmethod
    def get_user_swap_history(user):
        """
        Get all swaps for a user (sent and received).
        
        Args:
            user: User to get swap history for
            
        Returns:
            QuerySet: All swaps involving the user
        """
        return SwapRequest.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related(
            'sender', 'receiver', 'skill_offered', 'skill_requested'
        ).order_by('-created_at')
    
    @staticmethod
    def get_pending_swaps_for_user(user):
        """
        Get pending swaps for a user.
        
        Args:
            user: User to get pending swaps for
            
        Returns:
            QuerySet: Pending swaps for the user
        """
        return SwapRequest.objects.filter(
            Q(sender=user) | Q(receiver=user),
            status=SwapStatus.PENDING
        ).select_related(
            'sender', 'receiver', 'skill_offered', 'skill_requested'
        ).order_by('-created_at')


class SkillService:
    """Service for skill-related operations."""
    
    @staticmethod
    def get_all_skills():
        """Get all available skills."""
        return Skill.objects.all().order_by('name')
    
    @staticmethod
    def get_skills_by_category(category):
        """
        Get skills by category.
        
        Args:
            category: Category to filter by
            
        Returns:
            QuerySet: Skills in the specified category
        """
        return Skill.objects.filter(category=category).order_by('name')
    
    @staticmethod
    def search_skills(query):
        """
        Search skills by name or description.
        
        Args:
            query: Search query
            
        Returns:
            QuerySet: Matching skills
        """
        return Skill.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).order_by('name')


class NotificationService:
    """Service for handling notifications (optional bonus feature)."""
    
    @staticmethod
    def create_swap_notification(swap_request, action):
        """
        Create a notification for a swap action.
        
        Args:
            swap_request: The SwapRequest object
            action: Action performed (created, accepted, rejected, etc.)
            
        Returns:
            dict: Notification data
        """
        notification = {
            'id': swap_request.id,
            'action': action,
            'timestamp': swap_request.updated_at,
            'swap_request': {
                'sender': swap_request.sender.username,
                'receiver': swap_request.receiver.username,
                'skill_offered': swap_request.skill_offered.name,
                'skill_requested': swap_request.skill_requested.name,
                'status': swap_request.status,
            }
        }
        
        return notification
    
    @staticmethod
    def get_user_notifications(user):
        """
        Get notifications for a user.
        
        Args:
            user: User to get notifications for
            
        Returns:
            list: List of notification data
        """
        # Get recent swap activities for the user
        recent_swaps = SwapRequest.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-updated_at')[:10]
        
        notifications = []
        for swap in recent_swaps:
            if swap.status != SwapStatus.PENDING:
                action = f"swap_{swap.status}"
                notifications.append(
                    NotificationService.create_swap_notification(swap, action)
                )
        
        return notifications 