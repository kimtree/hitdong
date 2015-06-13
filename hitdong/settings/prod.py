from base import *
DEBUG = False

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

STATIC_ROOT = '/home/hitdong/staticfiles'
