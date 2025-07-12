#!/usr/bin/env python
"""
Script to fix skills without user associations.
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

def fix_skills_users():
    """Fix skills that don't have user associations."""
    print("🔧 Fixing Skills User Associations...")
    print("=" * 50)
    
    # Get all skills without user associations
    orphaned_skills = Skill.objects.filter(user__isnull=True)
    print(f"Found {orphaned_skills.count()} skills without user associations")
    
    if orphaned_skills.count() == 0:
        print("✅ All skills already have user associations!")
        return
    
    # Get available users
    users = User.objects.all()
    if users.count() == 0:
        print("❌ No users found in database!")
        return
    
    print(f"Available users: {users.count()}")
    for user in users:
        print(f"  - {user.email}")
    
    # Group skills by name to handle duplicates
    skills_by_name = {}
    for skill in orphaned_skills:
        if skill.name not in skills_by_name:
            skills_by_name[skill.name] = []
        skills_by_name[skill.name].append(skill)
    
    print(f"\nSkills grouped by name:")
    for name, skills in skills_by_name.items():
        print(f"  - '{name}': {len(skills)} skills")
    
    # Distribute skills among users
    user_index = 0
    updated_count = 0
    deleted_count = 0
    
    for name, skills in skills_by_name.items():
        # Keep only the first skill with this name, delete duplicates
        if len(skills) > 1:
            print(f"\n  Found {len(skills)} skills named '{name}' - keeping first, deleting others")
            # Keep the first one, delete the rest
            for skill in skills[1:]:
                skill.delete()
                deleted_count += 1
                print(f"    - Deleted duplicate skill '{skill.name}' (ID: {skill.id})")
            skills = [skills[0]]  # Keep only the first one
        
        # Assign the remaining skill to a user
        skill = skills[0]
        user = users[user_index % len(users)]  # Distribute among users
        
        try:
            skill.user = user
            skill.save()
            updated_count += 1
            print(f"  - Assigned skill '{skill.name}' (ID: {skill.id}) to user {user.email}")
        except Exception as e:
            print(f"  - Error assigning skill '{skill.name}' to user {user.email}: {e}")
            # Try next user
            user_index += 1
            if user_index < len(users):
                user = users[user_index]
                try:
                    skill.user = user
                    skill.save()
                    updated_count += 1
                    print(f"    - Retried: Assigned skill '{skill.name}' (ID: {skill.id}) to user {user.email}")
                except Exception as e2:
                    print(f"    - Failed to assign skill '{skill.name}' to any user: {e2}")
        
        user_index += 1
    
    print(f"\n✅ Summary:")
    print(f"  - Updated {updated_count} skills with user associations")
    print(f"  - Deleted {deleted_count} duplicate skills")
    print("=" * 50)
    
    # Show final state
    print("\n📊 Final Skills State:")
    all_skills = Skill.objects.all()
    for skill in all_skills:
        user_email = skill.user.email if skill.user else "NO USER"
        print(f"  - Skill {skill.id}: {skill.name} -> User: {user_email}")

if __name__ == "__main__":
    fix_skills_users() 