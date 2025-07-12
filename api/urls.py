"""
URL configuration for the API app.
"""

from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', views.login_view, name='login'),
    path('auth/register/', views.register_view, name='register'),
    path('auth/me/', views.me_view, name='me'),
    path('auth/profile/', views.profile_view, name='profile'),
    
    # Dashboard endpoints
    path('dashboard/stats/', views.dashboard_stats_view, name='dashboard_stats'),
    
    # Skill-related endpoints
    path('skills/', views.list_skills, name='list_skills'),
    path('skills/my-skills/', views.my_skills_view, name='my_skills'),
    
    # Swap-related endpoints
    path('swaps/', views.list_swaps, name='list_swaps'),
    path('swaps/create/', views.create_swap_request, name='create_swap'),
    path('swaps/pending/', views.get_pending_swaps, name='pending_swaps'),
    path('swaps/<int:swap_id>/', views.get_swap_details, name='swap_details'),
    path('swaps/<int:swap_id>/respond/', views.respond_to_swap, name='respond_swap'),
    
    # Profile-related endpoints
    path('profiles/search/', views.search_profiles, name='search_profiles'),
    
    # Notification endpoints (optional bonus feature)
    path('notifications/', views.get_notifications, name='notifications'),
] 