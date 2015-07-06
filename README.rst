
Django Cassandra Engine
=======================

.. image:: https://pypip.in/version/django-cassandra-engine/badge.svg
    :target: https://pypi.python.org/pypi/django-cassandra-engine/
    :alt: Latest Version
.. image:: https://api.travis-ci.org/r4fek/django-cassandra-engine.svg?branch=master
    :target: https://travis-ci.org/r4fek/django-cassandra-engine
.. image:: https://pypip.in/download/django-cassandra-engine/badge.svg
    :target: https://pypi.python.org/pypi//django-cassandra-engine/
    :alt: Downloads
.. image:: https://codeclimate.com/github/r4fek/django-cassandra-engine/badges/gpa.svg
   :target: https://codeclimate.com/github/r4fek/django-cassandra-engine
   :alt: Code Climate


django-cassandra-engine is a database wrapper for Django Framework.
It uses the latest `cassandra-driver <https://github.com/datastax/python-driver>`_
while primarily utilizing `Cqlengine <https://github.com/cqlengine/cqlengine>`_
which is currently the best Cassandra CQL 3 Object Mapper for Python and was
integrated into `cassandra-driver`.

:License: 2-clause BSD
:Keywords: django, cassandra, orm, nosql, database, python
:URL (pypi): `django-cassandra-engine <https://pypi.python.org/pypi/django-cassandra-engine>`_


Installation
------------

Recommended installation::

   pip install django-cassandra-engine
  

Usage
-----

#. Add django-cassandra-engine to ``INSTALLED_APPS`` in your settings.py file::

    INSTALLED_APPS = ('django_cassandra_engine',) + INSTALLED_APPS
   

IMPORTANT: This app should be **the first app** on ``INSTALLED_APPS`` list.

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
    from cassandra.cqlengine import columns
    from cassandra.cqlengine.models import Model

    class ExampleModel(Model):
        read_repair_chance = 0.05 # optional - defaults to 0.1
        example_id      = columns.UUID(primary_key=True, default=uuid.uuid4)
        example_type    = columns.Integer(index=True)
        created_at      = columns.DateTime()
        description     = columns.Text(required=False)

#. Run ``./manage.py sync_cassandra``
#. Done!

Documentation
-------------

You can find `documentation here <http://r4fek.github.io/django-cassandra-engine/>`_.
