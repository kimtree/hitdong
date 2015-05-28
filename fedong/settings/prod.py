from base import *
import dj_database_url

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
