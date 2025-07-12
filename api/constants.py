"""
Constants and enums for the Skill Swap Platform.
This module contains all the constants used throughout the application
to avoid hardcoded strings and ensure consistency.
"""

# Swap Request Status Constants
class SwapStatus:
    """Constants for swap request statuses."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    COMPLETED = "completed"  # Added for completed swaps
    REJECTED = "rejected"
    DELETED = "deleted"
    
    # All valid statuses
    VALID_STATUSES = [PENDING, ACCEPTED, COMPLETED, REJECTED, DELETED]
    
    # Status transitions
    TRANSITIONS = {
        PENDING: [ACCEPTED, REJECTED, DELETED],
        ACCEPTED: [COMPLETED],  # Can transition to completed
        COMPLETED: [],  # Final state
        REJECTED: [],  # Final state
        DELETED: [],   # Final state
    }

# Availability Constants
class Availability:
    """Constants for user availability."""
    WEEKDAYS = "weekdays"
    WEEKENDS = "weekends"
    EVENINGS = "evenings"
    MORNINGS = "mornings"
    ALL_DAY = "all_day"
    
    VALID_AVAILABILITIES = [WEEKDAYS, WEEKENDS, EVENINGS, MORNINGS, ALL_DAY]

# Profile Visibility Constants
class ProfileVisibility:
    """Constants for profile visibility settings."""
    PUBLIC = "public"
    PRIVATE = "private"
    FRIENDS_ONLY = "friends_only"
    
    VALID_VISIBILITIES = [PUBLIC, PRIVATE, FRIENDS_ONLY]

# Error Messages
class ErrorMessages:
    """Centralized error messages for consistency."""
    # Swap-related errors
    SWAP_TO_SELF = "Cannot send swap request to yourself"
    DUPLICATE_PENDING = "A pending swap request already exists between these users"
    INVALID_STATUS_TRANSITION = "Invalid status transition"
    UNAUTHORIZED_ACTION = "You are not authorized to perform this action"
    SWAP_NOT_FOUND = "Swap request not found"
    INVALID_SKILL = "Invalid skill ID provided"
    
    # Profile-related errors
    PROFILE_NOT_PUBLIC = "Profile is not public"
    INCOMPATIBLE_AVAILABILITY = "User is not available for the requested time"
    PROFILE_NOT_FOUND = "Profile not found"
    
    # General errors
    INVALID_USER = "Invalid user ID"
    PERMISSION_DENIED = "Permission denied"
    VALIDATION_ERROR = "Validation error"

# Success Messages
class SuccessMessages:
    """Centralized success messages."""
    SWAP_CREATED = "Swap request created successfully"
    SWAP_UPDATED = "Swap request updated successfully"
    SWAP_DELETED = "Swap request deleted successfully"
    PROFILE_UPDATED = "Profile updated successfully"

# API Response Status
class ResponseStatus:
    """API response status constants."""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning" 