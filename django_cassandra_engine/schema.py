try:
    from django.db.backends.schema import BaseDatabaseSchemaEditor
except ImportError:
    BaseDatabaseSchemaEditor = object


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    # TODO: support cql statements

    def create_model(self, model):
        pass

    def delete_model(self, model):
        pass
