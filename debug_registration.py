#!/usr/bin/env python
"""
Debug script to test registration endpoint
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill_swap_platform.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from api.constants import ResponseStatus

def test_registration():
    """Test the registration process step by step."""
    print("Testing registration process...")
    
    try:
        # Test data
        email = "test@example.com"
        password = "testpass123"
        first_name = "Test"
        last_name = "User"
        
        print(f"1. Checking if user exists: {email}")
        if User.objects.filter(email=email).exists():
            print("   User already exists, deleting for test...")
            User.objects.filter(email=email).delete()
        
        print("2. Creating user...")
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        print(f"   User created successfully: {user.id}")
        
        print("3. Creating profile...")
        profile = Profile.objects.create(user=user)
        print(f"   Profile created successfully: {profile.id}")
        
        print("4. Generating JWT token...")
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        print(f"   Token generated successfully: {access_token[:20]}...")
        
        print("5. Creating user data...")
        user_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': profile.bio,
            'location': profile.location,
            'phone': profile.phone
        }
        print(f"   User data created: {user_data}")
        
        print("6. Creating API response...")
        response_data = {
            'status': ResponseStatus.SUCCESS,
            'message': "Registration successful",
            'data': {
                'token': access_token,
                'user': user_data
            }
        }
        print(f"   Response data created successfully")
        
        print("✅ All registration steps completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during registration: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_registration() 