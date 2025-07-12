"""
Admin configuration for the Skill Swap Platform.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Skill, Profile, SwapRequest
from .constants import SwapStatus, Availability, ProfileVisibility


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin configuration for Skill model."""
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description', 'category']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profile model."""
    list_display = ['user', 'location', 'availability', 'visibility', 'is_public', 'created_at']
    list_filter = ['availability', 'visibility', 'is_public', 'created_at']
    search_fields = ['user__username', 'user__email', 'location', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['skills_offered', 'skills_wanted']
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        return super().get_queryset(request).select_related('user')


@admin.register(SwapRequest)
class SwapRequestAdmin(admin.ModelAdmin):
    """Admin configuration for SwapRequest model."""
    list_display = [
        'id', 'sender', 'receiver', 'skill_offered', 'skill_requested', 
        'status', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = [
        'sender__username', 'receiver__username', 
        'skill_offered__name', 'skill_requested__name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        return super().get_queryset(request).select_related(
            'sender', 'receiver', 'skill_offered', 'skill_requested'
        )
    
    def has_add_permission(self, request):
        """Disable manual creation of swap requests."""
        return False


# Customize User admin to include profile information
class ProfileInline(admin.StackedInline):
    """Inline profile for User admin."""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    """Custom User admin with profile inline."""
    inlines = (ProfileInline,)
    
    def get_inline_instances(self, request, obj=None):
        """Only show profile inline when editing existing user."""
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


# Re-register User admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin) 