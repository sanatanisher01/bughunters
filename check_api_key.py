#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bughunter_site.settings')
django.setup()

from django.conf import settings

print("Current Gemini API Key:")
print(f"Key: {settings.GEMINI_API_KEY}")
print(f"Length: {len(settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else 0}")
print(f"Starts with: {settings.GEMINI_API_KEY[:20] if settings.GEMINI_API_KEY else 'None'}...")