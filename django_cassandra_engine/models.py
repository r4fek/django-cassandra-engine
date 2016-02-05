from django_cassandra_engine.utils import get_cassandra_connection


cassandra_connection = get_cassandra_connection()
if cassandra_connection is not None:
    cassandra_connection.connect()
