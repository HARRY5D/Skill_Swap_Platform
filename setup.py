#!/usr/bin/env python
"""
Setup script for the Skill Swap Platform.
This script automates the initial setup process.
"""

import os
import sys
import subprocess
import platform


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def create_virtual_environment():
    """Create a virtual environment."""
    if os.path.exists('venv'):
        print("✅ Virtual environment already exists")
        return True
    
    return run_command("python -m venv venv", "Creating virtual environment")


def activate_virtual_environment():
    """Activate the virtual environment."""
    if platform.system() == "Windows":
        activate_script = "venv\\Scripts\\activate"
    else:
        activate_script = "venv/bin/activate"
    
    if os.path.exists(activate_script):
        print("✅ Virtual environment is ready")
        return True
    else:
        print("❌ Virtual environment not found")
        return False


def install_dependencies():
    """Install Python dependencies."""
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")


def run_django_migrations():
    """Run Django migrations."""
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    commands = [
        (f"{python_cmd} manage.py makemigrations", "Creating migrations"),
        (f"{python_cmd} manage.py migrate", "Running migrations"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def load_sample_data():
    """Load sample data for testing."""
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} load_sample_data.py", "Loading sample data")


def create_superuser():
    """Create a superuser account."""
    print("\n👤 Creating superuser account...")
    print("Please enter the following details:")
    
    username = input("Username (default: admin): ").strip() or "admin"
    email = input("Email (default: admin@example.com): ").strip() or "admin@example.com"
    password = input("Password (default: admin123): ").strip() or "admin123"
    
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    # Create superuser using Django management command
    command = f"{python_cmd} manage.py shell -c \"from django.contrib.auth.models import User; User.objects.create_superuser('{username}', '{email}', '{password}')\""
    
    return run_command(command, "Creating superuser")


def run_tests():
    """Run the workflow tests."""
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} test_workflow.py", "Running workflow tests")


def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("1. Start the development server:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\python manage.py runserver")
    else:
        print("   venv/bin/python manage.py runserver")
    
    print("\n2. Access the application:")
    print("   - Admin interface: http://localhost:8000/admin/")
    print("   - API endpoints: http://localhost:8000/api/")
    
    print("\n3. Sample user credentials:")
    print("   - Username: alice_dev, Password: testpass123")
    print("   - Username: bob_designer, Password: testpass123")
    print("   - Username: carol_data, Password: testpass123")
    
    print("\n4. API Documentation:")
    print("   - See README.md for detailed API documentation")
    print("   - Test endpoints using tools like Postman or curl")
    
    print("\n5. Development:")
    print("   - Run tests: python test_workflow.py")
    print("   - Load more data: python load_sample_data.py")
    
    print("\n" + "=" * 60)
    print("Happy coding! 🚀")
    print("=" * 60)


def main():
    """Main setup function."""
    print("🏗️  SKILL SWAP PLATFORM - SETUP")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Activate virtual environment
    if not activate_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Run migrations
    if not run_django_migrations():
        sys.exit(1)
    
    # Load sample data
    if not load_sample_data():
        print("⚠️  Sample data loading failed, but setup can continue")
    
    # Create superuser
    if not create_superuser():
        print("⚠️  Superuser creation failed, but setup can continue")
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but setup can continue")
    
    # Print next steps
    print_next_steps()


if __name__ == '__main__':
    main() 