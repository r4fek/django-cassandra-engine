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
        'RelatedAutoField':  'id',
    }

    def set_autocommit(self):
        """ There is no such thing in Cassandra """

    def create_test_db(self, verbosity=1, autoclobber=False, **kwargs):
        """
        Creates a test database, prompting the user for confirmation if the
        database already exists. Returns the name of the test database created.
        """

        # Don't import django.core.management if it isn't needed.
        from django.core.management import call_command
        from django.conf import settings

        # If using django-nose, its runner has already set the db name
        # to test_*, so restore it here so that all the models for the
        # live keyspace can be found.
        self.connection.connection.keyspace = \
            self.connection.settings_dict['NAME']
        test_database_name = self._get_test_db_name()

        # Set all models keyspace to the test keyspace
        self.set_models_keyspace(test_database_name)

        if verbosity >= 1:
            test_db_repr = ''
            if verbosity >= 2:
                test_db_repr = " ('%s')" % test_database_name
            print("Creating test database for alias '%s'%s..." % (
                self.connection.alias, test_db_repr))

        self.connection.connect()
        options = self.connection.settings_dict.get('OPTIONS', {})
        replication_opts = options.get('replication', {})
        strategy_class = replication_opts.pop('strategy_class',
                                              'SimpleStrategy')
        replication_factor = replication_opts.pop('replication_factor', 1)

        create_keyspace(self.connection.settings_dict['NAME'], strategy_class,
                        replication_factor, **replication_opts)

        settings.DATABASES[self.connection.alias]["NAME"] = test_database_name
        self.connection.settings_dict["NAME"] = test_database_name

        self.connection.reconnect()

        # Report syncdb messages at one level lower than that requested.
        # This ensures we don't get flooded with messages during testing
        # (unless you really ask to be flooded)
        call_command(
            'sync_cassandra',
            verbosity=max(verbosity - 1, 0),
            interactive=False,
            database=self.connection.alias,
            load_initial_data=False
        )

        return test_database_name

    def _destroy_test_db(self, test_database_name, verbosity=1, **kwargs):

        delete_keyspace(test_database_name)

    def set_models_keyspace(self, keyspace):
        """Set keyspace for all connection models"""
        for models in self.connection.introspection.cql_models.values():
            for model in models:
                model.__keyspace__ = keyspace
