from cassandra.policies import RoundRobinPolicy

from .base import *

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django_cassandra_engine",
        "NAME": "db",
        "USER": "cassandra",
        "PASSWORD": "cassandra",
        "TEST_NAME": "test_db",
        "HOST": CASSANDRA_HOST,
        "OPTIONS": {
            "replication": {
                "strategy_class": "SimpleStrategy",
                "replication_factor": 1,
            },
            "connection": {
                "retry_connect": True,
                "consistency": ConsistencyLevel.ALL,
                "load_balancing_policy": RoundRobinPolicy(),
            },
            "session": {"default_timeout": 15},
        },
    }
}

# If default and only engine is cassandra
INSTALLED_APPS = [
    "django_cassandra_engine",
    "django_cassandra_engine.sessions",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "app",
    "common",
    "model_meta",
]
