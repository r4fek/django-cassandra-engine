from datetime import timedelta
import string
import unittest
import django
from django.conf import settings
from django.core.cache import InvalidCacheBackendError
from django.test.utils import override_settings
from django.utils import timezone
from django.utils.encoding import force_str
from mock import Mock

from django_cassandra_engine.sessions.backends.cached_db import (
    SessionStore as CachedDatabaseSession,
)
from django_cassandra_engine.sessions.backends.db import (
    SessionStore as DatabaseSession,
)
from django_cassandra_engine.test import TestCase

try:
    from django.test.utils import ignore_warnings
except ImportError:
    ignore_warnings = Mock()


class SessionTestsMixin(object):
    # This does not inherit from TestCase to avoid any tests being run with this
    # class, which wouldn't work, and to allow different TestCase subclasses to
    # be used.

    backend = None  # subclasses must specify

    def setUp(self):
        self.session = self.backend()

    def tearDown(self):
        # NB: be careful to delete any sessions created; stale sessions fill up
        # the /tmp (with some backends) and eventually overwhelm it after lots
        # of runs (think buildbots)
        self.session.delete()

    def test_new_session(self):
        self.assertFalse(self.session.modified)
        self.assertFalse(self.session.accessed)

    def test_get_empty(self):
        self.assertEqual(self.session.get("cat"), None)

    def test_store(self):
        self.session["cat"] = "dog"
        self.assertTrue(self.session.modified)
        self.assertEqual(self.session.pop("cat"), "dog")

    def test_pop(self):
        self.session["some key"] = "exists"
        # Need to reset these to pretend we haven't accessed it:
        self.accessed = False
        self.modified = False

        self.assertEqual(self.session.pop("some key"), "exists")
        self.assertTrue(self.session.accessed)
        self.assertTrue(self.session.modified)
        self.assertEqual(self.session.get("some key"), None)

    def test_pop_default(self):
        self.assertEqual(
            self.session.pop("some key", "does not exist"), "does not exist"
        )
        self.assertTrue(self.session.accessed)
        self.assertFalse(self.session.modified)

    def test_setdefault(self):
        self.assertEqual(self.session.setdefault("foo", "bar"), "bar")
        self.assertEqual(self.session.setdefault("foo", "baz"), "bar")
        self.assertTrue(self.session.accessed)
        self.assertTrue(self.session.modified)

    def test_update(self):
        self.session.update({"update key": 1})
        self.assertTrue(self.session.accessed)
        self.assertTrue(self.session.modified)
        self.assertEqual(self.session.get("update key", None), 1)

    def test_has_key(self):
        self.session["some key"] = 1
        self.session.modified = False
        self.session.accessed = False
        self.assertIn("some key", self.session)
        self.assertTrue(self.session.accessed)
        self.assertFalse(self.session.modified)

    def test_values(self):
        self.assertEqual(list(self.session.values()), [])
        self.assertTrue(self.session.accessed)
        self.session["some key"] = 1
        self.assertEqual(list(self.session.values()), [1])

    def test_iterkeys(self):
        self.session["x"] = 1
        self.session.modified = False
        self.session.accessed = False
        i = self.session.keys()
        self.assertTrue(hasattr(i, "__iter__"))
        self.assertTrue(self.session.accessed)
        self.assertFalse(self.session.modified)
        self.assertEqual(list(i), ["x"])

    def test_itervalues(self):
        self.session["x"] = 1
        self.session.modified = False
        self.session.accessed = False
        i = self.session.values()
        self.assertTrue(hasattr(i, "__iter__"))
        self.assertTrue(self.session.accessed)
        self.assertFalse(self.session.modified)
        self.assertEqual(list(i), [1])

    def test_iteritems(self):
        self.session["x"] = 1
        self.session.modified = False
        self.session.accessed = False
        i = self.session.items()
        self.assertTrue(hasattr(i, "__iter__"))
        self.assertTrue(self.session.accessed)
        self.assertFalse(self.session.modified)
        self.assertEqual(list(i), [("x", 1)])

    def test_clear(self):
        self.session["x"] = 1
        self.session.modified = False
        self.session.accessed = False
        self.assertEqual(list(self.session.items()), [("x", 1)])
        self.session.clear()
        self.assertEqual(list(self.session.items()), [])
        self.assertTrue(self.session.accessed)
        self.assertTrue(self.session.modified)

    def test_save(self):
        if (
            hasattr(self.session, "_cache")
            and "DummyCache" in settings.CACHES[settings.SESSION_CACHE_ALIAS]["BACKEND"]
        ):
            raise unittest.SkipTest("Session saving tests require a real cache backend")
        self.session.save()
        self.assertTrue(self.session.exists(self.session.session_key))

    def test_delete(self):
        self.session.save()
        self.session.delete(self.session.session_key)
        self.assertFalse(self.session.exists(self.session.session_key))

    def test_flush(self):
        self.session["foo"] = "bar"
        self.session.save()
        prev_key = self.session.session_key
        self.session.flush()
        self.assertFalse(self.session.exists(prev_key))
        self.assertNotEqual(self.session.session_key, prev_key)
        self.assertIsNone(self.session.session_key)
        self.assertTrue(self.session.modified)
        self.assertTrue(self.session.accessed)

    def test_cycle(self):
        self.session["a"], self.session["b"] = "c", "d"
        self.session.save()
        prev_key = self.session.session_key
        prev_data = list(self.session.items())
        self.session.cycle_key()
        self.assertNotEqual(self.session.session_key, prev_key)
        self.assertEqual(list(self.session.items()), prev_data)

    def test_save_doesnt_clear_data(self):
        self.session["a"] = "b"
        self.session.save()
        self.assertEqual(self.session["a"], "b")

    def test_invalid_key(self):
        # Submitting an invalid session key (either by guessing, or if the db has
        # removed the key) results in a new key being generated.
        try:
            session = self.backend("1")
            try:
                session.save()
            except AttributeError:
                self.fail(
                    "The session object did not save properly. "
                    "Middleware may be saving cache items without namespaces."
                )
            self.assertNotEqual(session.session_key, "1")
            self.assertEqual(session.get("cat"), None)
            session.delete()
        finally:
            # Some backends leave a stale cache entry for the invalid
            # session key; make sure that entry is manually deleted
            session.delete("1")

    def test_session_key_valid_string_saved(self):
        """Strings of length 8 and up are accepted and stored."""
        self.session._session_key = "12345678"
        self.assertEqual(self.session.session_key, "12345678")

    def test_session_key_is_read_only(self):
        def set_session_key(session):
            session.session_key = session._get_new_session_key()

        with self.assertRaises(AttributeError):
            set_session_key(self.session)

    # Custom session expiry
    def test_default_expiry(self):
        # A normal session has a max age equal to settings
        self.assertEqual(self.session.get_expiry_age(), settings.SESSION_COOKIE_AGE)

        # So does a custom session with an idle expiration time of 0 (but it'll
        # expire at browser close)
        self.session.set_expiry(0)
        self.assertEqual(self.session.get_expiry_age(), settings.SESSION_COOKIE_AGE)

    def test_custom_expiry_seconds(self):
        modification = timezone.now()

        self.session.set_expiry(10)

        date = self.session.get_expiry_date(modification=modification)
        self.assertEqual(date, modification + timedelta(seconds=10))

        age = self.session.get_expiry_age(modification=modification)
        self.assertEqual(age, 10)

    def test_custom_expiry_timedelta(self):
        modification = timezone.now()

        # Mock timezone.now, because set_expiry calls it on this code path.
        original_now = timezone.now
        try:
            timezone.now = lambda: modification
            self.session.set_expiry(timedelta(seconds=10))
        finally:
            timezone.now = original_now

        date = self.session.get_expiry_date(modification=modification)
        self.assertEqual(date, modification + timedelta(seconds=10))

        age = self.session.get_expiry_age(modification=modification)
        self.assertEqual(age, 10)

    def test_custom_expiry_datetime(self):
        modification = timezone.now()

        self.session.set_expiry(modification + timedelta(seconds=10))

        date = self.session.get_expiry_date(modification=modification)
        self.assertEqual(date, modification + timedelta(seconds=10))

        age = self.session.get_expiry_age(modification=modification)
        self.assertEqual(age, 10)

    def test_custom_expiry_reset(self):
        self.session.set_expiry(None)
        self.session.set_expiry(10)
        self.session.set_expiry(None)
        self.assertEqual(self.session.get_expiry_age(), settings.SESSION_COOKIE_AGE)

    def test_get_expire_at_browser_close(self):
        # Tests get_expire_at_browser_close with different settings and different
        # set_expiry calls
        with override_settings(SESSION_EXPIRE_AT_BROWSER_CLOSE=False):
            self.session.set_expiry(10)
            self.assertFalse(self.session.get_expire_at_browser_close())

            self.session.set_expiry(0)
            self.assertTrue(self.session.get_expire_at_browser_close())

            self.session.set_expiry(None)
            self.assertFalse(self.session.get_expire_at_browser_close())

        with override_settings(SESSION_EXPIRE_AT_BROWSER_CLOSE=True):
            self.session.set_expiry(10)
            self.assertFalse(self.session.get_expire_at_browser_close())

            self.session.set_expiry(0)
            self.assertTrue(self.session.get_expire_at_browser_close())

            self.session.set_expiry(None)
            self.assertTrue(self.session.get_expire_at_browser_close())

    def test_decode(self):
        # Ensure we can decode what we encode
        data = {"a test key": "a test value"}
        encoded = self.session.encode(data)
        self.assertEqual(self.session.decode(encoded), data)

    @unittest.skipIf(
        django.VERSION[0] >= 5, "Django 5.x does not support PickleSerializer"
    )
    def test_actual_expiry(self):
        # this doesn't work with JSONSerializer (serializing timedelta)
        with override_settings(
            SESSION_SERIALIZER="django.contrib.sessions.serializers.PickleSerializer"
        ):
            self.session = self.backend()  # reinitialize after overriding settings

            # Regression test for #19200
            old_session_key = None
            new_session_key = None
            try:
                self.session["foo"] = "bar"
                self.session.set_expiry(-timedelta(seconds=10))
                self.session.save()
                old_session_key = self.session.session_key
                # With an expiry date in the past, the session expires instantly.
                new_session = self.backend(self.session.session_key)
                new_session_key = new_session.session_key
                self.assertNotIn("foo", new_session)
            finally:
                self.session.delete(old_session_key)
                self.session.delete(new_session_key)


class DatabaseSessionTestCase(SessionTestsMixin, TestCase):

    backend = DatabaseSession
    session_engine = "django_cassandra_engine.sessions.backends.db"

    @property
    def model(self):
        return self.backend.get_model_class()

    def test_session_str(self):
        self.session["x"] = 1
        self.session.save()

        session_key = self.session.session_key
        s = self.model.objects.get(session_key=session_key)

        self.assertEqual(force_str(s), session_key)

    def test_session_get_decoded(self):
        """
        Test we can use Session.get_decoded to retrieve data stored
        in normal way
        """
        self.session["x"] = 1
        self.session.save()

        s = self.model.objects.get(session_key=self.session.session_key)

        self.assertEqual(s.get_decoded(), {"x": 1})

    def test_clearsessions_command(self):
        """
        Test clearsessions command for clearing expired sessions.
        """
        # TODO


class CachedDatabaseSessionTestCase(SessionTestsMixin, TestCase):

    backend = CachedDatabaseSession
    session_engine = "django_cassandra_engine.sessions.backends.cached_db"

    def test_exists_searches_cache_first(self):
        self.session.save()
        with self.assertNumQueries(0):
            self.assertTrue(self.session.exists(self.session.session_key))

    @ignore_warnings(module="django.core.cache.backends.base")
    def test_load_overlong_key(self):
        self.session._session_key = (string.ascii_letters + string.digits) * 20
        self.assertEqual(self.session.load(), {})

    @override_settings(SESSION_CACHE_ALIAS="sessions")
    def test_non_default_cache(self):
        # 21000 - CacheDB backend should respect SESSION_CACHE_ALIAS.
        with self.assertRaises(InvalidCacheBackendError):
            self.backend()
