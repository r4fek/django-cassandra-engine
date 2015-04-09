try:
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor
except ImportError:
    try:
        from django.db.backends import BaseDatabaseSchemaEditor
    except ImportError:
        BaseDatabaseSchemaEditor = object


class CassandraDatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    # TODO: support cql statements

    def create_model(self, model):
        pass

    def delete_model(self, model):
        pass
