from cqlengine.management import sync_table, create_keyspace
from djangotoolbox.db.creation import NonrelDatabaseCreation


class DatabaseCreation(NonrelDatabaseCreation):

    data_types = {
        'AutoField':         'text',
        'BigIntegerField':   'long',
        'BooleanField':      'bool',
        'CharField':         'text',
        'CommaSeparatedIntegerField': 'text',
        'DateField':         'date',
        'DateTimeField':     'datetime',
        'DecimalField':      'decimal:%(max_digits)s,%(decimal_places)s',
        'EmailField':        'text',
        'FileField':         'text',
        'FilePathField':     'text',
        'FloatField':        'float',
        'ImageField':        'text',
        'IntegerField':      'int',
        'IPAddressField':    'text',
        'NullBooleanField':  'bool',
        'OneToOneField':     'integer',
        'PositiveIntegerField': 'int',
        'PositiveSmallIntegerField': 'int',
        'SlugField':         'text',
        'SmallIntegerField': 'integer',
        'TextField':         'text',
        'TimeField':         'time',
        'URLField':          'text',
        'XMLField':          'text',
        'GenericAutoField':  'id',
        'StringForeignKey':  'id',
        'AutoField':         'id',
        'RelatedAutoField':  'id',
    }

    def sql_create_model(self, model, style, known_models=set()):
        """
        Most NoSQL databases are mostly schema-less, no data
        definitions are needed.
        """

        #TODO
        options = self.connection.settings_dict.get('OPTIONS', {})
        replication_opts = options.get('replication', {})
        create_keyspace(self.connection.settings_dict['NAME'],
                        **replication_opts)
        sync_table(model, create_missing_keyspace=False)

        return [], {}

    def create_test_db(self, verbosity=1, autoclobber=False):
        raise NotImplementedError

    def destroy_test_db(self, old_database_name, verbosity=1):
        raise NotImplemented
