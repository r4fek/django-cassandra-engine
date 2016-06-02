from .base import *

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_cassandra_engine',
        'NAME': 'db',
        'USER': 'user',
        'PASSWORD': 'pass',
        'TEST_NAME': 'test_db',
        'HOST': '127.0.0.1',
        'OPTIONS': {
            'replication': {
                'strategy_class': 'SimpleStrategy',
                'replication_factor': 1,
            },
            'connection': {
                'retry_connect': True,
                'consistency': ConsistencyLevel.ALL
            },
            'session': {
                'default_timeout': 15
            }
        }
    }
}

# If default and only engine is cassandra
INSTALLED_APPS = (
    'django_cassandra_engine',
    'django_cassandra_engine.sessions',
    'django.contrib.contenttypes',
    'django_nose',
    'app',
    'model_meta',
)
