﻿"""
Django settings for portemail project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g1zu9#)k1$m%fsopt^2c$03o3nz_g-%r%p$@c2nqt_&b0o&ogh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'emailmanage',    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portemail.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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


#Django-suit的一些界面设置(一种写法)

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': '陆海邮件管理系统',
    # 'HEADER_DATE_FORMAT': 'l, j. F Y',
    # 'HEADER_TIME_FORMAT': 'H:i',
    # forms
    #'SHOW_REQUIRED_ASTERISK': True,  # Default True
    #'CONFIRM_UNSAVED_CHANGES': True,  # Default True
    # menu
   # 'SEARCH_URL': '/admin/auth/user/',
    'MENU_ICONS': {
        'Emailmanage': 'icon-leaf',
       'auth': 'icon-lock',
    },
   # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    # 'MENU_EXCLUDE': ('auth.group',), 
    # misc
    'LIST_PER_PAGE': 10,
    'MENU': (
        'sites',
        {'app': 'emailmanage', 'label':u'邮件管理'},
        {'app': 'emailmanage', 'label':u'邮件匹配', 'models': ('emailmanage.Tonnage_Cargo', 'emailmanage.Tonnage_TCT')},
        {'label': 'Users', 'url': 'auth.user', 'icon':'icon-user'},
        {'label': 'Settings', 'icon':'icon-chevron-right', 'models': ('auth.user', 'auth.group')},
     ),
}


WSGI_APPLICATION = 'portemail.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'portemail',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:i:s'  # suit在admin里设置时间的一个小bug。需要把时间格式指定一下

DATE_FORMAT = 'Y-m-d'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = 'zhouxin314159@163.com'
EMAIL_HOST_PASSWORD = 'ZXphd4'
EMAIL_PORT = 25
EMAIL_USE_TLS = False

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER 


LOGIN_REDIRECT_URL = '/admin'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}