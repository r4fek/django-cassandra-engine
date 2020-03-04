from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class CassandraDatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    def prepare_default(self, value):
        return value

    def quote_value(self, value):
        return value

    def create_model(self, model):
        # Hack to disable checking migrations for cassandra connection
        try:
            from django.db.migrations.exceptions import (
                MigrationSchemaMissing as Exc,
            )
        except ImportError:
            from django.core.exceptions import ImproperlyConfigured as Exc
        raise Exc('No schema for cassandra database')

    def delete_model(self, model):
        pass
