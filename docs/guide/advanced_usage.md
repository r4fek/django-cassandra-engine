# Django Cassandra Engine - Advanced Usage

## Cassandra as secondary database

Sometimes you want to use cassandra database along with your relational database.
This is also possible! Just define your `DATABASES` like below:

``` python
    from cassandra import ConsistencyLevel

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
        'cassandra': {
            'ENGINE': 'django_cassandra_engine',
            'NAME': 'db',
            'USER': 'user',
            'PASSWORD': 'pass',
            'TEST_NAME': 'test_db',
            'HOST': '127.0.0.1',
            'OPTIONS': {
                'replication': {
                    'strategy_class': 'SimpleStrategy',
                    'replication_factor': 1
                },
                'connection': {
                    'consistency': ConsistencyLevel.LOCAL_ONE,
                    'retry_connect': True
                    # + All connection options for cassandra.cluster.Cluster()
                },
                'session': {
                    'default_timeout': 10,
                    'default_fetch_size': 10000
                    # + All options for cassandra.cluster.Session()
                }
            }
        }
    }
```

Then run `./manage.py syncdb` for your regular database and
`./manage.py sync_cassandra` or `./manage.py syncdb --database cassandra`
for Cassandra DB.

All `cassandra.cluster.Cluster` and `cassandra.cluster.Session` options are well described
<a href="http://datastax.github.io/python-driver/api/cassandra/cluster.html" target="_blank" rel="nofollow">
    here
</a>.

## Using internal authorization

If you want to use
<a href="http://www.datastax.com/documentation/cassandra/2.1/cassandra/security/secure_config_native_authorize_t.html" target="_blank" rel="nofollow">
    internal authorization
</a>
just provide `USER` and `PASSWORD` in cassandra's database alias.

``` python
    ...
    'cassandra' {
        'ENGINE': 'django_cassandra_engine',
        'NAME': 'db',
        'USER': 'user',
        'PASSWORD': 'pass'
    }
```

You can also pass custom
<a href="http://datastax.github.io/python-driver/api/cassandra/auth.html#cassandra.auth.PlainTextAuthProvider" target="_blank" rel="nofollow">
    auth_provider
</a>
to `connection` dict:

``` python
    ...
    'connection': {
        'consistency': ConsistencyLevel.LOCAL_ONE,
        'retry_connect': True,
        'port': 9042,
        'auth_provider': PlainTextAuthProvider(username='user', password='password')
        # + All connection options for cassandra.cluster.Cluster()
    }
```

## Performing raw database queries

You might need to perform queries that don't map cleanly to models,
or directly execute `UPDATE`, `INSERT`, or `DELETE` queries.

In these cases, you can always access the database directly,
routing around the model layer entirely:

``` python
    from django.db import connection
    cursor = connection.cursor()
    result = cursor.execute("SELECT COUNT(*) FROM users")
    print result[0]['count']
```

---

That was easy! Show me some useful [management commands](management_commands.md) now.
