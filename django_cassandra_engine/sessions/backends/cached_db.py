from django.contrib.sessions.backends.cached_db import (
    SessionStore as CachedStore
)
from django.contrib.sessions.backends import cached_db

from django_cassandra_engine.sessions.backends.db import (
    SessionStore as DBStore
)

# monkey patch for Django versions older than 1.9
from django_cassandra_engine.sessions.models import Session as CassandraSession
cached_db.Session = CassandraSession

KEY_PREFIX = "dce.sessions.cached_db"


class SessionStore(DBStore, CachedStore):
    """
    Implements cached, cassandra backed sessions.
    """
    cache_key_prefix = KEY_PREFIX
