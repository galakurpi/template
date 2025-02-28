from pathlib import Path
import os
import logging
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', "set_env_var")
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS.extend(['*.ngrok-free.app', '10.0.2.2', 'localhost'])

CELERY_BROKER_URL = os.environ.get('REDIS_HOST', 'redis://redis:6379')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_HOST', 'redis://redis:6379')

LOGIN_REDIRECT_URL = '/prototype'
LOGOUT_REDIRECT_URL = '/login'
LOGIN_URL = '/api/login/'

MIME_TYPES = {
    'webm': 'video/webm',
    'mp4': 'video/mp4',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('POSTGRES_HOST', 'database'),
        'NAME': os.environ.get('POSTGRES_DB', 'devdatabase'),
        'USER': os.environ.get('POSTGRES_USER', 'desa'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'desa'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'corsheaders',
    'api',
    'front',
    'trai',
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'front.middleware.CsrfExemptMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'front.middleware.GlobalHeaders',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # React Native development server
    "http://10.0.2.2:8000",      # Android emulator
    "http://localhost:8000",      # Local development
    "https://coaches.yekar.es",   # Production
    "http://coaches.yekar.es",    # Production (if needed)
    "https://yekar.es",          # Main domain
    "http://yekar.es",           # Main domain (if needed)
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# CSRF settings
CSRF_USE_SESSIONS = True  # More secure to store in session
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookie
CSRF_COOKIE_SECURE = not DEBUG  # True in production, False in development
CSRF_COOKIE_SAMESITE = 'Lax'  # Provides some XSS protection

CSRF_TRUSTED_ORIGINS = [
    'http://10.0.2.2:8000',      # Android emulator
    'http://localhost:8000',      # Local development
    'https://coaches.yekar.es',   # Production
    'http://coaches.yekar.es',    # Production (if needed)
    'https://yekar.es',          # Main domain
    'http://yekar.es',           # Main domain (if needed)
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'api': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'front': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

ROOT_URLCONF = 'trai.urls'

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

LOGGING_LEVEL = os.environ.get('DJANGO_LOG_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)8s][%(name)16.16s]@[%(lineno)5s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
        'propagate': False,
    },
    'loggers': {
        'django.server': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'api': {
            'level': LOGGING_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'front': {
            'level': LOGGING_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

WSGI_APPLICATION = 'trai.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/debug/media/'

MEDIA_ROOT = '/vol/web/media'
STATIC_ROOT = '/vol/web/static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'staticfiles'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': True,
    'JSON_EDITOR': True,
    'DISPLAY_OPERATION_ID': False,
    'PERSIST_AUTH': True,
    'DEEP_LINKING': True,
    'DOC_EXPANSION': 'none',
    'DEFAULT_MODEL_RENDERING': 'example',
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch',
    ],
    'VALIDATOR_URL': None,
}

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # Token auth 
        'rest_framework.authentication.SessionAuthentication',  # Session auth for web
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Require authentication by default
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1'],
}

print("="*50)
print("DEBUGGING ENV VARIABLES:")
print(f"DEBUG setting = {DEBUG}")
print(f"All environment variables:")
for key, value in os.environ.items():
    print(f"{key}: {value[:5]}..." if value else f"{key}: {value}")
print("="*50)

APPSTORE_SECRET = os.environ.get('APPSTORE_SHARED_SECRET')
# Only enforce APPSTORE_SECRET in production runtime
if not APPSTORE_SECRET and not DEBUG:
    # Check if we're in a build/collect static context
    import sys
    is_build_command = any(cmd in sys.argv for cmd in ['collectstatic', 'migrate', 'makemigrations'])
    print(f"is_build_command: {is_build_command}")
    if not is_build_command:
        print(f"CRITICAL ERROR: APPSTORE_SHARED_SECRET not set in production runtime")
        raise ValueError("APPSTORE_SHARED_SECRET must be set in production environment")
    else:
        print("Notice: APPSTORE_SHARED_SECRET not set, but ignoring for build/migration commands")