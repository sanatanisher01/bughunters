from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from smtplib import SMTPException
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def _validate_email_config():
        """Validate email configuration"""
        if not all([settings.EMAIL_HOST, settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD]):
            logger.error("Email configuration incomplete")
            return False
        return True
    
    @staticmethod
    def send_verification_email(user, verification_url):
        """Send email verification email"""
        if not EmailService._validate_email_config():
            logger.error("Email configuration invalid, cannot send verification email")
            return False
            
        try:
            subject = "Verify Your Email - BugHunter"
            
            message = f"""
Hi {user.name or user.username},

Welcome to BugHunter! Please verify your email address by clicking the link below:

{verification_url}

If you didn't create this account, please ignore this email.

Best regards,
BugHunter Team
"""
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
            
            logger.info(f"Verification email sent to {user.email}")
            return True
            
        except SMTPException as e:
            logger.error(f"SMTP error sending verification email: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")
            return False
    
    @staticmethod
    def send_analysis_started(user, job):
        """Send email when analysis starts"""
        if not EmailService._validate_email_config():
            return False
            
        try:
            subject = f"🔍 Analysis Started - BugHunter"
            
            message = f"""
Hi {user.name or user.username},

Your code analysis has started! We'll notify you when it's complete.

Analysis Details:
- Project: {getattr(job, 'project_name', 'Code Analysis')}
- Started: {job.created_at.strftime('%Y-%m-%d %H:%M UTC')}

You can check the status in your dashboard.

Best regards,
BugHunter Team
"""
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
            
            logger.info(f"Analysis started email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send analysis started email: {e}")
            return False
    
    @staticmethod
    def send_analysis_completed(user, job, results_summary):
        """Send email when analysis completes successfully"""
        if not EmailService._validate_email_config():
            return False
            
        try:
            subject = f"✅ Analysis Complete - BugHunter"
            
            total_issues = results_summary.get('total_bugs', 0) + results_summary.get('total_vulnerabilities', 0)
            
            message = f"""
Hi {user.name or user.username},

Your code analysis is complete!

Results Summary:
- Files Analyzed: {results_summary.get('total_files', 0)}
- Issues Found: {total_issues}
- Bugs: {results_summary.get('total_bugs', 0)}
- Security Issues: {results_summary.get('total_vulnerabilities', 0)}
- Code Smells: {results_summary.get('total_smells', 0)}

View your detailed results in the dashboard.

Best regards,
BugHunter Team
"""
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
            
            logger.info(f"Analysis completed email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send analysis completed email: {e}")
            return False
    
    @staticmethod
    def send_analysis_failed(user, job, error_message):
        """Send email when analysis fails"""
        if not EmailService._validate_email_config():
            return False
            
        try:
            subject = f"❌ Analysis Failed - BugHunter"
            
            message = f"""
Hi {user.name or user.username},

Unfortunately, your code analysis failed to complete.

Error: {error_message}

Please try again or contact support if the issue persists.

Best regards,
BugHunter Team
"""
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
            
            logger.info(f"Analysis failed email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send analysis failed email: {e}")
            return False