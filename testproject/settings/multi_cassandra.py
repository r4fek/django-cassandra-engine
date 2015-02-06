from .base import *

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'cassandra': {
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
                'lazy_connect': True,
                'retry_connect': True,
                'consistency': ConsistencyLevel.ALL
            },
            'session': {
                'default_timeout': 15
            }
        }
    },
    'cassandra2': {
        'ENGINE': 'django_cassandra_engine',
        'NAME': 'db2',
        'TEST_NAME': 'test_db2',
        'HOST': '127.0.0.1',
        'OPTIONS': {
            'replication': {
                'strategy_class': 'SimpleStrategy',
                'replication_factor': 1,
            },
            'connection': {
                'lazy_connect': True,
                'retry_connect': True,
                'consistency': ConsistencyLevel.ALL
            },
            'session': {
                'default_timeout': 15
            }
        }
    },
}

INSTALLED_APPS = (
    'django_cassandra_engine',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'multiapp',
)
