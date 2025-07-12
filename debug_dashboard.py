#!/usr/bin/env python
"""
Debug script for dashboard endpoint
"""

import os
import sys
import django
import requests
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill_swap_platform.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Skill, SwapRequest
from api.constants import SwapStatus

def test_dashboard():
    """Test the dashboard endpoint."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Dashboard Endpoint...")
    print(f"Base URL: {base_url}")
    print("-" * 50)
    
    # Step 1: Register a test user
    print("1. Registering test user...")
    register_data = {
        "email": "dashboard_test@example.com",
        "password": "testpass123",
        "first_name": "Dashboard",
        "last_name": "Test"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/register/", json=register_data)
        print(f"   Registration status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Registration successful: {result.get('status')}")
            
            if result.get('status') == 'success':
                token = result['data']['token']
                user_id = result['data']['user']['id']
                print(f"   User ID: {user_id}")
                print(f"   Token: {token[:20]}...")
                
                # Step 2: Test dashboard with token
                print("\n2. Testing dashboard endpoint...")
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
                
                dashboard_response = requests.get(f"{base_url}/api/dashboard/stats/", headers=headers)
                print(f"   Dashboard status: {dashboard_response.status_code}")
                print(f"   Dashboard response: {dashboard_response.text}")
                
                # Step 3: Check database state
                print("\n3. Checking database state...")
                try:
                    user = User.objects.get(id=user_id)
                    skills_count = Skill.objects.filter(user=user).count()
                    swaps_count = SwapRequest.objects.filter(sender=user).count()
                    
                    print(f"   User exists: {user.username}")
                    print(f"   Skills count: {skills_count}")
                    print(f"   Swaps count: {swaps_count}")
                    
                    # Check SwapRequest model
                    print(f"   SwapRequest model fields: {[f.name for f in SwapRequest._meta.fields]}")
                    
                except Exception as e:
                    print(f"   Database check error: {e}")
                
            else:
                print(f"   Registration failed: {result}")
        else:
            print(f"   Registration failed with status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Dashboard test completed!")
    return True

if __name__ == "__main__":
    test_dashboard() 