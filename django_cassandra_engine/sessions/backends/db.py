from django.contrib.sessions.backends.db import (
    SessionStore as DjangoSessionStore
)
from django.utils.functional import cached_property


class SessionStore(DjangoSessionStore):

    @classmethod
    def get_model_class(cls):
        """
        Avoid circular import
        """
        from django_cassandra_engine.sessions.models import Session
        return Session

    @cached_property
    def model(self):
        return self.get_model_class()

    def exists(self, session_key):
        try:
            self.model.objects.get(session_key=session_key)
            return True
        except self.model.DoesNotExist:
            return False

    def save(self, must_create=False):
        """
        Saves the current session data to the database. If 'must_create' is
        True, a database error will be raised if the saving operation doesn't
        create a *new* entry (as opposed to possibly updating an existing
        entry).

        :param must_create:
        """
        if self.session_key is None:
            return self.create()
        data = self._get_session(no_load=must_create)
        obj = self.create_model_instance(data)
        obj.save()

    @classmethod
    def clear_expired(cls):
        """
        # TODO: implement this
        """
