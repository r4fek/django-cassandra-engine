# django-cassandra-engine docs

## Overview

*django-cassandra-engine* is a database wrapper for *Django Framework*.
It uses latest *Cqlengine*, which is currently the best Cassandra CQL 3 Object Mapper for Python.

---

## Features

* working `syncdb` and `flush` commands
* support for creating/destroying test database
* accepts all `Cqlengine` and `cassandra.Cluster` connection options
* automatic connection/disconnection handling
* support for multiple databases (also relational)

---

## Requirements

* Cassandra (of course)
* cqlengine
* django-nonrel
* djangotoolbox
* Django (1.6 or 1.7)

---

## Download

[Github](https://github.com/r4fek/django-cassandra-engine)

[PyPi](https://pypi.python.org/pypi/django-cassandra-engine)

---

## Installation

You can install it easily from PyPi by single command:

    pip install django-cassandra-engine

or clone source code and run:

    python setup.py install

---

## Getting started

1.  Add django-cassandra-engine to `INSTALLED_APPS` in your settings.py file:

        INSTALLED_APPS += ('django_cassandra_engine',)


`IMPORTANT`: This app should be last on `INSTALLED_APPS` list.

2.  Change `DATABASES` setting:

        DATABASES = {
            'default': {
                'ENGINE': 'django_cassandra_engine',
                'NAME': 'db',
                'TEST_NAME': 'test_db',
                'HOST': 'db1.example.com,db2.example.com',
                'OPTIONS': {
                    'replication': {
                        'strategy_class': 'SimpleStrategy',
                        'replication_factor': 1
                    }
                }
            }
        }

3.  Define some model:

        #  myapp/models.py
        import uuid
        from cqlengine import columns
        from cqlengine.models import Model

        class ExampleModel(Model):
            read_repair_chance = 0.05 # optional - defaults to 0.1
            example_id      = columns.UUID(primary_key=True, default=uuid.uuid4)
            example_type    = columns.Integer(index=True)
            created_at      = columns.DateTime()
            description     = columns.Text(required=False)

4.  Run `./manage.py syncdb` in order to sync your models with Cassandra.

5.  Thats all!

---

## Advanced usage

Sometimes you want to use cassandra database along with your RDMS.
This is also possible! Just define your `DATABASES` like here:

    from cassandra import ConsistencyLevel

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
        'cassandra': {
            'ENGINE': 'django_cassandra_engine',
            'NAME': 'db',
            'TEST_NAME': 'test_db',
            'HOST': '127.0.0.1',
            'OPTIONS': {
                'replication': {
                    'strategy_class': 'SimpleStrategy',
                    'replication_factor': 1
                },
                'connection': {
                    'consistency': ConsistencyLevel.ONE,
                    'lazy_connect': False,
                    'retry_connect': False
                    # + All connection options for cassandra.Cluster()
                }
            }
        }
    }

Then run `./manage.py syncdb` for your regular database and
`./manage.py syncdb --database cassandra` for Cassandra DB.

All `cassandra.Cluster` options are well described [here](http://datastax.github.io/python-driver/api/cassandra/cluster.html).

