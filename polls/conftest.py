import pytest
import os
import django
from django.conf import settings

# Set up Django settings for tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup() 