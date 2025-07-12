#!/usr/bin/env python
"""
Sample data loader for the Skill Swap Platform.
This script populates the database with sample users, skills, and profiles
for testing and demonstration purposes.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill_swap_platform.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Skill, Profile
from api.constants import Availability, ProfileVisibility


def create_sample_skills():
    """Create sample skills for the platform."""
    skills_data = [
        {
            'name': 'Python Programming',
            'description': 'Python programming language and frameworks',
            'category': 'Programming'
        },
        {
            'name': 'JavaScript',
            'description': 'JavaScript programming and web development',
            'category': 'Programming'
        },
        {
            'name': 'React.js',
            'description': 'React.js frontend framework',
            'category': 'Web Development'
        },
        {
            'name': 'Django',
            'description': 'Django web framework for Python',
            'category': 'Web Development'
        },
        {
            'name': 'Data Analysis',
            'description': 'Data analysis and visualization',
            'category': 'Data Science'
        },
        {
            'name': 'Machine Learning',
            'description': 'Machine learning algorithms and models',
            'category': 'Data Science'
        },
        {
            'name': 'Graphic Design',
            'description': 'Graphic design and visual arts',
            'category': 'Design'
        },
        {
            'name': 'UI/UX Design',
            'description': 'User interface and user experience design',
            'category': 'Design'
        },
        {
            'name': 'Digital Marketing',
            'description': 'Digital marketing strategies and tools',
            'category': 'Marketing'
        },
        {
            'name': 'Content Writing',
            'description': 'Content writing and copywriting',
            'category': 'Writing'
        },
        {
            'name': 'Photography',
            'description': 'Photography and photo editing',
            'category': 'Arts'
        },
        {
            'name': 'Cooking',
            'description': 'Cooking and culinary skills',
            'category': 'Lifestyle'
        },
        {
            'name': 'Guitar',
            'description': 'Guitar playing and music',
            'category': 'Music'
        },
        {
            'name': 'Spanish',
            'description': 'Spanish language learning',
            'category': 'Language'
        },
        {
            'name': 'French',
            'description': 'French language learning',
            'category': 'Language'
        }
    ]
    
    created_skills = []
    for skill_data in skills_data:
        skill, created = Skill.objects.get_or_create(
            name=skill_data['name'],
            defaults=skill_data
        )
        created_skills.append(skill)
        if created:
            print(f"Created skill: {skill.name}")
        else:
            print(f"Skill already exists: {skill.name}")
    
    return created_skills


def create_sample_users():
    """Create sample users with profiles."""
    users_data = [
        {
            'username': 'alice_dev',
            'email': 'alice@example.com',
            'first_name': 'Alice',
            'last_name': 'Developer',
            'password': 'testpass123',
            'profile': {
                'bio': 'Full-stack developer passionate about Python and React',
                'location': 'New York, NY',
                'phone': '+1-555-0101',
                'availability': Availability.WEEKENDS,
                'is_public': True,
                'visibility': ProfileVisibility.PUBLIC,
                'skills_offered': ['Python Programming', 'Django', 'React.js'],
                'skills_wanted': ['Machine Learning', 'Data Analysis']
            }
        },
        {
            'username': 'bob_designer',
            'email': 'bob@example.com',
            'first_name': 'Bob',
            'last_name': 'Designer',
            'password': 'testpass123',
            'profile': {
                'bio': 'Creative designer specializing in UI/UX and graphic design',
                'location': 'San Francisco, CA',
                'phone': '+1-555-0102',
                'availability': Availability.EVENINGS,
                'is_public': True,
                'visibility': ProfileVisibility.PUBLIC,
                'skills_offered': ['Graphic Design', 'UI/UX Design'],
                'skills_wanted': ['JavaScript', 'React.js']
            }
        },
        {
            'username': 'carol_data',
            'email': 'carol@example.com',
            'first_name': 'Carol',
            'last_name': 'Data Scientist',
            'password': 'testpass123',
            'profile': {
                'bio': 'Data scientist with expertise in ML and analytics',
                'location': 'Boston, MA',
                'phone': '+1-555-0103',
                'availability': Availability.WEEKDAYS,
                'is_public': True,
                'visibility': ProfileVisibility.PUBLIC,
                'skills_offered': ['Data Analysis', 'Machine Learning', 'Python Programming'],
                'skills_wanted': ['Graphic Design', 'Digital Marketing']
            }
        },
        {
            'username': 'david_marketer',
            'email': 'david@example.com',
            'first_name': 'David',
            'last_name': 'Marketer',
            'password': 'testpass123',
            'profile': {
                'bio': 'Digital marketing specialist with content writing skills',
                'location': 'Chicago, IL',
                'phone': '+1-555-0104',
                'availability': Availability.ALL_DAY,
                'is_public': True,
                'visibility': ProfileVisibility.PUBLIC,
                'skills_offered': ['Digital Marketing', 'Content Writing'],
                'skills_wanted': ['Data Analysis', 'Python Programming']
            }
        },
        {
            'username': 'emma_artist',
            'email': 'emma@example.com',
            'first_name': 'Emma',
            'last_name': 'Artist',
            'password': 'testpass123',
            'profile': {
                'bio': 'Artist and photographer with creative skills',
                'location': 'Los Angeles, CA',
                'phone': '+1-555-0105',
                'availability': Availability.WEEKENDS,
                'is_public': True,
                'visibility': ProfileVisibility.PUBLIC,
                'skills_offered': ['Photography', 'Graphic Design'],
                'skills_wanted': ['Cooking', 'Guitar']
            }
        },
        {
            'username': 'frank_chef',
            'email': 'frank@example.com',
            'first_name': 'Frank',
            'last_name': 'Chef',
            'password': 'testpass123',
            'profile': {
                'bio': 'Professional chef with culinary expertise',
                'location': 'Miami, FL',
                'phone': '+1-555-0106',
                'availability': Availability.EVENINGS,
                'is_public': True,
                'visibility': ProfileVisibility.PUBLIC,
                'skills_offered': ['Cooking'],
                'skills_wanted': ['Photography', 'Spanish']
            }
        },
        {
            'username': 'grace_musician',
            'email': 'grace@example.com',
            'first_name': 'Grace',
            'last_name': 'Musician',
            'password': 'testpass123',
            'profile': {
                'bio': 'Musician and guitar instructor',
                'location': 'Nashville, TN',
                'phone': '+1-555-0107',
                'availability': Availability.WEEKENDS,
                'is_public': True,
                'visibility': ProfileVisibility.PUBLIC,
                'skills_offered': ['Guitar'],
                'skills_wanted': ['French', 'Content Writing']
            }
        },
        {
            'username': 'henry_writer',
            'email': 'henry@example.com',
            'first_name': 'Henry',
            'last_name': 'Writer',
            'password': 'testpass123',
            'profile': {
                'bio': 'Content writer and language enthusiast',
                'location': 'Seattle, WA',
                'phone': '+1-555-0108',
                'availability': Availability.MORNINGS,
                'is_public': True,
                'visibility': ProfileVisibility.PUBLIC,
                'skills_offered': ['Content Writing', 'Spanish', 'French'],
                'skills_wanted': ['Digital Marketing', 'UI/UX Design']
            }
        }
    ]
    
    created_users = []
    for user_data in users_data:
        # Create user
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name']
            }
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"Created user: {user.username}")
        else:
            print(f"User already exists: {user.username}")
        
        # Create or update profile
        profile_data = user_data['profile']
        profile, profile_created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'bio': profile_data['bio'],
                'location': profile_data['location'],
                'phone': profile_data['phone'],
                'availability': profile_data['availability'],
                'is_public': profile_data['is_public'],
                'visibility': profile_data['visibility']
            }
        )
        
        if profile_created:
            print(f"Created profile for: {user.username}")
        else:
            # Update existing profile
            profile.bio = profile_data['bio']
            profile.location = profile_data['location']
            profile.phone = profile_data['phone']
            profile.availability = profile_data['availability']
            profile.is_public = profile_data['is_public']
            profile.visibility = profile_data['visibility']
            profile.save()
            print(f"Updated profile for: {user.username}")
        
        # Add skills
        for skill_name in profile_data['skills_offered']:
            try:
                skill = Skill.objects.get(name=skill_name)
                profile.skills_offered.add(skill)
            except Skill.DoesNotExist:
                print(f"Warning: Skill '{skill_name}' not found for {user.username}")
        
        for skill_name in profile_data['skills_wanted']:
            try:
                skill = Skill.objects.get(name=skill_name)
                profile.skills_wanted.add(skill)
            except Skill.DoesNotExist:
                print(f"Warning: Skill '{skill_name}' not found for {user.username}")
        
        created_users.append(user)
    
    return created_users


def main():
    """Main function to load sample data."""
    print("Loading sample data for Skill Swap Platform...")
    print("=" * 50)
    
    # Create skills
    print("\n1. Creating sample skills...")
    skills = create_sample_skills()
    print(f"Created {len(skills)} skills")
    
    # Create users and profiles
    print("\n2. Creating sample users and profiles...")
    users = create_sample_users()
    print(f"Created {len(users)} users with profiles")
    
    print("\n" + "=" * 50)
    print("Sample data loading completed!")
    print("\nYou can now:")
    print("- Run the development server: python manage.py runserver")
    print("- Access the admin interface: http://localhost:8000/admin/")
    print("- Test the API endpoints: http://localhost:8000/api/")
    print("\nSample user credentials:")
    print("Username: alice_dev, Password: testpass123")
    print("Username: bob_designer, Password: testpass123")
    print("Username: carol_data, Password: testpass123")
    print("(and more...)")


if __name__ == '__main__':
    main() 