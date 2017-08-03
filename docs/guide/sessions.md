# Django Cassandra Engine - Sessions

Two session backends backed up with Cassandra are available

* `django_cassandra_engine.sessions.backends.db`
* `django_cassandra_engine.sessions.backends.cached_db`

All you need to do is to enable one of them in your `settings.py` file:

``` python
    INSTALLED_APPS += ['django_cassandra_engine.sessions']
    SESSION_ENGINE = 'django_cassandra_engine.sessions.backends.db'
```

Then you need to sync session model with Cassandra:

``` sh
    $ python manage.py sync_cassandra
```

That's it.
