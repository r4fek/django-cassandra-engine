
Django Cassandra Engine
=======================

.. image:: https://travis-ci.org/r4fek/django-cassandra-engine.svg?branch=master
    :target: https://travis-ci.org/r4fek/django-cassandra-engine

django-cassandra-engine is a database wrapper for Django Framework.
It uses latest `Cqlengine <https://github.com/cqlengine/cqlengine>`_ which is currently the best Cassandra CQL 3 Object Mapper for Python.

:License: 2-clause BSD
:Keywords: django, cassandra, orm, nosql, database, python
:URL (pypi): `django-cassandra-engine <https://pypi.python.org/pypi/django-cassandra-engine>`_

Requirements
------------

- cassandra
- cqlengine
- django-nonrel
- djangotoolbox


Features
--------

- complete django integration
- working syncdb and flush commands
- support for creating/destroying test database
- accept all Cqlengine connection options
- automatic connection/disconnection handling
- support for multiple databases (also relational)


Installation
------------

Recommended installation::

   pip install django-cassandra-engine
  

Usage
-----

#. Add django-cassandra-engine to ``INSTALLED_APPS`` in your settings.py file::

    INSTALLED_APPS += ('django_cassandra_engine',)
   

#. Also change ``DATABASES`` setting::

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


#. Define some model::

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

#. Run ``./manage.py syncdb``
#. Done!

Links
-----

* `Changelog`_


.. _Changelog: https://github.com/r4fek/django-cassandra-engine/blob/master/CHANGELOG.rst
