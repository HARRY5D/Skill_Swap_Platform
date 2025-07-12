#!/usr/bin/env python
"""
Script to check skills in the database.
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

def check_skills():
    """Check skills in the database."""
    print("🔍 Checking Skills in Database...")
    print("=" * 50)
    
    # Check users
    users = User.objects.all()
    print(f"Total Users: {users.count()}")
    for user in users:
        print(f"  - User {user.id}: {user.email} ({user.first_name} {user.last_name})")
    
    print("\n" + "=" * 50)
    
    # Check skills
    skills = Skill.objects.all()
    print(f"Total Skills: {skills.count()}")
    
    if skills.count() == 0:
        print("  No skills found in database.")
        print("  This is normal for a new installation.")
        return
    
    for skill in skills:
        print(f"  - Skill {skill.id}: {skill.name}")
        print(f"    Description: {skill.description}")
        print(f"    Category: {skill.category}")
        print(f"    Difficulty: {skill.difficulty_level}")
        print(f"    User: {skill.user.email if skill.user else 'NO USER ASSOCIATED'}")
        print(f"    Created: {skill.created_at}")
        print()
    
    print("=" * 50)
    print("✅ Skills check completed!")

if __name__ == "__main__":
    check_skills() 