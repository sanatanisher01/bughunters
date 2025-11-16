from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid
from datetime import datetime, timedelta


class User(AbstractUser):
    """Extended user model with additional fields."""
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class VerificationToken(models.Model):
    """Email verification tokens."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        return not self.is_expired()


class BugHunterJob(models.Model):
    """Code analysis job tracking."""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    github_url = models.URLField(blank=True, null=True)
    zip_file = models.FileField(upload_to='uploads/', blank=True, null=True)
    code_input = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    summary = models.JSONField(blank=True, null=True)
    details = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def project_name(self):
        """Get a friendly project name."""
        if self.github_url:
            return self.github_url.split('/')[-1].replace('.git', '')
        elif self.zip_file:
            return self.zip_file.name.split('/')[-1]
        elif self.code_input:
            return f"Code Analysis ({self.language})"
        return "Unknown Project"
    
    def __str__(self):
        return f"{self.user.username} - {self.project_name} ({self.status})"