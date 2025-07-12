"""
API views for the Skill Swap Platform.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Skill, Profile, SwapRequest
from .serializers import (
    SkillSerializer, ProfileSerializer, SwapRequestSerializer,
    CreateSwapRequestSerializer, SwapResponseSerializer,
    ProfileSearchSerializer, APIResponseSerializer, NotificationSerializer
)
from .services import (
    SwapWorkflowService, ProfileService, SkillService, NotificationService
)
from .constants import (
    SwapStatus, ResponseStatus, ErrorMessages, SuccessMessages
)


def create_api_response(status_type, message, data=None, errors=None):
    """
    Create a standardized API response.
    
    Args:
        status_type: ResponseStatus constant
        message: Response message
        data: Optional response data
        errors: Optional list of errors
        
    Returns:
        Response: Standardized API response
    """
    response_data = {
        'status': status_type,
        'message': message
    }
    
    if data is not None:
        response_data['data'] = data
    
    if errors is not None:
        response_data['errors'] = errors
    
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_swap_request(request):
    """
    Create a new swap request.
    
    Endpoint: POST /api/swaps/
    """
    try:
        serializer = CreateSwapRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return create_api_response(
                ResponseStatus.ERROR,
                ErrorMessages.VALIDATION_ERROR,
                errors=serializer.errors
            )
        
        # Get the validated data
        receiver_id = serializer.validated_data['receiver_id']
        skill_offered_id = serializer.validated_data['skill_offered_id']
        skill_requested_id = serializer.validated_data['skill_requested_id']
        message = serializer.validated_data.get('message', '')
        
        # Get the objects
        receiver = get_object_or_404(User, id=receiver_id)
        skill_offered = get_object_or_404(Skill, id=skill_offered_id)
        skill_requested = get_object_or_404(Skill, id=skill_requested_id)
        
        # Create the swap request using the service
        swap_request = SwapWorkflowService.create_swap_request(
            sender=request.user,
            receiver=receiver,
            skill_offered=skill_offered,
            skill_requested=skill_requested,
            message=message
        )
        
        # Serialize the response
        swap_serializer = SwapRequestSerializer(swap_request)
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            SuccessMessages.SWAP_CREATED,
            data=swap_serializer.data
        )
        
    except ValidationError as e:
        return create_api_response(
            ResponseStatus.ERROR,
            str(e),
            errors=[str(e)]
        )
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_swap(request, swap_id):
    """
    Respond to a swap request (accept/reject/delete).
    
    Endpoint: POST /api/swaps/<id>/respond/
    """
    try:
        # Get the swap request
        swap_request = get_object_or_404(SwapRequest, id=swap_id)
        
        # Validate the response data
        serializer = SwapResponseSerializer(data=request.data)
        if not serializer.is_valid():
            return create_api_response(
                ResponseStatus.ERROR,
                ErrorMessages.VALIDATION_ERROR,
                errors=serializer.errors
            )
        
        # Get the new status
        new_status = serializer.validated_data['action']
        
        # Process the response using the service
        updated_swap = SwapWorkflowService.respond_to_swap(
            swap_request=swap_request,
            user=request.user,
            new_status=new_status
        )
        
        # Serialize the response
        swap_serializer = SwapRequestSerializer(updated_swap)
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            SuccessMessages.SWAP_UPDATED,
            data=swap_serializer.data
        )
        
    except ValidationError as e:
        return create_api_response(
            ResponseStatus.ERROR,
            str(e),
            errors=[str(e)]
        )
    except PermissionDenied as e:
        return create_api_response(
            ResponseStatus.ERROR,
            str(e),
            errors=[str(e)]
        )
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_swaps(request):
    """
    List user's swaps (sent and received).
    
    Endpoint: GET /api/swaps/
    """
    try:
        # Get query parameters
        status_filter = request.GET.get('status')
        swap_type = request.GET.get('type', 'all')  # 'sent', 'received', 'all'
        
        # Get swaps for the user
        swaps = ProfileService.get_user_swap_history(request.user)
        
        # Apply filters
        if status_filter:
            swaps = swaps.filter(status=status_filter)
        
        if swap_type == 'sent':
            swaps = swaps.filter(sender=request.user)
        elif swap_type == 'received':
            swaps = swaps.filter(receiver=request.user)
        
        # Serialize the response
        swap_serializer = SwapRequestSerializer(swaps, many=True)
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            "Swaps retrieved successfully",
            data=swap_serializer.data
        )
        
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pending_swaps(request):
    """
    Get pending swaps for the user.
    
    Endpoint: GET /api/swaps/pending/
    """
    try:
        # Get pending swaps
        pending_swaps = ProfileService.get_pending_swaps_for_user(request.user)
        
        # Serialize the response
        swap_serializer = SwapRequestSerializer(pending_swaps, many=True)
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            "Pending swaps retrieved successfully",
            data=swap_serializer.data
        )
        
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_profiles(request):
    """
    Search public profiles by skill.
    
    Endpoint: GET /api/profiles/search/
    """
    try:
        # Validate search parameters
        serializer = ProfileSearchSerializer(data=request.GET)
        if not serializer.is_valid():
            return create_api_response(
                ResponseStatus.ERROR,
                ErrorMessages.VALIDATION_ERROR,
                errors=serializer.errors
            )
        
        # Get search parameters
        skill_name = serializer.validated_data.get('skill', '')
        availability = serializer.validated_data.get('availability', '')
        location = serializer.validated_data.get('location', '')
        
        # Get public profiles
        profiles = ProfileService.get_public_profiles()
        
        # Apply filters
        if skill_name:
            profiles = ProfileService.search_profiles_by_skill(skill_name)
        
        if availability:
            profiles = profiles.filter(availability=availability)
        
        if location:
            profiles = profiles.filter(location__icontains=location)
        
        # Serialize the response
        profile_serializer = ProfileSerializer(profiles, many=True)
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            "Profiles retrieved successfully",
            data=profile_serializer.data
        )
        
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_skills(request):
    """
    List all available skills.
    
    Endpoint: GET /api/skills/
    """
    try:
        # Get query parameters
        category = request.GET.get('category')
        search = request.GET.get('search')
        
        # Get skills
        if category:
            skills = SkillService.get_skills_by_category(category)
        elif search:
            skills = SkillService.search_skills(search)
        else:
            skills = SkillService.get_all_skills()
        
        # Serialize the response
        skill_serializer = SkillSerializer(skills, many=True)
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            "Skills retrieved successfully",
            data=skill_serializer.data
        )
        
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    """
    Get notifications for the user (optional bonus feature).
    
    Endpoint: GET /api/notifications/
    """
    try:
        # Get notifications
        notifications = NotificationService.get_user_notifications(request.user)
        
        # Serialize the response
        notification_serializer = NotificationSerializer(notifications, many=True)
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            "Notifications retrieved successfully",
            data=notification_serializer.data
        )
        
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_swap_details(request, swap_id):
    """
    Get detailed information about a specific swap.
    
    Endpoint: GET /api/swaps/<id>/
    """
    try:
        # Get the swap request
        swap_request = get_object_or_404(SwapRequest, id=swap_id)
        
        # Check if user is involved in this swap
        if swap_request.sender != request.user and swap_request.receiver != request.user:
            return create_api_response(
                ResponseStatus.ERROR,
                ErrorMessages.PERMISSION_DENIED,
                errors=[ErrorMessages.PERMISSION_DENIED]
            )
        
        # Serialize the response
        swap_serializer = SwapRequestSerializer(swap_request)
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            "Swap details retrieved successfully",
            data=swap_serializer.data
        )
        
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        ) 