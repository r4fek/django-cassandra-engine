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

    def set_autocommit(self):
        """ There is no such thing in Cassandra """

    def create_test_db(self, verbosity=1, autoclobber=False):
        """
        Creates a test database, prompting the user for confirmation if the
        database already exists. Returns the name of the test database created.
        """

        # Don't import django.core.management if it isn't needed.
        from django.core.management import call_command
        from django.conf import settings

        test_database_name = self._get_test_db_name()

        if verbosity >= 1:
            test_db_repr = ''
            if verbosity >= 2:
                test_db_repr = " ('%s')" % test_database_name
            print("Creating test database for alias '%s'%s..." % (
                self.connection.alias, test_db_repr))

        self.connection.connect()
        options = self.connection.settings_dict.get('OPTIONS', {})
        replication_opts = options.get('replication', {})
        create_keyspace(self.connection.settings_dict['NAME'],
                        **replication_opts)

        settings.DATABASES[self.connection.alias]["NAME"] = test_database_name
        self.connection.settings_dict["NAME"] = test_database_name

        self.connection.reconnect()

        # Report syncdb messages at one level lower than that requested.
        # This ensures we don't get flooded with messages during testing
        # (unless you really ask to be flooded)
        call_command(
            'syncdb',
            verbosity=max(verbosity - 1, 0),
            interactive=False,
            database=self.connection.alias,
            load_initial_data=False)

        return test_database_name

    def _destroy_test_db(self, test_database_name, verbosity=1):

        delete_keyspace(test_database_name)
