
# Django Cassandra Engine - the Cassandra backend for Django #

All tools you need to start your journey with Apache Cassandra and Django Framework!

[![Latest version](https://img.shields.io/pypi/v/django-cassandra-engine.svg "Latest version")](https://pypi.python.org/pypi/django-cassandra-engine/)
[![CI](https://api.travis-ci.org/r4fek/django-cassandra-engine.svg?branch=master "CI")](https://travis-ci.org/r4fek/django-cassandra-engine)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/rrafek/5)

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
                'NAME': 'db_name',
                'TEST_NAME': 'db_name',
                'USER': username,
                'PASSWORD': password,
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

## Donation
If this project help you reduce time to develop, you can give me a cup of coffee :)

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/rrafek/5)

## License ##
Copyright (c) 2014-2020, [Rafał Furmański](https://linkedin.com/in/furmanski).

All rights reserved. Licensed under BSD 2-Clause License.
