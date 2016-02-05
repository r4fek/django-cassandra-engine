from django_cassandra_engine.utils import get_cassandra_connections


for _, conn in get_cassandra_connections():
    conn.connect()
