from base import *
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hitdong',
        'USER': 'hitdong',
        'PASSWORD': 'hitdong',
        'HOST': 'db.kimtree.net',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },

    }
}
