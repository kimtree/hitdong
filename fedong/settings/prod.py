from base import *
import dj_database_url

DEBUG = False

# Database
DATABASES = {
    'default': dj_database_url.config()
}
