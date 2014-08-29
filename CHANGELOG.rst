CHANGELOG
=========

Version 0.0.5 (29.08.2014)
--------------------------

* Improved models discovery
* Call the standard syncdb if the engine is not django_cassandra_engine
  (thanks to @ratm)

Version 0.0.4 (22.08.2014)
--------------------------

* Feature: add support for *flush* management command
* Bugfix: lock dependencies in setup.py
* add more tests


Version 0.0.3 (21.08.2014)
--------------------------

* Bugfix: Fix some issue in *flush* command (add dummy support for Django 1.6.6)


Version 0.0.2 (04.08.2014)
--------------------------

* Bugfix: Do not reconnect on every request


Version 0.0.1 (31.07.2014)
--------------------------

* Feature: allow to define cassandra backend in settings.py
* Feature: connect to the Cassandra database automatically on app startup
* Feature: *syncdb* management command
* Feature: support for django test framework
* Feature: Support for Cqlengine Object Mapper
