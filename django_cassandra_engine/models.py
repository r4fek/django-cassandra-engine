from django.db import connections


cassandra_connection = None

for alias in connections:
    engine = connections[alias].settings_dict.get('ENGINE', '')
    if engine == 'django_cassandra_engine':
        cassandra_connection = connections[alias]


try:
    from uwsgidecorators import postfork
except ImportError:
    # We're not in a uWSGI context, no need to hook Cassandra session
    # initialization to the postfork event.
    if cassandra_connection is not None:
        cassandra_connection.connect()
else:
    @postfork
    def cassandra_init():
        """ Initialize a new Cassandra session in the context.

        Ensures that a new session is returned for every new request.
        """
        if cassandra_connection is not None:
            cassandra_connection.reconnect()
