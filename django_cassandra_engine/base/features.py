import django

from django.db.backends.base.features import BaseDatabaseFeatures


class CassandraDatabaseFeatures(BaseDatabaseFeatures):
    string_based_auto_field = True
    supports_long_model_names = False
    supports_microsecond_precision = True
    supports_transactions = False
    can_rollback_ddl = True
    uses_savepoints = False
    requires_rollback_on_dirty_transaction = False
    atomic_transactions = True
