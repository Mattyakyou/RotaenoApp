"""
Django settings for rotaeno project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4z$5l9*8o!2@xv%y^3@f@k3v2+!u7*7s@z@3@#1o6"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'main',
    "django_extensions",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'rotaeno.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'rotaeno.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST':'localhost',
#         'NAME': 'mattyaDatabase',
#         'USER': 'root',
#         'PASSWORD': 'gT4$Lm@qX9^NpWz7&Vb!F2KdY3',
#         'OPTIONS': {
#             'charset': 'utf8',
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         }
#     }
# }

# import dj_database_url

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('mattya_rotaeno_database'),
#         'USER': os.getenv('mattya_rotaeno_database_5ycw_user'),
#         'PASSWORD': os.getenv('xe9kqPTy4UyJTkme8Ti04dJTd1WLoqMG'),
#         'HOST': os.getenv('dpg-cv4ov3lds78s73e1qukg-a'),
#         'PORT': os.getenv('DB_PORT', '5432'),
#     }
# }

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  
        'NAME': 'railway',                          
        'USER': 'postgres',                         
        'PASSWORD': 'WbKelquuSufWfvjkNidduVKkJNxpCnna',  
        'HOST': 'trolley.proxy.rlwy.net',           
        'PORT': '22347',                            
    }
}





# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

CSRF_TRUSTED_ORIGINS = [
    'https://web-production-1218.up.railway.app',
    'https://*.amazanaws.com',
]











AUTH_USER_MODEL = 'main.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', 
]

# ログインページのURLを指定する（ログインしていないユーザーがアクセスするとリダイレクトされる）
LOGIN_URL = '/main/login/'  # ログイン画面へのURLを指定

# ログイン後にリダイレクトされるURLを指定
LOGIN_REDIRECT_URL = '/main/input_score/'  # ログイン後の遷移先を設定

# ログアウト後にリダイレクトされるページ
LOGOUT_REDIRECT_URL = '/main/login/'  # ホームページや任意のページにリダイレクト