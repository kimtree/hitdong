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

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
