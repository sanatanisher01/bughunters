#!/usr/bin/env python
"""
Email Configuration Test Script for BugHunter
Run this script to test your email configuration before deployment.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bughunter_site.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from bughunter_site.accounts.email_service import EmailService

def test_email_configuration():
    """Test email configuration and send a test email"""
    
    print("Testing BugHunter Email Configuration")
    print("=" * 50)
    
    # Check configuration
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print()
    
    # Validate configuration
    if not all([settings.EMAIL_HOST, settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD]):
        print("Email configuration incomplete!")
        print("Missing required settings:")
        if not settings.EMAIL_HOST:
            print("  - EMAIL_HOST")
        if not settings.EMAIL_HOST_USER:
            print("  - EMAIL_HOST_USER")
        if not settings.EMAIL_HOST_PASSWORD:
            print("  - EMAIL_HOST_PASSWORD")
        return False
    
    print("Email configuration looks complete")
    
    # Test email sending
    test_email = input("Enter test email address: ").strip()
    if not test_email:
        print("No email address provided")
        return False
    
    try:
        print(f"Sending test email to {test_email}...")
        
        success = send_mail(
            subject="BugHunter Email Test",
            message="""
Hi there!

This is a test email from BugHunter to verify that email configuration is working correctly.

If you received this email, your email settings are configured properly!

Best regards,
BugHunter Team
            """.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False
        )
        
        if success:
            print("Test email sent successfully!")
            return True
        else:
            print("Failed to send test email")
            return False
            
    except Exception as e:
        print(f"Error sending test email: {e}")
        return False

def main():
    """Main function"""
    try:
        success = test_email_configuration()
        if success:
            print("\nEmail configuration test passed!")
            print("Your BugHunter application should be able to send emails.")
        else:
            print("\nEmail configuration test failed!")
            print("Please check your email settings in .env file.")
            
    except Exception as e:
        print(f"Error running email test: {e}")

if __name__ == "__main__":
    main()