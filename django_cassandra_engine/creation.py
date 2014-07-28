from cqlengine.management import create_keyspace, delete_keyspace
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

    def _create_test_db(self, verbosity=1, autoclobber=False):

        self.connection.connect()
        options = self.connection.settings_dict.get('OPTIONS', {})
        replication_opts = options.get('replication', {})
        create_keyspace(self.connection.settings_dict['NAME'],
                        **replication_opts)

    def _destroy_test_db(self, test_database_name, verbosity=1):

        delete_keyspace(test_database_name)
        self.connection.close()
