
# Django Cassandra Engine - the Cassandra backend for Django #

All tools you need to start your journey with Apache Cassandra and Django Framework!

[![Latest version](https://img.shields.io/pypi/v/django-cassandra-engine.svg "Latest version")](https://pypi.python.org/pypi/django-cassandra-engine/)
[![Downloads](https://img.shields.io/pypi/dm/django-cassandra-engine.svg "Downloads")](https://pypi.python.org/pypi/django-cassandra-engine/)
[![CI](https://api.travis-ci.org/r4fek/django-cassandra-engine.svg?branch=master "CI")](https://travis-ci.org/r4fek/django-cassandra-engine)
[![Code climate](https://codeclimate.com/github/r4fek/django-cassandra-engine/badges/gpa.svg "Code climate")](https://codeclimate.com/github/r4fek/django-cassandra-engine)

## Features ##

* integration with latest `python-driver` from DataStax
* working `flush`, `migrate`, `sync_cassandra`, `inspectdb` and 
  `dbshell` commands
* support for creating/destroying test database
* accepts all `Cqlengine` and `cassandra.cluster.Cluster` connection options
* automatic connection/disconnection handling
* works well along with relational databases (as secondary DB)
* storing sessions in Cassandra (NEW!)

## Plans (TODO) ##

* User model stored in Cassandra (auth module)
* Admin panel for Cassandra models
* Forms

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
        from cassandra.cqlengine.models import Model
        
        class ExampleModel(Model):
            example_id    = columns.UUID(primary_key=True, default=uuid.uuid4)
            example_type  = columns.Integer(index=True)
            created_at    = columns.DateTime()
            description   = columns.Text(required=False)

4. Run `./manage.py sync_cassandra`
5. Done!

## Documentation ##

The documentation can be found online [here](http://r4fek.github.io/django-cassandra-engine/).

## License ##
Copyright (c) 2014-2016, [Rafał Furmański](https://rafal-furmanski.com).

All rights reserved. Licensed under BSD 2-Clause License.
