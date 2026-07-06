from pathlib import Path
import os
import dj_database_url  # Hakikisha hii ipo kwa ajili ya Render database parsing

from dotenv import load_dotenv
load_dotenv() 

# 1. Mipangilio ya Njia (Paths)
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Usalama (Security)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-local-test-key-12345')

# Kagua kama tuko Render au Local
IS_RENDER = 'RENDER' in os.environ

if IS_RENDER:
    DEBUG = False
    ALLOWED_HOSTS = ['phonix-ticket-system.onrender.com']
else:
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

CSRF_TRUSTED_ORIGINS = ['https://phonix-ticket-system.onrender.com']

# 3. Usajili wa Application (Installed Apps)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # App yako ya Mfumo wa Tiketi
    'tickets',
]

# 4. Mifumo ya Kati (Middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',  # Imerekebishwa (isirudie)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 5. Mipangilio ya Faili Kuu la URL
ROOT_URLCONF = 'phoenix_core.urls'

# 6. Mipangilio ya Muonekano (Templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# 7. Mipangilio ya WSGI
WSGI_APPLICATION = 'phoenix_core.wsgi.application'

# 8. Mipangilio ya Database (MAMP Local vs Render Live)
if IS_RENDER:
    # Kama umeweka PostgreSQL au MySQL ya Render, itasoma hapa kiotomatiki
    if os.environ.get('DATABASE_URL'):
        DATABASES = {
            'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
        }
    else:
        # Kama hujaunganisha database kule Render, tunaiwekea SQLite ya muda ili isilete Error 500
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # MAMP MySQL yako ya kwenye Mac (Local)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'online_ticket_booking',  
            'USER': 'root',
            'PASSWORD': 'root',                
            'HOST': '127.0.0.1',
            'PORT': '8889',                    
        }
    }

# 9. Ukaguzi wa Password (Password Validation)
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

# 10. Lugha na Muda (Internationalization)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 11. Mafaili Tuli (Static Files - CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'