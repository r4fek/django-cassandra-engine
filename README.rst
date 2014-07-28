Django Cassandra Engine
=======================

django-cassandra-engine is a database wrapper for Django Framework.
It uses latest ``cqlengine`` which is currently the best Cassandra CQL 3 Object Mapper for Python.

Installation
------------

Recommended installation::

  pip install git+https://github.com/r4fek/django-cassandra-engine
  

Usage
-----

1. Add django-cassandra-engine to ``INSTALLED_APPS`` in your settings.py file::

.. code:: python

   INSTALLED_APPS += ('django_cassandra_engine',)
   
2. Also change ``DATABASES`` setting:

.. code:: python

   DATABASES = {
       'default': {
           'ENGINE': 'django_cassandra_engine',
           'NAME': 'keyspace',
           'TEST_NAME': 'test_keyspace',
           'HOST': 'db1.example.com,db2.example.com',
           'OPTIONS': {
               'replication': {
                   'strategy_class': 'SimpleStrategy',
                   'replication_factor': 1
               }
           }
       }  
   }

3. DONE!