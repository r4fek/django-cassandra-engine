from django.db import connections


for alias in connections:
    engine = connections[alias].settings_dict.get('ENGINE', '')
    if engine == 'django_cassandra_engine':
        connections[alias].connect()
