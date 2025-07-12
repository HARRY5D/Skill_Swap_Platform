"""
URL configuration for the API app.
"""

from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Swap-related endpoints
    path('swaps/', views.list_swaps, name='list_swaps'),
    path('swaps/create/', views.create_swap_request, name='create_swap'),
    path('swaps/pending/', views.get_pending_swaps, name='pending_swaps'),
    path('swaps/<int:swap_id>/', views.get_swap_details, name='swap_details'),
    path('swaps/<int:swap_id>/respond/', views.respond_to_swap, name='respond_swap'),
    
    # Profile-related endpoints
    path('profiles/search/', views.search_profiles, name='search_profiles'),
    
    # Skill-related endpoints
    path('skills/', views.list_skills, name='list_skills'),
    
    # Notification endpoints (optional bonus feature)
    path('notifications/', views.get_notifications, name='notifications'),
] 