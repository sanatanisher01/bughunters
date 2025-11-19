#!/usr/bin/env python
"""
Production Email Test for BugHunter
Test email functionality on live production server
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

def test_production_email():
    """Test email configuration on production"""
    
    print("=" * 60)
    print("🔍 BugHunter Production Email Test")
    print("=" * 60)
    
    # Check Django settings
    print(f"DEBUG: {settings.DEBUG}")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'NOT SET')}")
    print(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'NOT SET')}")
    print(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'NOT SET')}")
    print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'NOT SET')}")
    print(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'NOT SET')}")
    print()
    
    # Validate configuration
    required_settings = ['EMAIL_HOST', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD']
    missing_settings = []
    
    for setting in required_settings:
        if not getattr(settings, setting, None):
            missing_settings.append(setting)
    
    if missing_settings:
        print("❌ Missing email configuration:")
        for setting in missing_settings:
            print(f"   - {setting}")
        return False
    
    print("✅ Email configuration complete")
    print()
    
    # Get test email
    test_email = input("Enter test email address: ").strip()
    if not test_email:
        print("❌ No email address provided")
        return False
    
    # Test 1: Basic Django send_mail
    print("📧 Test 1: Basic Django send_mail...")
    try:
        result = send_mail(
            subject="BugHunter Production Test - Basic",
            message="""
Hello!

This is a basic email test from BugHunter production server.

If you received this email, basic Django email functionality is working.

Test Details:
- Server: Production
- Method: Django send_mail
- Time: Now

Best regards,
BugHunter Team
            """.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False
        )
        
        if result == 1:
            print("✅ Basic email test PASSED")
        else:
            print("❌ Basic email test FAILED - No emails sent")
            return False
            
    except Exception as e:
        print(f"❌ Basic email test FAILED: {e}")
        return False
    
    # Test 2: EmailService verification email
    print("📧 Test 2: EmailService verification email...")
    try:
        # Create a mock user object
        class MockUser:
            def __init__(self, email, name):
                self.email = email
                self.name = name
                self.username = email.split('@')[0]
        
        mock_user = MockUser(test_email, "Test User")
        verification_url = "https://bughunter-p0cx.onrender.com/verify/?token=test123"
        
        result = EmailService.send_verification_email(mock_user, verification_url)
        
        if result:
            print("✅ EmailService verification test PASSED")
        else:
            print("❌ EmailService verification test FAILED")
            return False
            
    except Exception as e:
        print(f"❌ EmailService verification test FAILED: {e}")
        return False
    
    # Test 3: SMTP Connection Test
    print("📧 Test 3: Direct SMTP connection...")
    try:
        import smtplib
        
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.quit()
        
        print("✅ SMTP connection test PASSED")
        
    except Exception as e:
        print(f"❌ SMTP connection test FAILED: {e}")
        return False
    
    print()
    print("=" * 60)
    print("🎉 ALL EMAIL TESTS PASSED!")
    print("=" * 60)
    print("✅ Production email system is working correctly")
    print("✅ Users should receive verification emails")
    print("✅ Analysis notification emails should work")
    print()
    print("Check your inbox for test emails!")
    
    return True

def quick_test():
    """Quick email test without user input"""
    try:
        # Test basic configuration
        required_settings = ['EMAIL_HOST', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD']
        for setting in required_settings:
            if not getattr(settings, setting, None):
                print(f"❌ Missing {setting}")
                return False
        
        # Test SMTP connection
        import smtplib
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.quit()
        
        print("✅ Email configuration and SMTP connection OK")
        return True
        
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_test()
    else:
        test_production_email()