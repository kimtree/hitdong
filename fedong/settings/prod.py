import os
from base import *
DEBUG = False

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fedong',
        'USER': 'fedong',
        'PASSWORD': 'fedong',
        'HOST': 'db.kimtree.net',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },

    }
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPPER_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
UPPER_DIR2 = os.path.abspath(os.path.join(UPPER_DIR, os.pardir))
print BASE_DIR
print UPPER_DIR
print UPPER_DIR2

STATICFILES_DIRS = (UPPER_DIR2 + '/static',)
