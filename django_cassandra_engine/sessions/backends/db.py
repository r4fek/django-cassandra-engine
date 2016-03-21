from datetime import datetime
import logging

from django.contrib.sessions.backends.db import (
    SessionStore as DjangoSessionStore
)
from django.core.exceptions import SuspiciousOperation
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.contrib.sessions.backends import db

# monkey patch for Django versions older than 1.9
from django_cassandra_engine.sessions.models import Session as CassandraSession
db.Session = CassandraSession


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

    def create_model_instance(self, data):
        """
        Return a new instance of the session model object, which represents the
        current session state. Intended to be used for saving the session data
        to the database.
        :param data:
        """
        return self.model(
            session_key=self._get_or_create_session_key(),
            session_data=self.encode(data),
            expire_date=self.get_expiry_date(),
        )

    def load(self):
        try:
            s = self.model.objects.get(session_key=self.session_key)
            if s.expire_date <= datetime.now():
                s.delete()
                raise SuspiciousOperation('old session detected')
            return self.decode(s.session_data)
        except (self.model.DoesNotExist, SuspiciousOperation) as e:
            if isinstance(e, SuspiciousOperation):
                logger = logging.getLogger('django.security.%s' %
                                           e.__class__.__name__)
                logger.warning(force_text(e))
            self.create()
            return {}

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

    def delete(self, session_key=None):
        if session_key is None:
            if not self.session_key:
                return
            session_key = self.session_key

        self.model.objects.filter(session_key=session_key).delete()

    @classmethod
    def clear_expired(cls):
        """
        # TODO: implement this
        """
