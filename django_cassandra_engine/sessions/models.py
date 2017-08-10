from ..compat import Model, columns


class AbstractBaseSession(Model):
    __abstract__ = True

    session_key = columns.Text(primary_key=True, max_length=40)
    expire_date = columns.DateTime()

    session_data = columns.Text()

    def __str__(self):
        return self.session_key

    @classmethod
    def get_session_store_class(cls):
        raise NotImplementedError

    def get_decoded(self):
        session_store_class = self.get_session_store_class()
        return session_store_class().decode(self.session_data)

    def encode(self, session_dict):
        """
        Return the given session dictionary serialized and encoded as a string.
        :param session_dict:
        """
        session_store_class = self.get_session_store_class()
        return session_store_class().encode(session_dict)


class Session(AbstractBaseSession):

    @classmethod
    def get_session_store_class(cls):
        from django_cassandra_engine.sessions.backends.db import SessionStore
        return SessionStore
