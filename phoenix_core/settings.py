from dotenv import load_dotenv
load_dotenv() 
from pathlib import Path
import os

# 1. Mipangilio ya Njia (Paths)
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Usalama (Security) - Hii ni key ya majaribio ya local
SECRET_KEY =  os.environ.get('DJANGO_SECRET_KEY')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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

# 8. Mipangilio ya Database (MAMP MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'online_ticket_booking',  # Jina la database utakayotengeneza phpMyAdmin
        'USER': 'root',
        'PASSWORD': 'root',                # Password ya MAMP kwenye Mac ni 'root'
        'HOST': '127.0.0.1',
        'PORT': '8889',                    # Port ya MySQL ya MAMP kwenye Mac
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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}