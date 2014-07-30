Django Cassandra Engine
=======================

django-cassandra-engine is a database wrapper for Django Framework.
It uses latest `Cqlengine <https://github.com/cqlengine/cqlengine>`_ which is currently the best Cassandra CQL 3 Object Mapper for Python.

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

.. code:: python

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

4. Run ``./manage.py syncdb``
5. Done!
