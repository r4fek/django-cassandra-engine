from cassandra.policies import RoundRobinPolicy

from .base import *

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
                "lazy_connect": True,
                "consistency": ConsistencyLevel.ALL,
                "load_balancing_policy": RoundRobinPolicy(),
            },
            "session": {"default_timeout": 15},
        },
    },
    "other": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    },
}

INSTALLED_APPS = BASE_APPS + ["app", "sessionsapp", "common", "model_meta"]
