"""
Configurações centrais do projeto Django Edge Monitor API.

Este arquivo define:
- Configurações de ambiente
- Aplicações instaladas
- Banco de dados
- Autenticação JWT
- Swagger / OpenAPI
- Arquivos estáticos e mídia
"""
from datetime import timedelta
import os
from dotenv import load_dotenv
from decouple import config, Csv
from pathlib import Path


# PATHS DO PROJETO

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis de ambiente a partir do arquivo .env
load_dotenv(BASE_DIR / '.env')


# CONFIGURAÇÕES DE SEGURANÇA

# Chave secreta da aplicação
SECRET_KEY = config('SECRET_KEY')

# Ativa modo debug
DEBUG = config('DEBUG', default=True, cast=bool)

# Hosts permitidos para acesso à aplicação
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# APLICAÇÕES INSTALADAS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Framework REST
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    
    # Documentação / Swagger
    'drf_spectacular',
    
    # Apps do projeto
    'core',
    'users',
    'monitoring',
    'dashboard',
]


# MIDDLEWARES

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# CONFIGURAÇÕES DE URL E TEMPLATES

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# BANCO DE DADOS

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# VALIDAÇÃO DE SENHAS

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


# INTERNACIONALIZAÇÃO

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# ARQUIVOS ESTÁTICOS E MÍDIA

STATIC_URL = 'static/'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# CONFIGURAÇÕES PADRÃO DO DJANGO

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CONFIGURAÇÕES DO SWAGGER / OPENAPI

SPECTACULAR_SETTINGS = {
    "TITLE": "Edge Monitor API",
    "DESCRIPTION": "API para monitoramento de risco químico e dashboard",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}


# CONFIGURAÇÕES DO DJANGO REST FRAMEWORK

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# CONFIGURAÇÕES JWT

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

