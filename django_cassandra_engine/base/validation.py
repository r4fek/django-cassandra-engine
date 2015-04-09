try:
    from django.db.backends.base.validation import BaseDatabaseValidation
except ImportError:
    from django.db.backends import BaseDatabaseValidation


class CassandraDatabaseValidation(BaseDatabaseValidation):
    pass
