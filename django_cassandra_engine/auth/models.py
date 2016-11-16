from cassandra.cqlengine import columns, models
from django.contrib.auth.hashers import (
    make_password,
    check_password,
    is_password_usable,
)
from django.utils.crypto import salted_hmac


class AnonymousUser(object):
    pk = None
    username = ''
    is_staff = False
    is_active = False
    is_superuser = False

    def __str__(self):
        return 'AnonymousUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return 1  # instances always return the same hash value

    def set_password(self, raw_password):
        raise NotImplementedError(
            "Django doesn't provide a DB representation for AnonymousUser.")

    def check_password(self, raw_password):
        raise NotImplementedError(
            "Django doesn't provide a DB representation for AnonymousUser.")

    def has_usable_password(self):
        return False

    def is_anonymous(self):
        return True

    def is_authenticated(self):
        return False

    def get_username(self):
        return self.username


class BaseUser(models.Model):
    """
    Base abstract user model with useful methods for manipulating passwords
    """
    __abstract__ = True
    _password = None

    username = columns.Text(primary_key=True, max_length=255)
    password = columns.Text(max_length=255, required=True)
    email = columns.Text(max_length=255)

    verified = columns.Boolean(default=True)
    banned = columns.Boolean(default=False)
    is_staff = columns.Boolean(default=False)
    is_active = columns.Boolean(default=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password
        self.update(password=self.password)

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.

        :param raw_password: raw password to check
        """

        def setter(raw_password):
            self.set_password(raw_password)
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "auth.models.BaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()
