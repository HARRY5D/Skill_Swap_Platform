"""
API views for the Skill Swap Platform.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction

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


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for the API.
    
    Endpoint: GET /api/health/
    """
    return create_api_response(
        ResponseStatus.SUCCESS,
        "API is healthy and running",
        data={
            'status': 'healthy',
            'timestamp': '2024-01-01T00:00:00Z',
            'version': '1.0.0'
        }
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    User login endpoint.
    
    Endpoint: POST /api/auth/login/
    """
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return create_api_response(
                ResponseStatus.ERROR,
                "Email and password are required",
                errors=["Email and password are required"]
            )
        
        # Try to authenticate with email
        user = authenticate(username=email, password=password)
        
        if user is None:
            return create_api_response(
                ResponseStatus.ERROR,
                "Invalid credentials",
                errors=["Invalid email or password"]
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Get user profile
        profile, created = Profile.objects.get_or_create(user=user)
        
        user_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': profile.bio,
            'location': profile.location,
            'phone': profile.phone
        }
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            "Login successful",
            data={
                'token': access_token,
                'user': user_data
            }
        )
        
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    User registration endpoint.
    
    Endpoint: POST /api/auth/register/
    """
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        
        if not email or not password:
            return create_api_response(
                ResponseStatus.ERROR,
                "Email and password are required",
                errors=["Email and password are required"]
            )
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return create_api_response(
                ResponseStatus.ERROR,
                "User with this email already exists",
                errors=["Email already registered"]
            )
        
        with transaction.atomic():
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create profile
            profile = Profile.objects.create(user=user)
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'bio': profile.bio,
                'location': profile.location,
                'phone': profile.phone
            }
            
            return create_api_response(
                ResponseStatus.SUCCESS,
                "Registration successful",
                data={
                    'token': access_token,
                    'user': user_data
                }
            )
        
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    Get current user profile.
    
    Endpoint: GET /api/auth/me/
    """
    try:
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        
        user_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': profile.bio,
            'location': profile.location,
            'phone': profile.phone
        }
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            "Profile retrieved successfully",
            data=user_data
        )
        
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Update user profile.
    
    Endpoint: PUT /api/auth/profile/
    """
    try:
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        
        # Update user fields
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'email' in request.data:
            user.email = request.data['email']
        
        user.save()
        
        # Update profile fields
        if 'bio' in request.data:
            profile.bio = request.data['bio']
        if 'location' in request.data:
            profile.location = request.data['location']
        if 'phone' in request.data:
            profile.phone = request.data['phone']
        
        profile.save()
        
        user_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': profile.bio,
            'location': profile.location,
            'phone': profile.phone
        }
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            "Profile updated successfully",
            data=user_data
        )
        
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats_view(request):
    """
    Get dashboard statistics.
    
    Endpoint: GET /api/dashboard/stats/
    """
    try:
        user = request.user
        
        # Get user's skills count
        total_skills = Skill.objects.filter(user=user).count()
        
        # Get active swaps count (sent by user, pending)
        active_swaps = SwapRequest.objects.filter(
            sender=user,
            status=SwapStatus.PENDING
        ).count()
        
        # Get completed swaps count (sent by user, completed)
        completed_swaps = SwapRequest.objects.filter(
            sender=user,
            status=SwapStatus.COMPLETED
        ).count()
        
        # Get pending requests count (received by user, pending)
        pending_requests = SwapRequest.objects.filter(
            receiver=user,
            status=SwapStatus.PENDING
        ).count()
        
        stats = {
            'totalSkills': total_skills,
            'activeSwaps': active_swaps,
            'completedSwaps': completed_swaps,
            'pendingRequests': pending_requests
        }
        
        # Add debug info
        print(f"Dashboard stats for user {user.id}: {stats}")
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            "Dashboard stats retrieved successfully",
            data=stats
        )
        
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_skills_view(request):
    """
    Get current user's skills.
    
    Endpoint: GET /api/skills/my-skills/
    """
    try:
        user = request.user
        skills = Skill.objects.filter(user=user)
        
        serializer = SkillSerializer(skills, many=True)
        
        return create_api_response(
            ResponseStatus.SUCCESS,
            "Skills retrieved successfully",
            data=serializer.data
        )
        
    except Exception as e:
        return create_api_response(
            ResponseStatus.ERROR,
            "An unexpected error occurred",
            errors=[str(e)]
        )


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
    Get pending swap requests for the user.
    
    Endpoint: GET /api/swaps/pending/
    """
    try:
        # Get pending swaps where user is the receiver
        pending_swaps = SwapRequest.objects.filter(
            receiver=request.user,
            status=SwapStatus.PENDING
        )
        
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
    Search for user profiles.
    
    Endpoint: GET /api/profiles/search/
    """
    try:
        # Get query parameters
        query = request.GET.get('q', '')
        skill_category = request.GET.get('category', '')
        location = request.GET.get('location', '')
        
        # Get all profiles
        profiles = Profile.objects.all()
        
        # Apply filters
        if query:
            profiles = profiles.filter(
                user__first_name__icontains=query
            ) | profiles.filter(
                user__last_name__icontains=query
            ) | profiles.filter(
                bio__icontains=query
            )
        
        if location:
            profiles = profiles.filter(location__icontains=location)
        
        if skill_category:
            profiles = profiles.filter(
                user__skill__category=skill_category
            ).distinct()
        
        # Serialize the response
        profile_serializer = ProfileSearchSerializer(profiles, many=True)
        
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


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow public access for GET
def list_skills(request):
    """
    List all available skills or create a new skill.
    
    Endpoint: GET /api/skills/ - List skills (public)
    Endpoint: POST /api/skills/ - Create skill (requires auth)
    """
    if request.method == 'GET':
        try:
            # Get query parameters
            category = request.GET.get('category', '')
            difficulty_level = request.GET.get('difficulty_level', '')
            search = request.GET.get('search', '')
            
            # Get all skills
            skills = Skill.objects.all()
            
            # Apply filters
            if category:
                skills = skills.filter(category=category)
            
            if difficulty_level:
                skills = skills.filter(difficulty_level=difficulty_level)
            
            if search:
                skills = skills.filter(
                    name__icontains=search
                ) | skills.filter(
                    description__icontains=search
                )
            
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
    
    elif request.method == 'POST':
        # Check if user is authenticated for POST
        if not request.user.is_authenticated:
            return create_api_response(
                ResponseStatus.ERROR,
                "Authentication required to create skills",
                errors=["Please log in to create skills"]
            )
        
        try:
            # Add user to the data
            data = request.data.copy()
            data['user'] = request.user.id
            
            # Validate and create skill
            serializer = SkillSerializer(data=data)
            if serializer.is_valid():
                skill = serializer.save()
                return create_api_response(
                    ResponseStatus.SUCCESS,
                    "Skill created successfully",
                    data=serializer.data
                )
            else:
                return create_api_response(
                    ResponseStatus.ERROR,
                    "Validation error",
                    errors=serializer.errors
                )
                
        except Exception as e:
            return create_api_response(
                ResponseStatus.ERROR,
                "An unexpected error occurred",
                errors=[str(e)]
            )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])  # Allow public access for GET
def skill_detail(request, skill_id):
    """
    Get, update, or delete a specific skill.
    
    Endpoint: GET /api/skills/<id>/ - Get skill details (public)
    Endpoint: PUT /api/skills/<id>/ - Update skill (requires auth)
    Endpoint: DELETE /api/skills/<id>/ - Delete skill (requires auth)
    """
    try:
        skill = get_object_or_404(Skill, id=skill_id)
        
        if request.method == 'GET':
            serializer = SkillSerializer(skill)
            return create_api_response(
                ResponseStatus.SUCCESS,
                "Skill details retrieved successfully",
                data=serializer.data
            )
        
        # For PUT and DELETE, require authentication
        if not request.user.is_authenticated:
            return create_api_response(
                ResponseStatus.ERROR,
                "Authentication required for this operation",
                errors=["Please log in to modify skills"]
            )
        
        # Check if user owns this skill for modifications
        if skill.user != request.user:
            return create_api_response(
                ResponseStatus.ERROR,
                "You are not authorized to modify this skill",
                errors=["Unauthorized access"]
            )
        
        if request.method == 'PUT':
            serializer = SkillSerializer(skill, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return create_api_response(
                    ResponseStatus.SUCCESS,
                    "Skill updated successfully",
                    data=serializer.data
                )
            else:
                return create_api_response(
                    ResponseStatus.ERROR,
                    "Validation error",
                    errors=serializer.errors
                )
        
        elif request.method == 'DELETE':
            skill.delete()
            return create_api_response(
                ResponseStatus.SUCCESS,
                "Skill deleted successfully"
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
    Get user notifications.
    
    Endpoint: GET /api/notifications/
    """
    try:
        # Get notifications for the user
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
        
        # Check if user is authorized to view this swap
        if swap_request.sender != request.user and swap_request.receiver != request.user:
            return create_api_response(
                ResponseStatus.ERROR,
                "You are not authorized to view this swap",
                errors=["Unauthorized access"]
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