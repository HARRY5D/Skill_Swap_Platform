#!/usr/bin/env python
"""
Check new user's skills and authentication.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill_swap_platform.settings')
django.setup()

from api.models import Skill, User, Profile
from api.views import my_skills_view
from django.test import RequestFactory
from rest_framework.test import force_authenticate

def check_new_user_skills():
    """Check new user's skills and test the endpoint."""
    print("🔍 Checking New User's Skills...")
    print("=" * 50)
    
    # Get all users and their skills
    users = User.objects.all().order_by('-id')  # Most recent first
    print(f"📊 Total Users: {users.count()}")
    
    print("\n👥 All Users:")
    for user in users:
        skills_count = Skill.objects.filter(user=user).count()
        print(f"  - User {user.id}: {user.email} ({user.first_name} {user.last_name}) - {skills_count} skills")
    
    # Get the most recent user (your new account)
    if users.count() > 0:
        newest_user = users.first()
        print(f"\n🎯 Checking newest user: {newest_user.email} (ID: {newest_user.id})")
        
        # Check their skills
        user_skills = Skill.objects.filter(user=newest_user)
        print(f"  - Skills count: {user_skills.count()}")
        
        if user_skills.count() > 0:
            print("  - Skills found:")
            for skill in user_skills:
                print(f"    * {skill.name} (ID: {skill.id}) - {skill.category} - {skill.difficulty_level}")
        else:
            print("  - No skills found for this user")
        
        # Test the my-skills endpoint for this user
        print(f"\n🧪 Testing my-skills endpoint for {newest_user.email}...")
        try:
            factory = RequestFactory()
            request = factory.get('/api/skills/my-skills/')
            force_authenticate(request, user=newest_user)
            
            response = my_skills_view(request)
            print(f"  - Response status: {response.status_code}")
            print(f"  - Response data: {response.data}")
            
            if response.status_code == 200 and response.data.get('status') == 'success':
                skills_data = response.data.get('data', [])
                print(f"  - Skills returned by endpoint: {len(skills_data)}")
                for skill in skills_data:
                    print(f"    * {skill.get('name')} (ID: {skill.get('id')})")
            else:
                print(f"  - Error: {response.data.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error testing endpoint: {e}")
    
    print("\n" + "=" * 50)
    
    # Show all skills in the database
    print("📋 All Skills in Database:")
    all_skills = Skill.objects.all().order_by('-id')
    print(f"  - Total skills: {all_skills.count()}")
    
    for skill in all_skills:
        user_email = skill.user.email if skill.user else "NO USER"
        print(f"    - Skill {skill.id}: {skill.name} -> User: {user_email}")
    
    print("\n" + "=" * 50)
    print("✅ Check completed!")

if __name__ == "__main__":
    check_new_user_skills() 