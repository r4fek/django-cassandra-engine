
# Django Cassandra Engine - the Cassandra backend for Django #

All tools you need to start your journey with Apache Cassandra and Django Framework!

[![Latest version](https://img.shields.io/pypi/v/django-cassandra-engine.svg "Latest version")](https://pypi.python.org/pypi/django-cassandra-engine/)
![workflow](https://github.com/r4fek/django-cassandra-engine/actions/workflows/tox.yml/badge.svg)

Discord: https://discord.gg/pxunMGmDNc
## Features ##

* integration with latest `python-driver` and optionally `dse-driver` from DataStax
* working `flush`, `migrate`, `sync_cassandra`, `inspectdb` and
  `dbshell` commands
* support for creating/destroying test database
* accepts all `Cqlengine` and `cassandra.cluster.Cluster` connection options
* automatic connection/disconnection handling
* works well along with relational databases (as secondary DB)
* storing sessions in Cassandra
* working django forms
* usable admin panel with Cassandra models
* support DataStax Astra cloud hosted Cassandra

## Sponsors ##
Help support ongoing development and maintenance by [sponsoring Django Cassandra Engine](https://github.com/sponsors/r4fek).

### Our Sponsors: ###
<table><tr>
<td align="center" width="300" ><a href="https://astra.dev/3xPljcu"><img src="https://www.datastax.com/sites/default/files/2021-07/astra-negative-square.png" width="90" height="90" alt="Astra DB" /><br />Astra DB</a><br/>Use Django with DataStax Astra DB - built on Apache Cassandra.</td>
<td align="center" width="300" ><a href="https://github.com/NoiSek"><img src="https://avatars.githubusercontent.com/u/631328?v=4" width="90" height="90" alt="NoiSek" /><br/>NoiSek</a></td>
</tr></table>


## Installation ##

Recommended installation:

    pip install django-cassandra-engine

## Basic Usage ##

1. Add `django_cassandra_engine` to `INSTALLED_APPS` in your `settings.py` file:

        INSTALLED_APPS = ('django_cassandra_engine',) + INSTALLED_APPS

2. Change `DATABASES` setting:

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

3. Define some model:

        # myapp/models.py

        import uuid
        from cassandra.cqlengine import columns
        from django_cassandra_engine.models import DjangoCassandraModel

        class ExampleModel(DjangoCassandraModel):
            example_id    = columns.UUID(primary_key=True, default=uuid.uuid4)
            example_type  = columns.Integer(index=True)
            created_at    = columns.DateTime()
            description   = columns.Text(required=False)

4. Run `./manage.py sync_cassandra`
5. Done!

## Connect to Cassandra with a Cloud Config bundle ##
To connect to a hosted Cassandra cluster that provides a secure connection bundle (ex. DataStax Astra) change the `DATABASES` setting of your settings.py:

        DATABASES = {
            'default': {
                'ENGINE': 'django_cassandra_engine',
                'NAME': 'keyspace_name',
                'TEST_NAME': 'table_name',
                'USER': 'token',
                'PASSWORD': token_value,
                'OPTIONS': {
                    'connection': {
                        'cloud': {
                            'secure_connect_bundle': '/path/to/secure/bundle.zip'
                        },
                    }
                }
            }
        }

## Documentation ##

The documentation can be found online [here](http://r4fek.github.io/django-cassandra-engine/).

## License ##
Copyright (c) 2014-2024, [Rafał Furmański](https://linkedin.com/in/furmanski).

All rights reserved. Licensed under BSD 2-Clause License.
