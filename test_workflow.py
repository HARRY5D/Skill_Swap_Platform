#!/usr/bin/env python
"""
Test script for the Skill Swap Platform workflow.
This script demonstrates the core functionality and validates the implementation.
"""

import os
import sys
import django
import json
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill_swap_platform.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from api.models import Skill, Profile, SwapRequest
from api.services import (
    SwapValidationService, SwapWorkflowService, 
    ProfileService, SkillService
)
from api.constants import (
    SwapStatus, Availability, ProfileVisibility,
    ErrorMessages, SuccessMessages
)


class SkillSwapWorkflowTest:
    """Test class for the Skill Swap Platform workflow."""
    
    def __init__(self):
        self.client = Client()
        self.test_results = []
        
    def log_test(self, test_name, status, message, details=None):
        """Log test results."""
        result = {
            'test_name': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        self.test_results.append(result)
        print(f"[{status.upper()}] {test_name}: {message}")
        if details:
            print(f"  Details: {details}")
    
    def test_skill_creation(self):
        """Test skill creation and validation."""
        try:
            # Create a test skill
            skill = Skill.objects.create(
                name='Test Programming',
                description='Test programming skill',
                category='Programming'
            )
            
            # Validate skill was created
            assert skill.name == 'Test Programming'
            assert skill.category == 'Programming'
            
            self.log_test(
                'Skill Creation',
                'PASS',
                'Skill created successfully',
                {'skill_id': skill.id, 'name': skill.name}
            )
            
        except Exception as e:
            self.log_test(
                'Skill Creation',
                'FAIL',
                f'Skill creation failed: {str(e)}'
            )
    
    def test_profile_creation(self):
        """Test profile creation and validation."""
        try:
            # Create a test user
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )
            
            # Create a test skill
            skill = Skill.objects.create(
                name='Test Skill',
                description='Test skill description',
                category='Test'
            )
            
            # Create profile
            profile = Profile.objects.create(
                user=user,
                bio='Test bio',
                location='Test City',
                availability=Availability.WEEKENDS,
                is_public=True,
                visibility=ProfileVisibility.PUBLIC
            )
            
            # Add skill to profile
            profile.skills_offered.add(skill)
            
            # Validate profile
            assert profile.user == user
            assert profile.is_available_for_swap == True
            assert skill in profile.skills_offered.all()
            
            self.log_test(
                'Profile Creation',
                'PASS',
                'Profile created successfully',
                {'user_id': user.id, 'profile_id': profile.id}
            )
            
        except Exception as e:
            self.log_test(
                'Profile Creation',
                'FAIL',
                f'Profile creation failed: {str(e)}'
            )
    
    def test_swap_validation(self):
        """Test swap validation logic."""
        try:
            # Create test users
            user1 = User.objects.create_user('user1', 'user1@test.com', 'pass123')
            user2 = User.objects.create_user('user2', 'user2@test.com', 'pass123')
            
            # Create test skills
            skill1 = Skill.objects.create(name='Skill 1', category='Test')
            skill2 = Skill.objects.create(name='Skill 2', category='Test')
            
            # Create profiles
            profile1 = Profile.objects.create(
                user=user1,
                is_public=True,
                visibility=ProfileVisibility.PUBLIC
            )
            profile2 = Profile.objects.create(
                user=user2,
                is_public=True,
                visibility=ProfileVisibility.PUBLIC
            )
            
            # Add skills to profiles
            profile1.skills_offered.add(skill1)
            profile2.skills_offered.add(skill2)
            
            # Test valid swap creation
            swap = SwapWorkflowService.create_swap_request(
                sender=user1,
                receiver=user2,
                skill_offered=skill1,
                skill_requested=skill2,
                message='Test swap request'
            )
            
            assert swap.status == SwapStatus.PENDING
            assert swap.sender == user1
            assert swap.receiver == user2
            
            self.log_test(
                'Swap Validation',
                'PASS',
                'Swap validation passed',
                {'swap_id': swap.id, 'status': swap.status}
            )
            
        except Exception as e:
            self.log_test(
                'Swap Validation',
                'FAIL',
                f'Swap validation failed: {str(e)}'
            )
    
    def test_swap_self_validation(self):
        """Test validation that prevents swapping with oneself."""
        try:
            # Create test user and skill
            user = User.objects.create_user('selfuser', 'self@test.com', 'pass123')
            skill = Skill.objects.create(name='Self Skill', category='Test')
            
            profile = Profile.objects.create(
                user=user,
                is_public=True,
                visibility=ProfileVisibility.PUBLIC
            )
            profile.skills_offered.add(skill)
            
            # Try to create swap with self (should fail)
            try:
                SwapWorkflowService.create_swap_request(
                    sender=user,
                    receiver=user,
                    skill_offered=skill,
                    skill_requested=skill
                )
                self.log_test(
                    'Self Swap Prevention',
                    'FAIL',
                    'Should have prevented self-swap'
                )
            except Exception as e:
                if ErrorMessages.SWAP_TO_SELF in str(e):
                    self.log_test(
                        'Self Swap Prevention',
                        'PASS',
                        'Successfully prevented self-swap'
                    )
                else:
                    self.log_test(
                        'Self Swap Prevention',
                        'FAIL',
                        f'Unexpected error: {str(e)}'
                    )
                    
        except Exception as e:
            self.log_test(
                'Self Swap Prevention',
                'FAIL',
                f'Self swap test failed: {str(e)}'
            )
    
    def test_swap_status_transitions(self):
        """Test swap status transitions."""
        try:
            # Create test users and skills
            user1 = User.objects.create_user('trans1', 'trans1@test.com', 'pass123')
            user2 = User.objects.create_user('trans2', 'trans2@test.com', 'pass123')
            
            skill1 = Skill.objects.create(name='Trans Skill 1', category='Test')
            skill2 = Skill.objects.create(name='Trans Skill 2', category='Test')
            
            profile1 = Profile.objects.create(
                user=user1,
                is_public=True,
                visibility=ProfileVisibility.PUBLIC
            )
            profile2 = Profile.objects.create(
                user=user2,
                is_public=True,
                visibility=ProfileVisibility.PUBLIC
            )
            
            profile1.skills_offered.add(skill1)
            profile2.skills_offered.add(skill2)
            
            # Create swap request
            swap = SwapWorkflowService.create_swap_request(
                sender=user1,
                receiver=user2,
                skill_offered=skill1,
                skill_requested=skill2
            )
            
            # Test accept transition
            updated_swap = SwapWorkflowService.respond_to_swap(
                swap_request=swap,
                user=user2,
                new_status=SwapStatus.ACCEPTED
            )
            
            assert updated_swap.status == SwapStatus.ACCEPTED
            
            self.log_test(
                'Status Transitions',
                'PASS',
                'Swap status transitions work correctly',
                {'initial_status': SwapStatus.PENDING, 'final_status': SwapStatus.ACCEPTED}
            )
            
        except Exception as e:
            self.log_test(
                'Status Transitions',
                'FAIL',
                f'Status transition test failed: {str(e)}'
            )
    
    def test_profile_search(self):
        """Test profile search functionality."""
        try:
            # Create test users with different skills
            user1 = User.objects.create_user('search1', 'search1@test.com', 'pass123')
            user2 = User.objects.create_user('search2', 'search2@test.com', 'pass123')
            
            skill1 = Skill.objects.create(name='Search Skill 1', category='Test')
            skill2 = Skill.objects.create(name='Search Skill 2', category='Test')
            
            profile1 = Profile.objects.create(
                user=user1,
                location='New York',
                availability=Availability.WEEKENDS,
                is_public=True,
                visibility=ProfileVisibility.PUBLIC
            )
            profile2 = Profile.objects.create(
                user=user2,
                location='San Francisco',
                availability=Availability.EVENINGS,
                is_public=True,
                visibility=ProfileVisibility.PUBLIC
            )
            
            profile1.skills_offered.add(skill1)
            profile2.skills_offered.add(skill2)
            
            # Test search by skill
            profiles = ProfileService.search_profiles_by_skill('Search Skill 1')
            assert len(profiles) >= 1
            
            # Test get public profiles
            public_profiles = ProfileService.get_public_profiles()
            assert len(public_profiles) >= 2
            
            self.log_test(
                'Profile Search',
                'PASS',
                'Profile search functionality works',
                {'search_results': len(profiles), 'public_profiles': len(public_profiles)}
            )
            
        except Exception as e:
            self.log_test(
                'Profile Search',
                'FAIL',
                f'Profile search test failed: {str(e)}'
            )
    
    def test_api_endpoints(self):
        """Test API endpoints functionality."""
        try:
            # Create test user and authenticate
            user = User.objects.create_user('apitest', 'apitest@test.com', 'pass123')
            self.client.force_login(user)
            
            # Test skills endpoint
            response = self.client.get('/api/skills/')
            assert response.status_code == 200
            
            # Test profiles search endpoint
            response = self.client.get('/api/profiles/search/')
            assert response.status_code == 200
            
            self.log_test(
                'API Endpoints',
                'PASS',
                'API endpoints are accessible',
                {'skills_status': response.status_code}
            )
            
        except Exception as e:
            self.log_test(
                'API Endpoints',
                'FAIL',
                f'API endpoint test failed: {str(e)}'
            )
    
    def run_all_tests(self):
        """Run all tests and generate report."""
        print("=" * 60)
        print("SKILL SWAP PLATFORM - WORKFLOW TESTING")
        print("=" * 60)
        
        # Run all tests
        self.test_skill_creation()
        self.test_profile_creation()
        self.test_swap_validation()
        self.test_swap_self_validation()
        self.test_swap_status_transitions()
        self.test_profile_search()
        self.test_api_endpoints()
        
        # Generate summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['status'] == 'PASS')
        failed = sum(1 for result in self.test_results if result['status'] == 'FAIL')
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"- {result['test_name']}: {result['message']}")
        
        # Save results to file
        with open('test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"\nDetailed results saved to: test_results.json")
        
        return passed == total


def main():
    """Main function to run the workflow tests."""
    tester = SkillSwapWorkflowTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! The Skill Swap Platform is working correctly.")
    else:
        print("\n❌ SOME TESTS FAILED. Please check the implementation.")
    
    return success


if __name__ == '__main__':
    main() 