"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'missing-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / os.environ.get('LOG_FILE', 'debug.log'),
            'formatter': 'default',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Application definition
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_password_validators',  # Ensure this package is installed
    'axes',  # For rate-limiting authentication attempts
    'captcha',
    'sslserver',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',  # Rate-limiting middleware
    'mysite.middleware.LogErrorMiddleware',
]

# Secure headers
SECURE_HSTS_SECONDS = 31536000  # Enforce HSTS for 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = False  # Redirect HTTP to HTTPS
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME sniffing
SECURE_BROWSER_XSS_FILTER = True  # Enable XSS filter
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SESSION_COOKIE_SECURE = True  # Secure cookies with HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'polls.validators.CustomPasswordValidator',
    },
]

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_REDIRECT_URL = '/polls/'
LOGOUT_REDIRECT_URL = '/polls/'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# Security related
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True') == 'True'
SESSION_COOKIE_AGE = 1800  # 30 minutes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "polls/static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Axes settings for rate-limiting
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # Lockout time in hours
AXES_ONLY_USER_FAILURES = True

if 'test' in sys.argv:
    AXES_ENABLED = False

PASSWORD_HISTORY_COUNT = 5  # Prevent reuse of last 5 passwords

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# File permission configuration
log_file_path = BASE_DIR / 'debug.log'
if os.path.exists(log_file_path):
    try:
        os.chmod(log_file_path, 0o600)  # Set read/write for owner only
    except PermissionError:
        print("Warning: Could not change permissions for the log file.")
else:
    # Create the file if it doesn't exist
    with open(log_file_path, 'w'):
        pass
    os.chmod(log_file_path, 0o600)
