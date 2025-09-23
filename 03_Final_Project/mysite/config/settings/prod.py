from .base import *



DEBUG = False
ALLOWED_HOSTS = ['13.209.106.188']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pybo',
        'USER': 'dbmasteruser',
        'PASSWORD': 'kkNY[:f8pZ%bFU(d]2!2]s7Gb>{AB#4g',
        'HOST': 'ls-08b690b662e41c3e713828df17c91339294fc316.cxgeogskomfe.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}