"""
Database models for the Skill Swap Platform.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from .constants import SwapStatus, Availability, ProfileVisibility


class Skill(models.Model):
    """
    Model representing skills that users can offer or request.
    """
    name = models.CharField(
        max_length=100, 
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    Extended user profile with skills, availability, and visibility settings.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    
    # Skills relationship
    skills_offered = models.ManyToManyField(
        Skill, 
        related_name='users_offering',
        blank=True
    )
    skills_wanted = models.ManyToManyField(
        Skill, 
        related_name='users_wanting',
        blank=True
    )
    
    # Availability settings
    availability = models.CharField(
        max_length=20,
        choices=[(av, av.title()) for av in Availability.VALID_AVAILABILITIES],
        default=Availability.WEEKENDS
    )
    
    # Profile visibility
    is_public = models.BooleanField(default=True)
    visibility = models.CharField(
        max_length=20,
        choices=[(vis, vis.title()) for vis in ProfileVisibility.VALID_VISIBILITIES],
        default=ProfileVisibility.PUBLIC
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def is_available_for_swap(self):
        """Check if user is available for skill swaps."""
        return self.is_public and self.visibility == ProfileVisibility.PUBLIC

    def get_available_skills(self):
        """Get skills that the user is offering."""
        return self.skills_offered.all()

    def get_wanted_skills(self):
        """Get skills that the user wants to learn."""
        return self.skills_wanted.all()


class SwapRequest(models.Model):
    """
    Model representing a skill swap request between two users.
    """
    # Users involved in the swap
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_swaps'
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_swaps'
    )
    
    # Skills being exchanged
    skill_offered = models.ForeignKey(
        Skill, 
        on_delete=models.CASCADE, 
        related_name='swaps_offering'
    )
    skill_requested = models.ForeignKey(
        Skill, 
        on_delete=models.CASCADE, 
        related_name='swaps_requesting'
    )
    
    # Swap status and metadata
    status = models.CharField(
        max_length=20,
        choices=[(status, status.title()) for status in SwapStatus.VALID_STATUSES],
        default=SwapStatus.PENDING
    )
    
    # Optional message from sender
    message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # Ensure only one pending swap between two users
        unique_together = ['sender', 'receiver', 'status']
        indexes = [
            models.Index(fields=['sender', 'status']),
            models.Index(fields=['receiver', 'status']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.skill_offered} ↔ {self.skill_requested}"

    def can_transition_to(self, new_status):
        """Check if the swap can transition to the new status."""
        return new_status in SwapStatus.TRANSITIONS.get(self.status, [])

    def is_authorized_user(self, user):
        """Check if user is authorized to modify this swap request."""
        if new_status == SwapStatus.DELETED:
            return user == self.sender
        elif new_status in [SwapStatus.ACCEPTED, SwapStatus.REJECTED]:
            return user == self.receiver
        return False

    def get_swap_partner(self, user):
        """Get the other user in the swap."""
        if user == self.sender:
            return self.receiver
        elif user == self.receiver:
            return self.sender
        return None 