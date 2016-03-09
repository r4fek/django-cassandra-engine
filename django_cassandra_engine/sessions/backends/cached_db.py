from django.contrib.sessions.backends.cached_db import (
    SessionStore as CachedStore
)

from .db import SessionStore as DBStore


KEY_PREFIX = "dce.sessions.cached_db"


class SessionStore(DBStore, CachedStore):
    """
    Implements cached, cassandra backed sessions.
    """
    cache_key_prefix = KEY_PREFIX
