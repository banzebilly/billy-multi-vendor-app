"""
Django settings for Billy_mult_vendor project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from django.contrib.messages import constants as messages
from decouple import config

# Base directory path - this is used to resolve paths to files and directories within the project.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Keep the secret key used in production secret!
# This should be kept out of version control, and we use `python-decouple` to manage sensitive settings.
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = True  # For development purposes, ensure to set to False in production.
ALLOWED_HOSTS = []  # In production, define your allowed hosts (e.g., ['yourdomain.com']).

# Application definition - List of apps used in your Django project
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Your custom apps for this project
    'account',
    'menu_app',
    'order_app',
    'vendor_app',
    'customer_app',
    'marketplace_app',
]

# Middleware definition - These middleware classes are used to process requests/responses.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration - Main URL configuration for the project.
ROOT_URLCONF = 'Billy_mult_vendor.urls'

# Templates configuration - Where Django looks for HTML templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],  # Add the directories containing your custom templates here.
        'APP_DIRS': True,  # This allows looking up templates within each app’s 'templates' folder.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #context  processors
                'account.context_processors.get_vendor',
                'marketplace_app.context_processors.get_cart_counter',
                'marketplace_app.context_processors.get_cart_amounts',
                'account.context_processors.get_user_profile',
            ],
        },
    },
]

# WSGI application - Used for deploying the project with WSGI servers like Gunicorn
WSGI_APPLICATION = 'Billy_mult_vendor.wsgi.application'


#telling django we re using custom model
AUTH_USER_MODEL = 'account.UserAccount'

# Database configuration - Uses PostgreSQL for the database connection.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),  # Use environment variables to store sensitive info.
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# Password validation - Defines password rules and validators to enforce strong security
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization settings - Language and timezone configuration for the application
LANGUAGE_CODE = 'en-us'  # Set the default language of the site
TIME_ZONE = 'UTC'  # Set your desired timezone
USE_I18N = True  # Enable internationalization
USE_TZ = True  # Enable timezone support

# Static files (CSS, JavaScript, Images) configuration
STATIC_URL = '/static/'  
# STATIC_ROOT is used in production for 'collectstatic' (Change 'static' to 'staticfiles')
STATIC_ROOT = BASE_DIR  / 'static'  

# STATICFILES_DIRS is used during development (Ensure this directory exists)
STATICFILES_DIRS = [
    BASE_DIR / 'Billy_mult_vendor/static', 

] 


# Media file configuration - Handles user-uploaded content such as images, videos, etc.
MEDIA_URL = '/media/'  # URL where media files are served
MEDIA_ROOT = BASE_DIR / 'media'  # Directory where media files are stored

# SMTP configuration - For sending emails using your configured SMTP server
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True  # Use TLS for secure email transmission


# Message tags - Customizing message tags for different message types
MESSAGE_TAGS = {
     messages.ERROR: 'danger',  # Display error messages with the 'danger' class in HTML
}

# Default primary key field type - This sets the default field type for primary keys in models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
