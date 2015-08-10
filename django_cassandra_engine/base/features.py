import django

if django.VERSION[0:2] >= (1, 8):
    from django.db.backends.base.features import BaseDatabaseFeatures
else:
    from django.db.backends import BaseDatabaseFeatures


class CassandraDatabaseFeatures(BaseDatabaseFeatures):
    string_based_auto_field = True
    supports_long_model_names = False
    supports_microsecond_precision = True
    can_rollback_ddl = True
    uses_savepoints = False
    requires_rollback_on_dirty_transaction = False
    atomic_transactions = True

    # Django 1.4 compatibility
    def _supports_transactions(self):
        return False

    supports_transactions = property(_supports_transactions)
