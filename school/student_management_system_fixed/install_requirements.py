#!/usr/bin/env python
"""
Installation script for Student Management System requirements
This script ensures all required packages are installed correctly
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    print("🚀 Installing Student Management System Requirements...")
    print("=" * 60)
    
    # List of required packages
    packages = [
        "Django==5.2.5",
        "Pillow>=10.0.0",
        "django-crispy-forms>=2.0",
        "crispy-bootstrap5>=2024.0",
        "reportlab>=4.0.0"
    ]
    
    failed_packages = []
    
    for package in packages:
        print(f"\n📦 Installing {package}...")
        if not install_package(package):
            failed_packages.append(package)
    
    print("\n" + "=" * 60)
    
    if failed_packages:
        print("❌ Some packages failed to install:")
        for package in failed_packages:
            print(f"   - {package}")
        print("\n💡 Try installing them manually using:")
        print("   pip install django-crispy-forms crispy-bootstrap5")
        return False
    else:
        print("✅ All packages installed successfully!")
        print("\n🎉 You can now run the Django server with:")
        print("   python manage.py runserver")
        return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

