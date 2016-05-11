# Django Cassandra Engine - Troubleshooting

In case of any question please don't hesitate to ask!

## **Q:  `syncdb` only creates a keyspace..**

A: Please make sure that `django_cassandra_engine` is 
**the first application** in `INSTALLED_APPS` list.

It's also important to include your app to that list too.

## **Q:  Is it possible to use it with Celery?**

A: Short answer: YES.

If you use `django_cassandra_engine` as your default backend:

``` python
    # project/tasks.py
    from celery.signals import worker_init
    from django.db import connection

    @worker_process_init.connect
    def connect_db(**kwargs):
        connection.reconnect()
```

Or if 'cassandra' is your secondary DB alias:

``` python
    from django.db import connections
    connection = connections['cassandra']

    @worker_process_init.connect
    def connect_db(**kwargs):
        connection.reconnect()
```

## **Q: is uWSGI supported?**

A: Yes, uWSGI is supported by default. 
It works best with `retry_connect` set to `True` (in django settings).
It also requires that `lazy-apps = True` is set in `uwsgi.ini`.
