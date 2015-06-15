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

CACHES = {
    'default': {
        'BACKEND': 'django_elasticache.memcached.ElastiCache',
        'LOCATION': 'hitdongcache.guudi7.cfg.apne1.cache.amazonaws.com:11211',
    }
}

STATIC_ROOT = '/home/hitdong/staticfiles'
