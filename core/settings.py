from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default=False, cast=str)

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.Arquivo",
    "rest_framework",
    "storages",
    'corsheaders',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://0.0.0.0:5501',
    'http://127.0.0.1:5501',
    'http://0.0.0.0:8000',
    'http://127.0.0.1:8000',
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = "storages.storage.StaticS3Boto3Storage"

MEDIA_URL = f"{config('MINIO_ACCESS_URL')}/"

DEFAULT_FILE_STORAGE = "blogs.storage.S3MediaStorage"

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_ENDPOINT_URL = config("AWS_S3_URL")

MINIO_ENDPOINT = config("MINIO_STORAGE_ENDPOINT_URL", default=AWS_S3_ENDPOINT_URL)
MINIO_ACCESS_KEY = config("MINIO_ACCESS_KEY", default=AWS_ACCESS_KEY_ID)
MINIO_SECRET_KEY = config("MINIO_SECRET_KEY", default=AWS_SECRET_ACCESS_KEY)
MINIO_BUCKET_NAME = config("MINIO_STORAGE_BUCKET_NAME", default=AWS_STORAGE_BUCKET_NAME)

MINIO_ACCESS_URL = config("MINIO_ACCESS_URL")

STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
        'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
        'AWS_STORAGE_BUCKET_NAME': AWS_STORAGE_BUCKET_NAME,
        'AWS_S3_ENDPOINT_URL': AWS_S3_ENDPOINT_URL,
        'AWS_S3_OBJECT_PARAMETERS': {
            'CacheControl': 'max-age=86400',
        },
        'AWS_QUERYSTRING_AUTH': False,
        'AWS_S3_FILE_OVERWRITE': False,
        'AWS_DEFAULT_ACL': None,
        'AWS_S3_REGION_NAME': AWS_S3_REGION_NAME,
        'AWS_S3_CUSTOM_DOMAIN': f"{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL}",
    },
    'media': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
        'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
        'AWS_STORAGE_BUCKET_NAME': AWS_STORAGE_BUCKET_NAME,
        'AWS_S3_ENDPOINT_URL': AWS_S3_ENDPOINT_URL,
        'AWS_S3_OBJECT_PARAMETERS': {
            'CacheControl': 'max-age=86400',
        },
        'AWS_QUERYSTRING_AUTH': False,
        'AWS_S3_FILE_OVERWRITE': False,
        'AWS_DEFAULT_ACL': None,
        'AWS_S3_REGION_NAME': AWS_S3_REGION_NAME,
        'AWS_S3_CUSTOM_DOMAIN': f"{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL}",
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
        'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
        'AWS_STORAGE_BUCKET_NAME': AWS_STORAGE_BUCKET_NAME,
        'AWS_S3_ENDPOINT_URL': AWS_S3_ENDPOINT_URL,
        'AWS_S3_OBJECT_PARAMETERS': {
            'CacheControl': 'max-age=86400',
        },
        'AWS_QUERYSTRING_AUTH': False,
        'AWS_S3_FILE_OVERWRITE': False,
        'AWS_DEFAULT_ACL': None,
        'AWS_S3_REGION_NAME': AWS_S3_REGION_NAME,
        'AWS_S3_CUSTOM_DOMAIN': f"{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL}",
    }
}



DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
